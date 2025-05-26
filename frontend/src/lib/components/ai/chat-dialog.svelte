<script lang="ts">
  import { onMount } from "svelte";
  import {
    Loader2,
    Send,
    Image,
    Mic,
    X,
  } from "lucide-svelte";
  import { GoogleGenerativeAI } from "@google/generative-ai";
  import { PUBLIC_GEMINI_API_KEY } from "$env/static/public";

  // Props
  let {
    open = $bindable(false),
    apiKey = PUBLIC_GEMINI_API_KEY,
    modelName = "gemini-1.5-flash",
    placeholder = "描述你的图片...",
    initialMessages = [],
    onclose,
  } = $props<{
    open?: boolean;
    apiKey?: string;
    modelName?: string;
    placeholder?: string;
    initialMessages?: ChatMessage[];
    onclose?: () => void;
  }>();

  // Types
  type ChatMessage = {
    role: "user" | "model";
    content: string;
    timestamp: Date;
  };

  // State
  let messages = $state<ChatMessage[]>(initialMessages);
  let inputText = $state("");
  let isLoading = $state(false);
  let error = $state<string | null>(null);
  let textareaElement = $state<HTMLTextAreaElement | null>(null);
  let scrollAreaRef = $state<HTMLDivElement | null>(null);

  // AI Client
  let genAI: GoogleGenerativeAI;
  let model: any;

  onMount(() => {
    initializeAI();
  });

  function initializeAI() {
    try {
      genAI = new GoogleGenerativeAI(apiKey);
      model = genAI.getGenerativeModel({
        model: modelName,
      });
    } catch (err) {
      console.error("初始化 AI 失败:", err);
      error = "无法初始化 AI 服务，请检查 API 密钥。";
    }
  }

  function autoResizeTextarea() {
    if (!textareaElement) return;

    // Reset height to auto to get the correct scrollHeight
    textareaElement.style.height = "auto";

    // Set the height to scrollHeight
    const newHeight = Math.min(textareaElement.scrollHeight, 150);
    textareaElement.style.height = `${newHeight}px`;
  }

  async function sendMessage() {
    if (!inputText.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      role: "user",
      content: inputText.trim(),
      timestamp: new Date(),
    };

    messages = [...messages, userMessage];
    inputText = "";

    if (textareaElement) {
      textareaElement.style.height = "auto";
    }

    isLoading = true;
    error = null;

    try {
      // Prepare chat history for the AI
      const chatHistory = messages.map(msg => ({
        role: msg.role === "user" ? "user" : "model",
        parts: [{ text: msg.content }]
      }));

      // Send to AI
      const result = await model.generateContent({
        contents: chatHistory,
        generationConfig: {
          temperature: 0.7,
          topK: 1,
          topP: 0.95,
          maxOutputTokens: 1024,
        },
      });

      const response = result.response;
      const responseText = response.text();

      // Add AI response to messages
      const aiMessage: ChatMessage = {
        role: "model",
        content: responseText,
        timestamp: new Date(),
      };

      messages = [...messages, aiMessage];

    } catch (err) {
      console.error("AI 响应失败:", err);
      error = err instanceof Error ? err.message : "AI 响应失败，请稍后再试。";
    } finally {
      isLoading = false;

      // Scroll to bottom after a short delay to ensure content is rendered
      setTimeout(() => {
        if (scrollAreaRef) {
          scrollAreaRef.scrollTop = scrollAreaRef.scrollHeight;
        }
      }, 100);
    }
  }

  function handleKeyDown(event: KeyboardEvent) {
    // Send message on Enter (without Shift)
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  }

  function closeDialog() {
    open = false;
    onclose?.();
  }

  // Watch for initialMessages changes
  $effect(() => {
    if (initialMessages.length > 0) {
      messages = [...initialMessages];
    }
  });
</script>

<div class="modal modal-bottom sm:modal-middle {open ? 'modal-open' : ''}" role="dialog">
  <div class="modal-box max-w-md">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4 pb-2 border-b">
      <div class="flex items-center gap-2">
        <div class="avatar placeholder">
          <div class="bg-primary text-primary-content rounded-full w-8">
            <span>G</span>
          </div>
        </div>
        <span class="font-medium">Google AI</span>
      </div>
      <button class="btn btn-sm btn-circle btn-ghost" onclick={closeDialog}>
        <X class="h-4 w-4" />
      </button>
    </div>

    <!-- Chat Messages -->
    <div class="overflow-y-auto h-[400px] p-2" bind:this={scrollAreaRef}>
      <div class="flex flex-col gap-4">
        {#if messages.length === 0}
          <div class="text-center opacity-60 py-8">
            <p>开始与 Google AI 对话</p>
          </div>
        {/if}

        {#each messages as message}
          <div class="chat {message.role === 'user' ? 'chat-end' : 'chat-start'}">
            <div class="chat-bubble {message.role === 'user' ? 'chat-bubble-primary' : 'chat-bubble-neutral'}">
              <p class="whitespace-pre-wrap break-words">{message.content}</p>
            </div>
          </div>
        {/each}

        {#if isLoading}
          <div class="chat chat-start">
            <div class="chat-bubble chat-bubble-neutral flex items-center justify-center">
              <Loader2 class="h-5 w-5 animate-spin opacity-70" />
            </div>
          </div>
        {/if}

        {#if error}
          <div class="flex justify-center">
            <div class="alert alert-error text-sm">
              <p>{error}</p>
            </div>
          </div>
        {/if}
      </div>
    </div>

    <!-- Input Area -->
    <div class="mt-4 pt-2 border-t">
      <div class="join w-full">
        <textarea
          class="textarea textarea-bordered join-item flex-grow min-h-[60px] max-h-[150px] resize-none focus:outline-none"
          bind:value={inputText}
          bind:this={textareaElement}
          placeholder={placeholder}
          oninput={autoResizeTextarea}
          onkeydown={handleKeyDown}
        ></textarea>

        <div class="join-item flex flex-col">
          <button class="btn btn-ghost btn-sm" disabled={isLoading}>
            <Image class="h-4 w-4 opacity-70" />
          </button>
          <button class="btn btn-ghost btn-sm" disabled={isLoading}>
            <Mic class="h-4 w-4 opacity-70" />
          </button>
          <button
            class="btn btn-primary btn-sm"
            onclick={sendMessage}
            disabled={isLoading || !inputText.trim()}
          >
            <Send class="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  </div>
  <form method="dialog" class="modal-backdrop">
    <button onclick={closeDialog}>关闭</button>
  </form>
</div>
