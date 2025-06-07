
import { eventStore } from "$lib/stores/event";
import type { Event } from "$lib/types/event";


// AI分析结果接口
export interface AIAnalysisResult {
  title?: string;
  summary?: string;
  entities?: {
    people?: Array<{ name: string; role: string }>;
    locations?: Array<{
      name: string;
      description: string;
      coordinates?: { lat: number; lng: number };
    }>;
    timeline?: Array<{ time: string; event: string }>;
  };
  categories?: string[];
  tags?: string[];
}

/**
 * 自动保存或更新事件数据
 * @param event 事件数据
 * @returns 保存后的事件数据
 */
export async function autoSaveEvent(event: Event): Promise<Event | null> {
  try {
    // 检查事件是否已存在（有ID）
    if (event.$id) {
      // 更新现有事件
      return await eventStore.updateEvent(event.$id, event);
    } else {
      // 创建新事件
      return await eventStore.createEvent(event);
    }
  } catch (error) {
    console.error("自动保存事件失败:", error);
    throw new Error(
      `自动保存事件失败: ${error instanceof Error ? error.message : "未知错误"}`
    );
  }
}

/**
 * 查询最近一周的神秘事件
 * @returns 神秘事件列表
 */
export async function queryRecentMysteriousEvents(): Promise<Event[]> {
  try {
    // 使用API调用，通过promptType指定使用服务端的提示词
    const response = await fetch("/api/ai/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        promptType: "queryRecentMysteriousEvents",
        model: "gemini-1.5-flash",
        temperature: 0.7,
        maxOutputTokens: 2048,
      }),
    });

    if (!response.ok) {
      throw new Error(`API调用失败: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    const text = data.text;

    // 解析JSON结果
    try {
      // 提取JSON部分
      const jsonMatch = text.match(/\{[\s\S]*\}/s);
      if (!jsonMatch) {
        throw new Error("无法从AI响应中提取JSON数据");
      }

      const data = JSON.parse(jsonMatch[0]);
      return data.events || [];
    } catch (parseError) {
      console.error("解析AI响应失败:", parseError);
      throw new Error(
        `解析AI响应失败: ${
          parseError instanceof Error ? parseError.message : "未知错误"
        }`
      );
    }
  } catch (error) {
    console.error("查询神秘事件失败:", error);
    throw new Error(
      `查询神秘事件失败: ${error instanceof Error ? error.message : "未知错误"}`
    );
  }
}

/**
 * 从Markdown内容中提取实体
 * @param markdownContent Markdown格式的内容
 * @returns 提取的实体JSON字符串
 */
export async function extractEntitiesFromMarkdown(
  markdownContent: string
): Promise<string> {
  try {
    // 使用API调用，通过promptType指定使用服务端的提示词
    const response = await fetch("/api/ai/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        promptType: "extractEntities",
        markdownContent,
        model: "gemini-1.5-flash",
        temperature: 0.7,
        maxOutputTokens: 2048,
      }),
    });

    if (!response.ok) {
      throw new Error(`API调用失败: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    const text = data.text;

    // 提取JSON部分
    const jsonMatch = text.match(/\{[\s\S]*\}/m);
    if (!jsonMatch) {
      throw new Error("无法从AI响应中提取JSON数据");
    }

    return jsonMatch[0];
  } catch (error) {
    console.error("提取实体失败:", error);
    throw new Error(
      `提取实体失败: ${error instanceof Error ? error.message : "未知错误"}`
    );
  }
}

/**
 * 从Markdown内容生成摘要
 * @param markdownContent Markdown格式的内容
 * @returns 生成的摘要
 */
export async function generateSummaryFromMarkdown(
  markdownContent: string
): Promise<string> {
  try {
    // 使用API调用，通过promptType指定使用服务端的提示词
    const response = await fetch("/api/ai/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        promptType: "generateSummary",
        markdownContent,
        model: "gemini-1.5-flash",
        temperature: 0.7,
        maxOutputTokens: 2048,
      }),
    });

    if (!response.ok) {
      throw new Error(`API调用失败: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    return data.text;
  } catch (error) {
    console.error("生成摘要失败:", error);
    throw new Error(
      `生成摘要失败: ${error instanceof Error ? error.message : "未知错误"}`
    );
  }
}

/**
 * 从Markdown内容生成标题
 * @param markdownContent Markdown格式的内容
 * @returns 生成的标题
 */
export async function generateTitleFromMarkdown(
  markdownContent: string
): Promise<string> {
  try {
    // 使用API调用，通过promptType指定使用服务端的提示词
    const response = await fetch("/api/ai/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        promptType: "generateTitle",
        markdownContent,
        model: "gemini-1.5-flash",
        temperature: 0.7,
        maxOutputTokens: 2048,
      }),
    });

    if (!response.ok) {
      throw new Error(`API调用失败: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    return data.text;
  } catch (error) {
    console.error("生成标题失败:", error);
    throw new Error(
      `生成标题失败: ${error instanceof Error ? error.message : "未知错误"}`
    );
  }
}

