<script lang="ts">
  export let src: string | null = null;
  export let fallback: string;
  export let userName: string;
  export let time: string;
  export let message: string;
  export let footerText: string = '';
</script>

<div class="chat-message flex justify-end">
  <div class="flex items-start gap-2.5">
    <div class="flex flex-col gap-1 max-w-xs md:max-w-md lg:max-w-lg xl:max-w-2xl">
      <div class="flex items-center space-x-2 rtl:space-x-reverse">
        <span class="text-sm font-semibold text-gray-200">{userName}</span>
        <span class="text-sm font-normal text-gray-400">{time}</span>
      </div>
      <div class="flex flex-col leading-1.5 p-4 border-gray-200 bg-blue-600 rounded-e-xl rounded-es-xl">
        <p class="text-sm font-normal text-white whitespace-pre-wrap break-words">
          {message}
        </p>
      </div>
      {#if footerText}
        <span class="text-xs font-normal text-gray-400">{footerText}</span>
      {/if}
    </div>
    <div class="relative w-8 h-8 overflow-hidden bg-gray-700 rounded-full">
      {#if src}
        <img src={src} alt={userName} class="w-full h-full object-cover" />
      {:else}
        <div class="absolute inset-0 flex items-center justify-center text-gray-200 font-semibold">
          {fallback}
        </div>
      {/if}
    </div>
  </div>
</div>
