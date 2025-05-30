<script lang="ts">
  import { Send, Plus, Search, Lightbulb, Brain, Image as ImageIcon, Mic, Settings2, MoreHorizontal, Camera, HelpCircle, Trash2 } from 'lucide-svelte';
  import { sineOut } from 'svelte/easing';
  import { fly } from 'svelte/transition';
  import { UserChat, InputArea } from '$lib/components/ai';

  type Message = {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
  };

  let messages = $state<Message[]>([]);
  let inputText = $state('');
  let isLoading = $state(false);
  let chatStarted = $derived(messages.length > 0);
  let showMoreOptions = $state(false);
  let moreOptionsMenuRef = $state<HTMLElement | undefined>();
  let moreOptionsButtonRef = $state<HTMLElement | undefined>();

  function generateId() {
    return Math.random().toString(36).substring(2, 15);
  }

  async function handleSubmit({ detail }: CustomEvent<{ text: string }>) {
    const text = detail.text;
    if (!text) return;

    const newMessage: Message = {
      id: generateId(),
      role: 'user',
      content: text,
      timestamp: new Date(),
    };
    messages = [...messages, newMessage];
    inputText = '';
    isLoading = true;

    // Simulate AI response
    await new Promise(resolve => setTimeout(resolve, 1500));

    const aiResponse: Message = {
      id: generateId(),
      role: 'assistant',
      content: `这是对 "${text}" 的模拟回复。`, // More sophisticated response logic will be needed
      timestamp: new Date(),
    };
    messages = [...messages, aiResponse];
    isLoading = false;

    // Scroll to bottom
    // This needs to be improved to wait for DOM update
    requestAnimationFrame(() => {
      const chatContainer = document.querySelector('.chat-messages-container');
      if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
      }
    });
  }

  const suggestedPrompts = [
    "解释量子计算的基本原理。",
    "为我的新咖啡店写一句标语。",
    "如果恐龙从未灭绝会怎样？",
    "给我推荐一部科幻电影。"
  ];
  function useSuggestedPrompt(prompt: string) {
    inputText = prompt;
    handleSubmit({ detail: { text: prompt } } as CustomEvent<{ text: string }>);
  }

  let inputWrapperRef: HTMLElement | undefined = $state();
  let inputHeight = $state(0);

  $effect(() => {
    if (inputWrapperRef) {
      const resizeObserver = new ResizeObserver(entries => {
        for (let entry of entries) {
          inputHeight = entry.contentRect.height;
        }
      });
      resizeObserver.observe(inputWrapperRef);
      return () => resizeObserver.disconnect();
    }
  });

  function clearConversation() {
    messages = [];
    showMoreOptions = false;
    // Optionally, reset other states if needed, e.g., inputText
  }

  $effect(() => {
    if (showMoreOptions) {
      const handleClickOutside = (event: MouseEvent) => {
        if (
          moreOptionsMenuRef && 
          !moreOptionsMenuRef.contains(event.target as Node) &&
          moreOptionsButtonRef && 
          !moreOptionsButtonRef.contains(event.target as Node)
        ) {
          showMoreOptions = false;
        }
      };
      window.addEventListener('click', handleClickOutside, true);
      return () => window.removeEventListener('click', handleClickOutside, true);
    }
  });

</script>

