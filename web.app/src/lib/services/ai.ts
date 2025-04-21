import {
  GoogleGenerativeAI,
  HarmCategory,
  HarmBlockThreshold,
} from "@google/generative-ai";
// import { env } from '$env/dynamic/private'; // Use dynamic private env for server-side

// API Key 将作为参数传递，不再在此处直接导入或检查

// 全局的 genAI 和 model 实例将被移除，改为在函数内部根据传入的 key 初始化

const generationConfig = {
  temperature: 0.9,
  topK: 1,
  topP: 1,
  maxOutputTokens: 2048, // 根据需要调整
};

// 安全设置，阻止不当内容
const safetySettings = [
  {
    category: HarmCategory.HARM_CATEGORY_HARASSMENT,
    threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
  },
  {
    category: HarmCategory.HARM_CATEGORY_HATE_SPEECH,
    threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
  },
  {
    category: HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
    threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
  },
  {
    category: HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
    threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
  },
];

interface GenerateEventArgs {
  apiKey: string; // 添加 API Key 参数
  name?: string;
  url?: string;
  description?: string; // 添加 description 参数
}

interface GenerateEventResult {
  title: string;
  content: string;
  eventTime?: string; // 新增：事件发生时间
  entities?: {
    people?: Array<{name: string; role: string}>;
    locations?: Array<{name: string; description: string; coordinates?: {lat: number; lng: number}}>;
    timeline?: Array<{time: string; event: string}>;
  };
}

// 定义公共的 Prompt 部分
const JSON_FORMAT_INSTRUCTION = `
请以 JSON 格式返回结果，包含以下字段：
- title: 事件标题
- content: 使用Markdown格式的详细事件内容描述
- eventTime: 事件发生的时间或时间段 (例如: '2023年5月', '1945年8月15日', '公元前221年')
- entities: 包含以下子字段的JSON对象：
  - people: 人物数组，每个人物包含name（姓名）和role（角色）
  - locations: 地点数组，每个地点包含name（地点名称）、description（简短描述），如果是真实地点还要包含coordinates（地理坐标，格式为{lat: number, lng: number}）
  - timeline: 时间线数组，每个时间点包含time（时间）和event（事件描述）`;

const JSON_EXAMPLE = `
例如：
{
  "title": "探索珠穆朗玛峰：一次惊心动魄的登山之旅",
  "content": "## 珠穆朗玛峰登山探险\n\n2023年5月，我参与了一次珠穆朗玛峰的登山探险活动。这次旅程充满了挑战和惊险..\n\n### 准备阶段\n\n我们花了三个月的时间进行体能训练和高海拔适应...\n\n### 登山过程\n\n登山过程中，我们遇到了暴风雪，不得不在海拔6500米的地方停留两天...",
  "eventTime": "2023年5月",
  "entities": {
    "people": [
      {"name": "张三", "role": "登山队长"},
      {"name": "李四", "role": "向导"},
      {"name": "王五", "role": "医疗顾问"}
    ],
    "locations": [
      {"name": "珠穆朗玛峰", "description": "世界最高峰，海拔8848.86米", "coordinates": {"lat": 27.9881, "lng": 86.9250}},
      {"name": "珠峰大本营", "description": "登山起点，海拔5200米", "coordinates": {"lat": 28.0025, "lng": 86.8530}}
    ],
    "timeline": [
      {"time": "2023-05-01", "event": "抵达珠峰大本营"},
      {"time": "2023-05-10", "event": "开始正式登山"},
      {"time": "2023-05-15", "event": "遭遇暴风雪"},
      {"time": "2023-05-20", "event": "成功登顶"}
    ]
  }
}`;

/**
 * 使用 AI 根据事件名称或 URL 生成标题和内容摘要。
 * @param args 包含 API 密钥、事件名称或 URL 的对象
 * @returns 返回包含生成标题和内容的对象
 */
