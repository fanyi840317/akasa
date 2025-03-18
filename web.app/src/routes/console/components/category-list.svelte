<script lang="ts">
    import { fade, fly } from "svelte/transition";
    import { Badge } from "$lib/components/ui/badge";

    export let categories: Array<{
        id: string;
        name: string;
        count: number;
    }>;
    export let selectedCategory: string;
    export let onCategoryClick: (categoryId: string) => void;
</script>

<div class="rounded-lg bg-card/40 p-4  shadow-md">
    {#each categories as category, i}
    
        <a
            href="#"
            class="block px-2 py-2 mr-10 flex items-center rounded-lg gap-4 transition-all hover:-translate-y-1 hover:shadow-lg {selectedCategory ===
            category.id
                ? ''
                : 'hover:bg-background/20'}"
            on:click={() => onCategoryClick(category.id)}
            in:fly={{ y: 20, delay: i * 50, duration: 400 }}
        >  <span class="text-xs {selectedCategory === category.id ? 'bg-primary/10 text-primary' : 'text-muted-foreground'}">
            {category.count}
        </span>
            <h4
                class="font-medium whitespace-nowrap transition-all {selectedCategory ===
                category.id
                    ? 'text-primary text-4xl font-bold'
                    : 'text-muted-foreground text-xs hover:text-primary'}"
            >
                {category.name}
            </h4>
          
        </a>
    {/each}
</div>
