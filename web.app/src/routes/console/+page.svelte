<script lang="ts">
    import type { PageData } from './$types';

    let { data }: { data: PageData } = $props();
    import {Shell} from "$lib/components/console";
    import * as Sidebar from "$lib/components/ui/sidebar";
    import NavSidebar from "$lib/components/console/navigation/sidebar.svelte";
    import { Button } from '$lib/components/ui/button';
    import { PlusCircle } from 'lucide-svelte';
</script>


{#snippet actions()}
<Button 
        variant="secondary" 
        size="sm" 
        class="map-control-button"
    >
        <PlusCircle class="h-4 w-4 mr-2" />

    </Button>
{/snippet}
{#snippet children()}
    <div></div>
{/snippet}