<div class="flex flex-col h-full text-white relative overflow-hidden">
  <!-- Messages Area -->
  <div 
    class="flex-grow overflow-y-auto chat-messages-container p-4 md:p-6 space-y-4"
    style:padding-bottom={`${chatStarted ? inputHeight + 16 : 20}px`}
  >
    {#if !chatStarted}
      <div class="flex flex-col items-center justify-center h-full text-center" in:fly={{ y: 20, duration: 300, easing: sineOut }}>
        <div class="mb-8">
          <svg width="41" height="41" viewBox="0 0 41 41" fill="none" xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto mb-4">
            <path d="M33.3645 20.001C33.3645 22.019 32.6245 23.979 31.3245 25.599C30.0245 27.219 28.2445 28.419 26.2345 28.999L26.2045 29.009C26.1845 29.009 26.1745 29.009 26.1545 29.009C25.0145 29.309 23.8145 29.469 22.5845 29.469C22.4545 29.469 22.3245 29.469 22.1945 29.459L22.1845 29.459C22.1845 29.459 22.1845 29.459 22.1745 29.459C20.4145 29.369 18.7345 28.909 17.2745 28.129C15.8145 27.349 14.6145 26.279 13.7745 24.999L13.7645 24.979C13.7645 24.979 13.7645 24.969 13.7545 24.959C13.0845 23.919 12.6745 22.749 12.5745 21.529L12.5735 21.519C12.5735 21.519 12.5735 21.509 12.5735 21.499C12.5335 21.019 12.5145 20.519 12.5145 20.009C12.5145 17.989 13.2545 16.029 14.5545 14.409C15.8545 12.789 17.6345 11.589 19.6445 11.009L19.6745 10.999C19.6945 10.999 19.7045 10.999 19.7245 10.999C20.8645 10.689 22.0645 10.529 23.2945 10.529C23.4245 10.529 23.5545 10.529 23.6845 10.539L23.6945 10.539C23.6945 10.539 23.6945 10.539 23.7045 10.539C25.4645 10.629 27.1445 11.089 28.6045 11.869C30.0645 12.649 31.2645 13.719 32.1045 14.999L32.1145 15.019C32.1145 15.019 32.1145 15.029 32.1245 15.039C32.7945 16.079 33.2045 17.249 33.3045 18.469L33.3055 18.479C33.3055 18.479 33.3055 18.489 33.3055 18.499C33.3455 18.979 33.3645 19.479 33.3645 19.999L33.3645 20.001Z" fill="#C1C1C1" fill-opacity="0.2"></path><path d="M20.5001 0.000976562C22.5181 0.000976562 24.4781 0.740977 26.0981 2.04098C27.7181 3.34098 28.9181 5.12098 29.4981 7.13098L29.5081 7.16098C29.5081 7.18098 29.5081 7.19098 29.5081 7.21098C29.8081 8.35098 29.9681 9.55098 29.9681 10.781C29.9681 10.911 29.9681 11.041 29.9581 11.171L29.9581 11.181C29.9581 11.181 29.9581 11.181 29.9581 11.191C29.8681 12.951 29.4081 14.631 28.6281 16.091C27.8481 17.551 26.7781 18.751 25.4981 19.591L25.4781 19.601C25.4781 19.601 25.4681 19.601 25.4581 19.611C24.4181 20.281 23.2481 20.691 22.0281 20.791L22.0181 20.791C22.0181 20.791 22.0081 20.791 21.9981 20.791C21.5181 20.831 21.0181 20.851 20.5081 20.851C18.4881 20.851 16.5281 20.111 14.9081 18.811C13.2881 17.511 12.0881 15.731 11.5081 13.721L11.4981 13.691C11.4981 13.671 11.4981 13.661 11.4981 13.641C11.1881 12.501 11.0281 11.301 11.0281 10.071C11.0281 9.94098 11.0281 9.81098 11.0381 9.68098L11.0381 9.67098C11.0381 9.67098 11.0381 9.67098 11.0381 9.66098C11.1281 7.90098 11.5881 6.22098 12.3681 4.76098C13.1481 3.30098 14.2181 2.10098 15.4981 1.26098L15.5181 1.25098C15.5181 1.25098 15.5281 1.25098 15.5381 1.24098C16.5781 0.570977 17.7481 0.160977 18.9681 0.0609766L18.9781 0.0609766C18.9781 0.0609766 18.9881 0.0609766 18.9981 0.0609766C19.4781 0.0209766 19.9781 0.000976562 20.4881 0.000976562L20.5001 0.000976562Z" fill="#C1C1C1" fill-opacity="0.2"></path><path d="M20.5001 40.999C18.4821 40.999 16.5221 40.259 14.9021 38.959C13.2821 37.659 12.0821 35.879 11.5021 33.869L11.4921 33.839C11.4921 33.819 11.4921 33.809 11.4921 33.789C11.1921 32.649 11.0321 31.449 11.0321 30.219C11.0321 30.089 11.0321 29.959 11.0421 29.829L11.0421 29.819C11.0421 29.819 11.0421 29.819 11.0421 29.809C11.1321 28.049 11.5921 26.369 12.3721 24.909C13.1521 23.449 14.2221 22.249 15.5021 21.409L15.5221 21.399C15.5221 21.399 15.5321 21.399 15.5421 21.389C16.5821 20.719 17.7521 20.309 18.9721 20.209L18.9821 20.209C18.9821 20.209 18.9921 20.209 19.0021 20.209C19.4821 20.169 19.9821 20.149 20.4921 20.149C22.5121 20.149 24.4721 20.889 26.0921 22.189C27.7121 23.489 28.9121 25.269 29.4921 27.279L29.5021 27.309C29.5021 27.329 29.5021 27.339 29.5021 27.359C29.8021 28.499 29.9621 29.699 29.9621 30.929C29.9621 31.059 29.9621 31.189 29.9521 31.319L29.9521 31.329C29.9521 31.329 29.9521 31.329 29.9521 31.339C29.8621 33.099 29.4021 34.779 28.6221 36.239C27.8421 37.699 26.7721 38.899 25.4921 39.739L25.4721 39.749C25.4721 39.749 25.4621 39.749 25.4521 39.759C24.4121 40.429 23.2421 40.839 22.0221 40.939L22.0121 40.939C22.0121 40.939 22.0021 40.939 21.9921 40.939C21.5121 40.979 21.0121 40.999 20.5021 40.999L20.5001 40.999Z" fill="#C1C1C1" fill-opacity="0.2"></path>
          </svg>
          <h1 class="text-2xl font-semibold text-base-content/50">我能为您做些什么？</h1>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-2xl">
          {#each suggestedPrompts as prompt}
            <button 
              onclick={() => useSuggestedPrompt(prompt)}
              class="bg-base-200 hover:bg-base-300 text-gray-300 text-sm p-3 rounded-lg text-left transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {prompt}
            </button>
          {/each}
        </div>
      </div>
    {/if}

    {#each messages as message (message.id)}
      {#if message.role === 'user'}
        <UserChat 
          src={null} 
          fallback="U" 
          userName="User" 
          time={new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} 
          message={message.content} 
          footerText="Sent"
        />
      {:else}
        <div 
          class="chat-message flex justify-start"
          in:fly={{ y: 10, duration: 200, easing: sineOut }}
        >
          <div class="max-w-xs md:max-w-md lg:max-w-lg xl:max-w-2xl px-4 py-2 rounded-lg shadow bg-gray-700 text-gray-200">
            <p class="whitespace-pre-wrap break-words">{message.content}</p>
            <p class="text-xs mt-1 text-gray-400 text-right">
              {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </p>
          </div>
        </div>
      {/if}
    {/each}

    {#if isLoading}
      <div class="chat-message flex justify-start" in:fly={{ y: 10, duration: 200, easing: sineOut }}>
        <div class="max-w-xs md:max-w-md lg:max-w-lg xl:max-w-2xl px-4 py-3 rounded-lg shadow bg-gray-700 text-gray-200 flex items-center">
          <div class="animate-pulse flex space-x-1">
            <div class="w-2 h-2 bg-gray-400 rounded-full"></div>
            <div class="w-2 h-2 bg-gray-400 rounded-full"></div>
            <div class="w-2 h-2 bg-gray-400 rounded-full"></div>
          </div>
        </div>
      </div>
    {/if}
  </div>

  <!-- Input Area -->
  <div 
    bind:this={inputWrapperRef}
    class="absolute bottom-0 left-0 right-0 transition-all duration-300 ease-in-out
    {chatStarted ? 'p-2 md:p-4' : 'p-4 md:p-8'} items-center justify-center"
    class:translate-y-0={chatStarted}
    class:translate-y-[calc(50vh-50%)]={!chatStarted && inputWrapperRef} 
  >
    <div class="max-w-3xl mx-auto">
      {#if !chatStarted}
        <!-- Placeholder for potential initial buttons when input is centered -->
      {/if}
      <InputArea 
          bind:value={inputText}
          {isLoading}
          on:submit={handleSubmit}
        />
    </div>
  </div>
</div>

<style>
  /* For Webkit browsers */
  .chat-messages-container::-webkit-scrollbar {
    width: 6px;
  }
  .chat-messages-container::-webkit-scrollbar-track {
    background: transparent;
  }
  .chat-messages-container::-webkit-scrollbar-thumb {
    background-color: rgba(107, 114, 128, 0.5); /* gray-500 with 50% opacity */
    border-radius: 3px;
  }
  .chat-messages-container::-webkit-scrollbar-thumb:hover {
    background-color: rgba(107, 114, 128, 0.7);
  }

  textarea::-webkit-scrollbar {
    width: 4px;
  }
  textarea::-webkit-scrollbar-thumb {
    background-color: rgba(107, 114, 128, 0.5);
    border-radius: 2px;
  }

  /* Tooltip styles */
  .tooltip {
    position: relative;
  }

  .tooltip::before {
    content: attr(data-tip);
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    padding: 4px 8px;
    background-color: rgba(55, 65, 81, 0.9);
    color: white;
    font-size: 12px;
    border-radius: 4px;
    white-space: nowrap;
    opacity: 0;
    visibility: hidden;
    transition: all 0.2s ease;
  }

  .tooltip:hover::before {
    opacity: 1;
    visibility: visible;
    bottom: calc(100% + 5px);
  }

  /* Input area transitions */
  textarea {
    transition: background-color 0.2s ease, border-color 0.2s ease;
  }

  textarea:focus {
    background-color: rgba(55, 65, 81, 0.3);
    outline: none;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
  }

  /* Button hover effects */
  button {
    transition: all 0.2s ease;
  }

  button:active {
    transform: scale(0.95);
  }

  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>