<script lang="ts">
  import { ScrollArea } from "../ui/scroll-area";
  import ChatMessages from "./chat-messages.svelte";
  import InputArea from "./input-area.svelte";
  import type { Message } from "@ai-sdk/svelte";

  // Props
  let {
    messages = $bindable([]),
    status = $bindable("ready"),
    error = $bindable(undefined),
    input = $bindable(""),
    windowHeight = 600,
    onCopyMessage,
    onRegenerateMessage,
    onLikeMessage,
    onDislikeMessage,
    onMessageSent, // 消息发送后的回调
  } = $props<{
    messages?: Message[];
    status?: string;
    error?: any;
    input?: string;
    windowHeight?: number;
    onCopyMessage?: (messageId: string) => void;
    onRegenerateMessage?: (messageId: string) => void;
    onLikeMessage?: (messageId: string) => void;
    onDislikeMessage?: (messageId: string) => void;
    onMessageSent?: (text: string) => void; // 消息发送后的回调
  }>();

  // State
  let scrollAreaRef = $state<HTMLDivElement | null>(null);

  // 滚动到底部函数
  function scrollToBottom() {
    if (scrollAreaRef) {
      scrollAreaRef.scrollTop = scrollAreaRef.scrollHeight;
    }
  }

  // 处理消息发送
  function handleSubmit(text: string) {
    console.log('Message submitted:', text);
    
    // 直接在组件内处理消息发送逻辑
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: text,
      createdAt: new Date()
    };
    
    // 添加用户消息到消息列表
    messages = [...messages, userMessage];
    
    // 更新状态为提交中
    status = "submitted";
    
    // 如果需要，可以调用父组件提供的回调
    onMessageSent?.(text);
    
    // 发送后清空输入框
    input = "";
    
    // 滚动到底部
    setTimeout(() => {
      scrollToBottom();
    }, 100);
    
    // 模拟AI响应（实际项目中应该通过API获取）
    simulateAiResponse();
  }
  
  // 模拟AI响应（实际项目中应该替换为真实的API调用）
  function simulateAiResponse() {
    setTimeout(() => {
      const aiMessage: Message = {
        id: `ai-${Date.now()}`,
        role: 'assistant',
        content: '这是一个模拟的AI响应。在实际项目中，你应该通过API获取真实的响应。',
        createdAt: new Date()
      };
      
      // 添加AI消息到消息列表
      messages = [...messages, aiMessage];
      
      // 更新状态为就绪
      status = "ready";
      
      // 滚动到底部
      setTimeout(() => {
        scrollToBottom();
      }, 100);
    }, 1000); // 模拟1秒延迟
  }
  
  // 处理复制消息
  function handleCopyMessage(messageId: string) {
    const message = messages.find((m: { id: string; }) => m.id === messageId);
    if (message) {
      navigator.clipboard.writeText(message.content);
      console.log('Message copied:', messageId);
    }
    
    // 如果需要，可以调用父组件提供的回调
    onCopyMessage?.(messageId);
  }
  
  // 处理重新生成消息
  function handleRegenerateMessage(messageId: string) {
    console.log('Regenerate message:', messageId);
    
    // 如果需要，可以调用父组件提供的回调
    onRegenerateMessage?.(messageId);
  }
  
  // 处理点赞消息
  function handleLikeMessage(messageId: string) {
    console.log('Like message:', messageId);
    
    // 如果需要，可以调用父组件提供的回调
    onLikeMessage?.(messageId);
  }
  
  // 处理点踩消息
  function handleDislikeMessage(messageId: string) {
    console.log('Dislike message:', messageId);
    
    // 如果需要，可以调用父组件提供的回调
    onDislikeMessage?.(messageId);
  }

  // 监听消息变化，自动滚动到底部
  $effect(() => {
    if (messages.length > 0) {
      setTimeout(() => {
        scrollToBottom();
      }, 100);
    }
  });
</script>

<div class="flex flex-col h-full">
  <!-- Chat Messages -->
  <ScrollArea
    class="p-4"
    style="height: {windowHeight - 210}px; overflow: hidden;"
    bind:ref={scrollAreaRef}
  >
    <ChatMessages
      messages={messages}
      status={status}
      error={error}
      onCopyMessage={handleCopyMessage}
      onRegenerateMessage={handleRegenerateMessage}
      onLikeMessage={handleLikeMessage}
      onDislikeMessage={handleDislikeMessage}
    />
  </ScrollArea>

  <!-- 输入区域 -->
  <div class="p-5">
    <InputArea
      placeholder="输入消息..."
      bind:inputValue={input}
      onSubmit={handleSubmit}
    />
  </div>
</div>