export async function generateEventContent(
  args: GenerateEventArgs
): Promise<GenerateEventResult> {
  if (!args.apiKey) {
    throw new Error("未提供 Gemini API 密钥。");
  }

  // 在函数内部初始化 AI 客户端和模型
  const genAI = new GoogleGenerativeAI(args.apiKey);
  const model = genAI.getGenerativeModel({
    model: "gemini-1.5-flash", // 确保模型名称正确
  });

  if (!model) {
    // 这个检查理论上不应该触发，因为上面已经初始化了
    throw new Error("Gemini AI 模型初始化失败。");
  }

  let prompt = "";
  const baseInstruction = `重要提示：请基于真实事件和事实生成内容，不要虚构信息。如果用户提供的信息不足，请基于可靠的历史事实和公开信息补充，而不是创造虚构内容。确保所有信息都是真实准确的。`;

  if (args.description) {
    prompt = `根据以下用户提供的经历描述，生成一个吸引人的中文标题和详细的事件内容，以及相关的人物、地点、时间线等实体信息。

${baseInstruction}

经历描述："${args.description}"
${JSON_FORMAT_INSTRUCTION}
${JSON_EXAMPLE}`;
  } else if (args.name) {
    prompt = `根据以下事件名称，生成一个吸引人的中文标题和详细的事件内容，以及相关的人物、地点、时间线等实体信息。

重要提示：请基于真实事件和事实生成内容，不要虚构信息。如果事件名称指向的是真实历史事件，请基于可靠的历史记录和公开信息生成内容。确保所有信息都是真实准确的。

事件名称："${args.name}"
${JSON_FORMAT_INSTRUCTION}`;
  } else if (args.url) {
    let context = "";
    try {
      // 尝试 fetch 页面内容
      const response = await fetch(args.url);
      if (!response.ok) {
        throw new Error(`无法访问链接: ${response.status} ${response.statusText}`);
      }
      const pageText = await response.text();
      context = pageText
        .replace(/<style[^>]*>.*?<\/style>/gs, "")
        .replace(/<script[^>]*>.*?<\/script>/gs, "")
        .replace(/<[^>]+>/g, " ")
        .replace(/\s{2,}/g, " ")
        .trim()
        .substring(0, 2000);

      if (!context) {
        throw new Error("无法从链接中提取有效文本内容。");
      }

      prompt = `根据以下从链接 ${args.url} 提取的内容片段，生成一个吸引人的中文标题和详细的事件内容，以及相关的人物、地点、时间线等实体信息。

重要提示：请仅基于提供的链接内容生成真实事件的描述，不要虚构信息。如果链接内容不足，请只基于已有信息生成，而不是创造虚构内容。确保所有信息都是真实准确的。

内容片段："${context}..."
${JSON_FORMAT_INSTRUCTION}`;
    } catch (fetchError: any) {
      console.error(`获取或处理 URL 内容失败: ${args.url}`, fetchError);
      prompt = `无法获取链接 ${args.url} 的内容。请基于这个链接本身，生成一个吸引人的中文标题和详细的事件内容，以及相关的人物、地点、时间线等实体信息。

重要提示：请基于链接的 URL 信息生成内容，但只生成你确定是真实的信息。如果无法确定链接指向的内容，请生成非常简洁的内容，只包含你能确定的信息，而不是创造虚构内容。确保所有信息都是真实准确的。
${JSON_FORMAT_INSTRUCTION}`;
    }
  } else {
    throw new Error("必须提供事件名称、URL 或经历描述。");
  }

  try {
    const result = await model.generateContent({
      contents: [{ role: "user", parts: [{ text: prompt }] }],
      generationConfig,
      safetySettings,
    });

    const response = result.response;
    const responseText = response.text();

    // 尝试解析 AI 返回的 JSON
    try {
      // 预处理响应文本，删除可能的 Markdown 代码块标记
      let cleanedText = responseText;

      // 删除开头的 ```json 或 ``` 标记
      if (cleanedText.startsWith('```json')) {
        cleanedText = cleanedText.substring(7);
      } else if (cleanedText.startsWith('```')) {
        cleanedText = cleanedText.substring(3);
      }

      // 删除结尾的 ``` 标记
      if (cleanedText.endsWith('```')) {
        cleanedText = cleanedText.substring(0, cleanedText.length - 3);
      }

      // 删除首尾空白字符
      cleanedText = cleanedText.trim();

      console.log('清理后的文本:', cleanedText);

      // 尝试解析 JSON
      const parsedResult: GenerateEventResult = JSON.parse(cleanedText);
      if (parsedResult.title && parsedResult.content) {
        // 确保返回结果包含 eventTime 字段，即使它是 undefined
        return { ...parsedResult, eventTime: parsedResult.eventTime };
      } else {
        console.error("AI 返回的 JSON 格式不正确:", responseText);
        throw new Error("AI 返回的 JSON 格式不正确。请检查 Gemini API 的响应或 Prompt。原始响应：" + responseText);
      }
    } catch (parseError) {
      console.error(
        "解析 AI 响应失败:",
        parseError,
        "\n原始响应:",
        responseText
      );

      // 尝试提取 JSON 部分
      try {
        const jsonMatch = responseText.match(/\{[\s\S]*\}/);
        if (jsonMatch) {
          const jsonText = jsonMatch[0];
          console.log('提取到的 JSON 文本:', jsonText);

          const extractedResult: GenerateEventResult = JSON.parse(jsonText);
          if (extractedResult.title && extractedResult.content) {
            console.log('成功从文本中提取并解析 JSON');
            // 确保返回结果包含 eventTime 字段，即使它是 undefined
            return { ...extractedResult, eventTime: extractedResult.eventTime };
          }
        }
      } catch (extractError) {
        console.error('尝试提取 JSON 失败:', extractError);
      }

      // 如果所有解析尝试都失败，则使用原始文本
      let fallbackTitle = "AI 生成内容";
      if (args.description) {
        fallbackTitle = `关于“${args.description.substring(0, 20)}...”的 AI 生成内容`;
      } else if (args.name) {
        fallbackTitle = `关于 ${args.name} 的 AI 生成内容`;
      } else if (args.url) {
        fallbackTitle = `关于链接 ${args.url} 的 AI 生成内容`;
      }
      // 返回包含原始文本和错误信息的对象，以便前端可以显示更友好的错误
      return {
        title: fallbackTitle,
        content: `AI 响应解析失败。原始响应：\n\n${responseText}`,
        eventTime: undefined // 确保 fallback 也有 eventTime
      };
    }
  } catch (error) {
    console.error("调用 Gemini API 时出错:", error);
    // 抛出更具体的错误信息
    if (error instanceof Error) {
      throw new Error(`AI 内容生成失败: ${error.message}`);
    } else {
      throw new Error("AI 内容生成失败，发生未知错误。请稍后再试。");
    }
  }
}

// 可以添加其他 AI 相关服务函数
// 注意：现在 aiService 只是一个包含函数的对象，调用时需要传递 apiKey
export const aiService = {
  generateEventContent,
};
