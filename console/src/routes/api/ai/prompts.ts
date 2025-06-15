/**
 * 提示词存储文件
 * 集中管理所有AI提示词，避免在前端暴露
 */

// 查询最近神秘事件的提示词
export const queryRecentMysteriousEventsPrompt = `请生成过去一周内（从今天算起）全球范围内发生的5个最神秘、最不可思议的真实事件。
这些事件应该具有神秘性、不明性或超自然性质，例如UFO目击、神秘现象、无法解释的自然事件等。

请确保这些事件是真实的，基于新闻报道或可靠来源，而不是虚构的。

对于每个事件，请提供以下信息，并以JSON格式返回：
1. 标题：简洁描述事件
2. 内容：使用Markdown格式的详细描述
3. 日期：事件发生的具体日期（YYYY-MM-DD格式）
4. 地点：事件发生的具体地点
5. 相关人物：涉及的人物及其角色
6. 事件摘要：100-200字的简短摘要
7. 分类：事件属于的类别（如"urban"、"paranormal"、"supernatural"、"mysterious"、"unexplained"、"phenomena"）
8. 标签：相关关键词

请以下面的JSON格式返回结果：
{
  "events": [
    {
      "title": "事件标题",
      "content": "详细描述（Markdown格式）",
      "date": "YYYY-MM-DD",
      "location_data": {"name": "地点名称", "lat": 纬度, "lng": 经度},
      "entities_data": {
        "people": [{"name": "人物名称", "role": "角色"}],
        "locations": [{"name": "地点名称", "description": "描述"}],
        "timeline": [{"time": "时间", "event": "事件描述"}]
      },
      "summary": "事件摘要",
      "categories": ["分类1", "分类2"],
      "tags": ["标签1", "标签2"]
    }
  ]
}
`;

// 从Markdown内容中提取实体的提示词
export const extractEntitiesPrompt = (markdownContent: string) => `
  请从以下Markdown内容中提取所有实体，包括：
  1. 人物：所有提到的人名及其角色
  2. 地点：所有提到的地理位置及其描述
  3. 时间线：按时间顺序排列的事件

  请以JSON格式返回结果，格式如下：
  {
    "people": [
      {"name": "人物名称", "role": "角色"}
    ],
    "locations": [
      {"name": "地点名称", "description": "描述"}
    ],
    "timeline": [
      {"time": "时间", "event": "事件描述"}
    ]
  }

  以下是Markdown内容：
  ${markdownContent}
`;

// 从Markdown内容生成摘要的提示词
export const generateSummaryPrompt = (markdownContent: string) => `
  请为以下Markdown内容生成一个简洁的摘要。摘要应该：
  1. 长度在100-200字之间
  2. 捕捉内容的主要观点和关键信息
  3. 使用客观、清晰的语言
  4. 不包含个人观点或评价

  以下是Markdown内容：
  ${markdownContent}
`;

// 从Markdown内容生成标题的提示词
export const generateTitlePrompt = (markdownContent: string) => `
  请为以下Markdown内容生成一个吸引人的标题。标题应该：
  1. 长度在10-30个字符之间
  2. 简洁有力，能够吸引读者注意
  3. 准确反映内容的主题
  4. 不使用夸张或误导性的表述

  以下是Markdown内容：
  ${markdownContent}
`;

// 获取分类和标签的提示词
export const getCategoriesAndTagsPrompt = (markdownContent: string) => `
  请为以下内容生成最多5个分类和10个标签。分类应该是广泛的主题领域，而标签应该是具体的关键词。
  请以JSON格式返回结果，格式如下：
  {
    "categories": ["分类1", "分类2", ...],
    "tags": ["标签1", "标签2", ...]
  }

  以下是内容：
  ${markdownContent}
`;