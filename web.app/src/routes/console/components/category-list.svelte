<script lang="ts">
    import { fade, fly } from "svelte/transition";

    export let categories: Array<{
        id: string;
        name: string;
        count: number;
    }>;
    export let selectedCategory: string;
    export let onCategoryClick: (categoryId: string) => void;
</script>

{#each categories as category, i}
    <a
        href="#"
        class="block px-4 py-2 mb-2 flex items-center justify-between gap-4 transition-transform hover:-translate-y-2 hover:shadow-lg {selectedCategory ===
        category.id
            ? 'bg-background/10'
            : 'hover:bg-background/20'}"
        on:click={() => onCategoryClick(category.id)}
        in:fly={{ y: 20, delay: i * 50, duration: 400 }}
    >
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
