<script lang="ts">
  import { Plus, FileText, Send } from "lucide-svelte";
  import { goto } from "$app/navigation";
  import { InputArea } from "../ai";
  import { UserAvatar } from "../ui";
  import TextCarousel from "../ui/carousel/text-carousel.svelte";

  let {
    title = "暂无事件",
    description = "",
    buttonText = "创建第一个事件",
    onButtonClick,
    aiPlaceholder = "或者告诉AI你想创建什么样的事件...",
  } = $props();

  let aiInput = $state("");

  function handleAiSubmit() {
    if (!aiInput.trim()) return;
    // 这里可以处理AI输入，例如调用API或导航到创建页面
    console.log("AI输入:", aiInput);
    // 示例：可以带着AI输入导航到创建页面
    goto(`/console/events/new?aiPrompt=${encodeURIComponent(aiInput)}`);
  }
</script>

<div class="flex flex-col gap-6 justify-between rounded-xl 
border border-border border-dashed p-6 w-full">
  <!-- 图标区域 -->
  <div class="flex items-start justify-between">
    <span class="text-xs text-gray-500">Aug 13, 2024</span>
    <UserAvatar ></UserAvatar>
  </div>
  <div class="flex flex-col ">
    <TextCarousel
        texts={[
          "प्रत्यभिज्ञानं आरम्भः", 
          "In tenebris, veritas quaeritur.", 
          "חֲקִירָה לַאֲוִירָה (Ḥaqirah la'avirah)", 
          "𒄑𒉈𒇻𒂵𒄑 (niĝ2-si-ga ki-ma e2-gal)"
        ]}
        ghost={true}
        
        class="h-18"
      />
    <span
      class=" text-base-content/50  line-clamp-2 overflow-ellipsis mt-3 sm:mt-4 leading-7 min-h-[3.5rem]"
      >{description}</span
    >
    <div class="flex-center w-full">  <button
        class="btn btn-sm btn-primary btn-outline mt-2 w-1/3"   
        onclick={onButtonClick}
      >
        {buttonText}
      </button></div>
  
  </div>

</div>
