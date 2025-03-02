<script lang="ts">
    import { _ } from 'svelte-i18n';
    import { Input } from "$lib/components/ui/input";
    import { Label } from "$lib/components/ui/label";
    import Map from "$lib/components/Map.svelte";
    import { MapPin } from "lucide-svelte";

    export let location = "";
    let mapLocation: [number, number] | null = null;

    function handleLocationSelect(event: CustomEvent<[number, number]>) {
        mapLocation = event.detail;
        // 这里可以通过反向地理编码获取地址，暂时使用坐标作为位置信息
        location = `${mapLocation[0].toFixed(6)}, ${mapLocation[1].toFixed(6)}`;
    }
</script>

<div class="space-y-4">
    <div class="space-y-2">
        <Label for="location">{$_('events.create.location')}</Label>
        <div class="relative">
            <MapPin class="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
                id="location"
                bind:value={location}
                placeholder={$_('events.create.location_placeholder')}
                class="pl-8"
                required
            />
        </div>
    </div>

    <div class="h-[300px] w-full rounded-md border">
        <Map on:locationSelect={handleLocationSelect} />
    </div>
</div>