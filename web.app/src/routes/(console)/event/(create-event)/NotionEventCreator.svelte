<script lang="ts">
  import { _ } from 'svelte-i18n';
  import { Button } from "$lib/components/ui/button";
  import NotionSidePanel from "$lib/components/NotionSidePanel.svelte";
  import { Input } from "$lib/components/ui/input";
  import { browser } from '$app/environment';
  import ShadEditor from '$lib/components/shad-editor/shad-editor.svelte';
  import { cn } from "$lib/utils.js";
  import { writable } from 'svelte/store';
  import { Loader2, Image, Calendar, MapPin, Tag, Share2,Save } from "lucide-svelte";
  
  export let isOpen = false;
  export let onClose = () => {};
  
  // Event data
  let title = "";
  let description = "";
  let loading = false;
  let coverImage: File | null = null;
  let imagePreview: string | null = null;
  let location = "";
  let date = "";
  let tags: string[] = [];
  
  // Editor content store
  let content = writable('');
  
  content.subscribe((value) => {
    if (!browser) return;
    description = value;
    localStorage.setItem('event_description', value);
  });
  
  // Load saved content from localStorage
  if (browser) {
    const savedContent = localStorage.getItem('event_description');
    if (savedContent) {
      content.set(savedContent);
      description = savedContent;
    }
  }
  
  // Handle image upload
  function handleImageUpload(event: Event) {
    const target = event.target as HTMLInputElement;
    if (!target.files || target.files.length === 0) return;
    
    const file = target.files[0];
    coverImage = file;
    
    const reader = new FileReader();
    reader.onload = (e) => {
      if (e.target?.result) {
        imagePreview = e.target.result as string;
      }
    };
    reader.readAsDataURL(file);
  }
  
  // Submit the form
  async function submitEvent() {
    loading = true;
    
    try {
      // Here you would implement the actual event submission logic
      // For example, uploading the image, then submitting the form data
      console.log("Submitting event:", { title, description, location, date, tags, coverImage });
      
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Clear form after successful submission
      title = "";
      content.set("");
      location = "";
      date = "";
      tags = [];
      coverImage = null;
      imagePreview = null;
      
      // Close panel
      onClose();
    } catch (error) {
      console.error("Error submitting event:", error);
    } finally {
      loading = false;
    }
  }
</script>

<NotionSidePanel isOpen={isOpen} title={$_('events.create.title')} {onClose}>
  <div class="space-y-8">
    <!-- Cover image section -->
     <div class="px-6 space-y-8">
    {#if imagePreview}
      <div class="relative group">
        <img src={imagePreview} alt="Cover" class="w-full h-48 object-cover rounded-lg" />
        <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center rounded-lg">
          <Button variant="outline" size="sm" class="text-white border-white hover:bg-white/20">
            更换封面
          </Button>
        </div>
      </div>
    {:else}
      <div class="border-2 border-dashed border-muted-foreground/20 rounded-lg p-8 text-center hover:bg-muted/50 transition-colors cursor-pointer" 
      onclick={() => document.getElementById('cover-upload')?.click()}>
        <Image class="w-8 h-8 mx-auto mb-2 text-muted-foreground" />
        <p class="text-sm text-muted-foreground mb-2">{$_('events.create.add_cover')}</p>
        <p class="text-xs text-muted-foreground/70">{$_('events.create.drag_or_click')}</p>
        <input 
          type="file" 
          id="cover-upload" 
          accept="image/*" 
          class="hidden" 
          onchange={handleImageUpload}
        />
      </div>
    {/if}
    
    <!-- Title input - Notion style -->
    <div class="relative group">
      <input 
        type="text" 
        bind:value={title} 
        placeholder={$_('events.create.title_placeholder') || "Untitled event"} 
        class={cn(
          "w-full px-0 text-3xl font-bold border-0 focus:outline-none focus:ring-0 bg-transparent transition-colors",
          !title ? "text-muted-foreground/60" : "text-foreground"
        )}
      />
    </div>
    
    <!-- Event metadata -->
    <div class="space-y-4">
      <div class="flex items-center gap-2 text-muted-foreground hover:text-foreground cursor-pointer transition-colors p-1 -ml-1">
        <Calendar class="h-4 w-4" />
        <input 
          type="date" 
          bind:value={date} 
          class="bg-transparent border-0 focus:outline-none focus:ring-0 text-sm p-0" 
          placeholder="Add date"
        />
      </div>
      
      <div class="flex items-center gap-2 text-muted-foreground hover:text-foreground cursor-pointer transition-colors p-1 -ml-1">
        <MapPin class="h-4 w-4" />
        <input 
          type="text" 
          bind:value={location} 
          class="bg-transparent border-0 focus:outline-none focus:ring-0 text-sm p-0" 
          placeholder={$_('events.create.location_placeholder')}
        />
      </div>
      
      <div class="flex items-center gap-2 text-muted-foreground hover:text-foreground cursor-pointer transition-colors p-1 -ml-1">
        <Tag class="h-4 w-4" />
        <input 
          type="text" 
          class="bg-transparent border-0 focus:outline-none focus:ring-0 text-sm p-0" 
          placeholder={$_('events.create.add_tags')}
          onkeydown={(e) => {
            if (e.key === 'Enter' && (e.target as HTMLInputElement).value) {
              tags = [...tags, (e.target as HTMLInputElement).value];
              (e.target as HTMLInputElement).value = '';
            }
          }}
        />
      </div>
      
      {#if tags.length > 0}
        <div class="flex flex-wrap gap-2 mt-2">
          {#each tags as tag}
            <div class="bg-muted px-2 py-1 rounded-full text-xs flex items-center gap-1">
              {tag}
              <button class="text-muted-foreground hover:text-foreground" onclick={() => tags = tags.filter(t => t !== tag)}>
                &times;
              </button>
            </div>
          {/each}
        </div>
      {/if}
    </div>
  </div>
    <!-- Description editor - Notion style -->
    <div class="notion-editor relative group">
      <ShadEditor 
        showToolbar={false}
        class="min-h-[300px] border-0 focus:outline-none" 
        content={$content}
      />
    </div>
  </div>
  
  <svelte:fragment slot="footer">
    <div class="flex items-center justify-end gap-2">
      <Button 
      variant="ghost" size="icon" 
        onclick={submitEvent} 
        disabled={loading || !title} 
        class={!title ? "opacity-50 cursor-not-allowed" : ""}
      >
        {#if loading}
          <Loader2 class="h-4 w-4 animate-spin" />
        {:else}
          <Save class="h-4 w-4" />
        {/if}
      </Button>
    </div>
  </svelte:fragment>
</NotionSidePanel>
