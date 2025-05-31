import { streamText, tool } from 'ai';
import { createGoogleGenerativeAI } from '@ai-sdk/google';
import { createAISDKTools } from '@agentic/ai-sdk';
import { DuckDuckGoClient } from '@agentic/duck-duck-go';
import { PUBLIC_GEMINI_API_KEY } from '$env/static/public';
import { z } from 'zod';
import type { RequestHandler } from './$types';

const google = createGoogleGenerativeAI({
  apiKey: PUBLIC_GEMINI_API_KEY || 'your-gemini-api-key-here',
});

// Initialize DuckDuckGo client for search functionality
const duckduckgo = new DuckDuckGoClient();

// Define additional tools
// const searchTool = tool({
//   description: 'Search the web for current information',
//   parameters: z.object({
//     query: z.string().describe('The search query'),
//   }),
//   execute: async ({ query }) => {
//     try {
//       const results = await duckduckgo.search(query, { maxResults: 5 });
//       return {
//         results: results.map(r => ({
//           title: r.title,
//           snippet: r.snippet,
//           url: r.url
//         }))
//       };
//     } catch (error) {
//       return { error: 'Search failed', message: error.message };
//     }
//   },
// });

export const POST: RequestHandler = async ({ request }) => {
  try {
    console.log('Chat API request received');
    const { messages } = await request.json();

    const result = streamText({
      model: google('models/gemini-2.0-flash-exp'),
      messages,
      tools: {
        // search: searchTool,
        ...createAISDKTools(duckduckgo),
      },
      maxSteps: 5,
      temperature: 0.7,
      system: 'You are a helpful AI assistant. You can search the web for current information when needed. Be concise and helpful.',
    });

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