/**
 * 对Markdown内容进行综合AI分析
 * @param markdownContent Markdown格式的内容
 * @returns AI分析结果
 */
export async function comprehensiveAIAnalysis(
  markdownContent: string
): Promise<AIAnalysisResult> {
  try {
    // 并行执行多个AI任务
    const [title, summary, entitiesJson] = await Promise.all([
      generateTitleFromMarkdown(markdownContent),
      generateSummaryFromMarkdown(markdownContent),
      extractEntitiesFromMarkdown(markdownContent),
    ]);

    // 解析实体JSON
    const entities = JSON.parse(entitiesJson);

    // 使用API调用获取分类和标签
    const categoriesResponse = await fetch("/api/ai/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        promptType: "getCategoriesAndTags",
        markdownContent,
        model: "gemini-1.5-flash",
        temperature: 0.7,
        maxOutputTokens: 2048,
      }),
    });

    if (!categoriesResponse.ok) {
      throw new Error(
        `API调用失败: ${categoriesResponse.status} ${categoriesResponse.statusText}`
      );
    }

    const categoriesData = await categoriesResponse.json();
    const categoriesText = categoriesData.text;

    // 提取JSON部分
    const categoriesJsonMatch = categoriesText.match(/\{[\s\S]*\}/m);
    if (!categoriesJsonMatch) {
      throw new Error("无法从AI响应中提取分类和标签数据");
    }

    // const categoriesData = JSON.parse(categoriesJsonMatch[0]);

    // 返回综合分析结果
    return {
      title,
      summary,
      entities,
      categories: categoriesData.categories,
      tags: categoriesData.tags,
    };
  } catch (error) {
    console.error("综合AI分析失败:", error);
    throw new Error(
      `综合AI分析失败: ${error instanceof Error ? error.message : "未知错误"}`
    );
  }
}

/**
 * 将AI分析结果应用到事件并保存
 * @param event 要更新的事件
 * @param markdownContent Markdown格式的内容
 * @returns 更新后的事件
 */
export async function adoptAIAnalysisToEvent(
  event: Event,
  markdownContent: string
): Promise<Event | null> {
  try {
    // 进行综合AI分析
    const analysisResult = await comprehensiveAIAnalysis(markdownContent);

    // 更新事件数据
    const updatedEvent: Event = {
      ...event,
      title: analysisResult.title || event.title,
      content: markdownContent,
      summary: analysisResult.summary || event.summary,
      categories: analysisResult.categories || event.categories,
      entities_data:
        JSON.stringify(analysisResult.entities?.locations?.[0] || {}) ||
        event.entities_data,
      tags: analysisResult.tags || event.tags,
    };

    // 自动保存更新后的事件
    return await autoSaveEvent(updatedEvent);
  } catch (error) {
    console.error("应用AI分析到事件失败:", error);
    throw new Error(
      `应用AI分析到事件失败: ${
        error instanceof Error ? error.message : "未知错误"
      }`
    );
  }
}

/**
 * 批量处理事件并应用AI分析
 * @param events 要处理的事件列表
 * @returns 处理后的事件列表
 */
export async function batchProcessEventsWithAI(
  events: Event[]
): Promise<Event[]> {
  try {
    const processedEvents: Event[] = [];

    // 逐个处理事件
    for (const event of events) {
      if (!event.content) {
        // 如果事件没有内容，跳过处理
        processedEvents.push(event);
        continue;
      }

      // 应用AI分析并保存
      const processedEvent = await adoptAIAnalysisToEvent(event, event.content);
      if (processedEvent) {
        processedEvents.push(processedEvent);
      }
    }

    return processedEvents;
  } catch (error) {
    console.error("批量处理事件失败:", error);
    throw new Error(
      `批量处理事件失败: ${error instanceof Error ? error.message : "未知错误"}`
    );
  }
}
