import { generateText } from 'ai';
import { createGoogleGenerativeAI } from '@ai-sdk/google';
import { PUBLIC_GEMINI_API_KEY } from '$env/static/public';
import { ProxyAgent } from 'undici';
import type { RequestHandler } from './$types';
import * as prompts from '../prompts';

// 强制使用本地代理，确保URL格式正确
const proxyUrl = 'http://127.0.0.1:7890';
const proxyAgent = new ProxyAgent(proxyUrl);

// 初始化Google AI SDK
const google = createGoogleGenerativeAI({
  apiKey: PUBLIC_GEMINI_API_KEY,
  fetch: (input: string | URL | globalThis.Request, init?: globalThis.RequestInit) => {
    const fetchOptions = {
      ...init,
      dispatcher: proxyAgent
    };
    return fetch(input, fetchOptions);
  },
});

export const POST: RequestHandler = async ({ request }) => {
  try {
    const { prompt, promptType, markdownContent, model = 'gemini-1.5-flash', temperature = 0.7, maxOutputTokens = 2048 } = await request.json();

    // 根据promptType选择对应的提示词
    let finalPrompt = prompt;
    if (promptType && !prompt) {
      switch (promptType) {
        case 'queryRecentMysteriousEvents':
          finalPrompt = prompts.queryRecentMysteriousEventsPrompt;
          break;
        case 'extractEntities':
          if (!markdownContent) {
            return new Response(
              JSON.stringify({ error: 'markdownContent is required for extractEntities prompt' }),
              { status: 400, headers: { 'Content-Type': 'application/json' } }
            );
          }
          finalPrompt = prompts.extractEntitiesPrompt(markdownContent);
          break;
        case 'generateSummary':
          if (!markdownContent) {
            return new Response(
              JSON.stringify({ error: 'markdownContent is required for generateSummary prompt' }),
              { status: 400, headers: { 'Content-Type': 'application/json' } }
            );
          }
          finalPrompt = prompts.generateSummaryPrompt(markdownContent);
          break;
        case 'generateTitle':
          if (!markdownContent) {
            return new Response(
              JSON.stringify({ error: 'markdownContent is required for generateTitle prompt' }),
              { status: 400, headers: { 'Content-Type': 'application/json' } }
            );
          }
          finalPrompt = prompts.generateTitlePrompt(markdownContent);
          break;
        case 'getCategoriesAndTags':
          if (!markdownContent) {
            return new Response(
              JSON.stringify({ error: 'markdownContent is required for getCategoriesAndTags prompt' }),
              { status: 400, headers: { 'Content-Type': 'application/json' } }
            );
          }
          finalPrompt = prompts.getCategoriesAndTagsPrompt(markdownContent);
          break;
        default:
          return new Response(
            JSON.stringify({ error: 'Invalid promptType' }),
            { status: 400, headers: { 'Content-Type': 'application/json' } }
          );
      }
    }

    if (!finalPrompt) {
      return new Response(
        JSON.stringify({ error: 'Prompt is required' }),
        {
          status: 400,
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
    }

    // 使用 ai-sdk 的 generateText 生成内容
    const result = await generateText({
      model: google(`models/${model}`),
      prompt: finalPrompt,
      temperature: temperature,
      maxTokens: maxOutputTokens,
      
      // onError({ error }) {
      //   console.error('GenerateText error:', error);
      // },
    });

    return new Response(
      JSON.stringify({ text: result }),
      {
        status: 200,
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

  } catch (error) {
    console.error('AI Generate API error:', error);
    return new Response(
      JSON.stringify({ error: `Internal server error: ${error instanceof Error ? error.message : 'Unknown error'}` }),
      {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
  }
};