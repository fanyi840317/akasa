import { streamText, tool } from 'ai';
import { createGoogleGenerativeAI } from '@ai-sdk/google';
// import { createAISDKTools } from '@agentic/ai-sdk';
import { DuckDuckGoClient } from '@agentic/duck-duck-go';
import { PUBLIC_GEMINI_API_KEY,PUBLIC_HTTPS_PROXY ,PUBLIC_HTTP_PROXY} from '$env/static/public';
import { z } from 'zod';
import { ProxyAgent } from 'undici';
import type { RequestHandler } from './$types';
// import { fetch as undiciFetch } from 'undici';

// 配置代理（如果需要）
console.log('HTTPS_PROXY:', PUBLIC_HTTPS_PROXY);
console.log('HTTP_PROXY:', PUBLIC_HTTP_PROXY);
// 强制使用本地代理，确保URL格式正确
const proxyUrl = PUBLIC_HTTPS_PROXY || PUBLIC_HTTP_PROXY || 'http://127.0.0.1:7890';
console.log('Using proxy URL:', proxyUrl);
const proxyAgent = new ProxyAgent(proxyUrl);

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

// Initialize DuckDuckGo client for search functionality with error handling
const duckduckgo = new DuckDuckGoClient();

// Define additional tools with enhanced error handling
const searchTool = tool({
  description: 'Search the web for current information',
  parameters: z.object({
    query: z.string().describe('The search query'),
  }),
  execute: async ({ query }) => {
    try {
      // Add timeout and retry logic
      // const results = await Promise.race([
      //   duckduckgo.search(query),
      //   new Promise((_, reject) => 
      //     setTimeout(() => reject(new Error('Search timeout')), 10000)
      //   )
      // ]) as Array<{ title: string; description: string; url: string }>;
      
      // return {
      //   results: results.map(r => ({
      //     title: r.title,
      //     description: r.description,
      //     url: r.url
      //   }))
      // };
      const results = await duckduckgo.search(query);
      console.log('DuckDuckGo search results:', results); // Log the results for debugging
      return {
        results: results.map(r => ({
          title: r.title,
          description: r.description,
          url: r.url
        }))
      };
    } catch (error) {
      console.warn('DuckDuckGo search failed:', (error as Error).message);
      // Return a graceful fallback message instead of throwing
      return { 
        error: 'Search temporarily unavailable', 
        message: 'DuckDuckGo search is currently experiencing issues. This may be due to rate limiting or VQD extraction problems.',
        fallback: 'Please try rephrasing your query or ask me to provide information based on my training data.'
      };
    }
  },
});

export const POST: RequestHandler = async ({ request }) => {
  try {
    const { messages } = await request.json();

    const result = await streamText({
      model: google('models/gemini-2.0-flash-exp'),
      messages: messages,
      tools: {
        search_web: searchTool
      },
      maxSteps: 5,
      temperature: 0.7,
      onError({ error }) {
        console.error('StreamText error:', error);
      },
    });
    // console.log('Chat API response:', result);
  return result.toDataStreamResponse();
 

  } catch (error) {
    console.error('Chat API error:', error);
    return new Response(
      JSON.stringify({ error: 'Internal server error' }),
      {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
  }
};