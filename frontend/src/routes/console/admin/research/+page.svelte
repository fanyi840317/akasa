<script lang="ts">
  import { onMount } from 'svelte';
  import { Send, Plus, MessageSquare, Trash2, Edit3, Bot, History } from 'lucide-svelte';
  import { GoogleGenerativeAI } from '@google/generative-ai';
  import { PUBLIC_GEMINI_API_KEY } from '$env/static/public';
  import { marked } from 'marked';
  import { fly, fade } from 'svelte/transition';
  import { sineOut } from 'svelte/easing';

  type Message = {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
  };

  type Conversation = {
    id: string;
    title: string;
    messages: Message[];
    lastUpdated: Date;
  };

  let conversations = $state<Conversation[]>([]);
  let currentConversation = $state<Conversation | null>(null);
  let inputText = $state('');
  let isLoading = $state(false);
  let showSidebar = $state(true);
  let genAI: GoogleGenerativeAI;
  let model: any;

  const STORAGE_KEY = 'ai-conversations';

  onMount(() => {
    initializeAI();
    loadConversations();
  });

  function initializeAI() {
    try {
      genAI = new GoogleGenerativeAI(PUBLIC_GEMINI_API_KEY);
      model = genAI.getGenerativeModel({
        model: 'gemini-1.5-flash',
      });
    } catch (err) {
      console.error('初始化 AI 失败:', err);
    }
  }

  function generateId() {
    return Math.random().toString(36).substring(2, 15) + Date.now().toString(36);
  }

  function saveConversations() {
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(conversations));
    }
  }

  function loadConversations() {
    if (typeof localStorage !== 'undefined') {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        try {
          const parsed = JSON.parse(stored);
          conversations = parsed.map((conv: any) => ({
            ...conv,
            lastUpdated: new Date(conv.lastUpdated),
            messages: conv.messages.map((msg: any) => ({
              ...msg,
              timestamp: new Date(msg.timestamp)
            }))
          }));
        } catch (err) {
          console.error('加载对话失败:', err);
        }
      }
    }
  }

  function createNewConversation() {
    const newConv: Conversation = {
      id: generateId(),
      title: '新对话',
      messages: [],
      lastUpdated: new Date()
    };
    conversations = [newConv, ...conversations];
    currentConversation = newConv;
    saveConversations();
  }

  function selectConversation(conv: Conversation) {
    currentConversation = conv;
  }

  function deleteConversation(conv: Conversation) {
    conversations = conversations.filter(c => c.id !== conv.id);
    if (currentConversation?.id === conv.id) {
      currentConversation = null;
    }
    saveConversations();
  }

  function updateConversationTitle(conv: Conversation, newTitle: string) {
    const index = conversations.findIndex(c => c.id === conv.id);
    if (index !== -1) {
      conversations[index].title = newTitle;
      saveConversations();
    }
  }

  async function sendMessage() {
    if (!inputText.trim() || isLoading) return;
    
    if (!currentConversation) {
      createNewConversation();
    }

    const userMessage: Message = {
      id: generateId(),
      role: 'user',
      content: inputText.trim(),
      timestamp: new Date()
    };

    // 添加用户消息
    if (currentConversation) {
      currentConversation.messages = [...currentConversation.messages, userMessage];
      currentConversation.lastUpdated = new Date();
      
      // 如果是第一条消息，更新标题
      if (currentConversation.messages.length === 1) {
        const title = inputText.length > 30 ? inputText.substring(0, 30) + '...' : inputText;
        currentConversation.title = title;
      }
      
      saveConversations();
    }

    const messageText = inputText;
    inputText = '';
    isLoading = true;

    try {
      // 准备对话历史
      const chatHistory = currentConversation?.messages.map(msg => ({
        role: msg.role === 'user' ? 'user' : 'model',
        parts: [{ text: msg.content }]
      })) || [];

      const chat = model.startChat({
        history: chatHistory.slice(0, -1), // 排除当前消息
        generationConfig: {
          temperature: 0.9,
          topK: 1,
          topP: 0.95,
          maxOutputTokens: 2048,
        },
      });

      const result = await chat.sendMessage(messageText);
      const response = result.response;
      const responseText = response.text();

      const aiMessage: Message = {
        id: generateId(),
        role: 'assistant',
        content: responseText,
        timestamp: new Date()
      };

      if (currentConversation) {
        currentConversation.messages = [...currentConversation.messages, aiMessage];
        currentConversation.lastUpdated = new Date();
        saveConversations();
      }
    } catch (err) {
      console.error('AI 响应失败:', err);
      const errorMessage: Message = {
        id: generateId(),
        role: 'assistant',
        content: '抱歉，我遇到了一些问题。请稍后再试。',
        timestamp: new Date()
      };
      
      if (currentConversation) {
        currentConversation.messages = [...currentConversation.messages, errorMessage];
        saveConversations();
      }
    } finally {
      isLoading = false;
      
      // 滚动到底部
      setTimeout(() => {
        const chatContainer = document.querySelector('.chat-container');
        if (chatContainer) {
          chatContainer.scrollTop = chatContainer.scrollHeight;
        }
      }, 100);
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  }

  function renderMarkdown(content: string): string {
    try {
      return marked(content) as string;
    } catch (err) {
      console.error('Markdown渲染失败:', err);
      return content;
    }
  }

  // 计算是否有对话
  let hasConversations = $derived(conversations.length > 0);
  let hasCurrentMessages = $derived(currentConversation?.messages.length > 0);
</script>

<div class="flex h-screen bg-base-100 rounded-2xl border border-base-300 ">
  <!-- 侧边栏 -->
  {#if showSidebar}
    <div class="w-80 bg-base-200 border-r border-base-300 flex flex-col" transition:fly={{ x: -320, duration: 300 }}>
      <!-- 头部 -->
      <div class="p-4 border-b border-base-300">
        <button 
          onclick={createNewConversation}
          class="w-full btn btn-primary btn-sm gap-2"
        >
          <Plus class="w-4 h-4" />
          新对话
        </button>
      </div>
      
      <!-- 对话列表 -->
      <div class="flex-1 overflow-y-auto p-2">
        {#if hasConversations}
          {#each conversations as conv (conv.id)}
            <div 
              class="p-3 rounded-lg mb-2 cursor-pointer transition-colors group relative
                     {currentConversation?.id === conv.id ? 'bg-primary/10 border border-primary/20' : 'hover:bg-base-300'}"
              onclick={() => selectConversation(conv)}
            >
              <div class="flex items-start justify-between">
                <div class="flex-1 min-w-0">
                  <h3 class="text-sm font-medium truncate text-base-content">
                    {conv.title}
                  </h3>
                  <p class="text-xs text-base-content/60 mt-1">
                    {conv.lastUpdated.toLocaleDateString()}
                  </p>
                </div>
                <button 
                  onclick={() => deleteConversation(conv)}
                  class="opacity-0 group-hover:opacity-100 btn btn-ghost btn-xs text-error"
                >
                  <Trash2 class="w-3 h-3" />
                </button>
              </div>
            </div>
          {/each}
        {:else}
          <div class="text-center text-base-content/50 mt-8">
            <History class="w-8 h-8 mx-auto mb-2 opacity-50" />
            <p class="text-sm">暂无对话历史</p>
          </div>
        {/if}
      </div>
    </div>
  {/if}

  <!-- 主内容区 -->
  <div class="flex-1 flex flex-col">
    <!-- 顶部栏 -->
    <div class="h-16 border-b border-base-300 flex items-center justify-between px-6">
      <div class="flex items-center gap-3">
        <button 
          onclick={() => showSidebar = !showSidebar}
          class="btn btn-ghost btn-sm"
        >
          <MessageSquare class="w-4 h-4" />
        </button>
        <div class="flex items-center gap-2">
          <Bot class="w-5 h-5 text-primary" />
          <h1 class="text-lg font-semibold">AI 助手</h1>
        </div>
      </div>
      
      {#if currentConversation}
        <div class="text-sm text-base-content/60">
          {currentConversation.messages.length} 条消息
        </div>
      {/if}
    </div>

    <!-- 聊天区域 -->
    <div class="flex-1 flex flex-col">
      {#if currentConversation}
        <!-- 消息列表 -->
        <div class="flex-1 overflow-y-auto chat-container p-6">
          {#if hasCurrentMessages}
            <div class="max-w-4xl mx-auto space-y-6">
              {#each currentConversation.messages as message (message.id)}
                <div class="flex gap-4 {message.role === 'user' ? 'justify-end' : 'justify-start'}">
                  {#if message.role === 'assistant'}
                    <div class="w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                      <Bot class="w-4 h-4 text-primary-content" />
                    </div>
                  {/if}
                  
                  <div class="max-w-3xl {message.role === 'user' ? 'order-first' : ''}">
                    <div class="
                      {message.role === 'user' 
                        ? 'bg-primary text-primary-content ml-auto' 
                        : 'bg-base-200 text-base-content'} 
                      rounded-2xl px-4 py-3 {message.role === 'user' ? 'rounded-br-sm' : 'rounded-bl-sm'}
                    ">
                      {#if message.role === 'assistant'}
                        <div class="prose prose-sm max-w-none">
                          {@html renderMarkdown(message.content)}
                        </div>
                      {:else}
                        <p class="whitespace-pre-wrap">{message.content}</p>
                      {/if}
                    </div>
                    <div class="text-xs text-base-content/50 mt-1 {message.role === 'user' ? 'text-right' : 'text-left'}">
                      {message.timestamp.toLocaleTimeString()}
                    </div>
                  </div>
                  
                  {#if message.role === 'user'}
                    <div class="w-8 h-8 rounded-full bg-base-300 flex items-center justify-center flex-shrink-0">
                      <span class="text-sm font-medium">你</span>
                    </div>
                  {/if}
                </div>
              {/each}
              
              {#if isLoading}
                <div class="flex gap-4 justify-start" transition:fade>
                  <div class="w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                    <Bot class="w-4 h-4 text-primary-content" />
                  </div>
                  <div class="bg-base-200 rounded-2xl rounded-bl-sm px-4 py-3">
                    <div class="flex items-center gap-2">
                      <div class="loading loading-dots loading-sm"></div>
                      <span class="text-sm text-base-content/70">正在思考...</span>
                    </div>
                  </div>
                </div>
              {/if}
            </div>
          {:else}
            <div class="flex items-center justify-center h-full">
              <div class="text-center">
                <Bot class="w-16 h-16 mx-auto mb-4 text-base-content/30" />
                <h2 class="text-xl font-semibold text-base-content/70 mb-2">开始新对话</h2>
                <p class="text-base-content/50">输入您的问题，我会尽力帮助您</p>
              </div>
            </div>
          {/if}
        </div>
      {:else}
        <!-- 欢迎界面 -->
        <div class="flex-1 flex items-center justify-center">
          <div class="text-center max-w-md" transition:fly={{ y: 20, duration: 300, easing: sineOut }}>
            <Bot class="w-20 h-20 mx-auto mb-6 text-primary" />
            <h1 class="text-3xl font-bold text-base-content mb-4">AI 助手</h1>
            <p class="text-base-content/70 mb-8">选择一个对话或创建新对话开始聊天</p>
            <button 
              onclick={createNewConversation}
              class="btn btn-primary btn-lg gap-2"
            >
              <Plus class="w-5 h-5" />
              开始新对话
            </button>
          </div>
        </div>
      {/if}

      <!-- 输入区域 -->
      {#if currentConversation}
        <div class="border-t border-base-300 p-6">
          <div class="max-w-4xl mx-auto">
            <div class="flex gap-3">
              <textarea
                bind:value={inputText}
                onkeydown={handleKeydown}
                placeholder="输入消息..."
                class="textarea textarea-bordered flex-1 resize-none min-h-[2.5rem] max-h-32"
                rows="1"
                disabled={isLoading}
              ></textarea>
              <button 
                onclick={sendMessage}
                disabled={!inputText.trim() || isLoading}
                class="btn btn-primary btn-square"
              >
                <Send class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      {/if}
    </div>
  </div>
</div>

<style>
  .chat-container {
    scroll-behavior: smooth;
  }
  
  .prose {
    color: inherit;
  }
  
  .prose h1, .prose h2, .prose h3, .prose h4, .prose h5, .prose h6 {
    color: inherit;
    margin-top: 1em;
    margin-bottom: 0.5em;
  }
  
  .prose p {
    margin-top: 0.5em;
    margin-bottom: 0.5em;
  }
  
  .prose code {
    background-color: rgba(0, 0, 0, 0.1);
    padding: 0.2em 0.4em;
    border-radius: 0.25em;
    font-size: 0.875em;
  }
  
  .prose pre {
    background-color: rgba(0, 0, 0, 0.05);
    padding: 1em;
    border-radius: 0.5em;
    overflow-x: auto;
  }
  
  .prose pre code {
    background-color: transparent;
    padding: 0;
  }
</style>