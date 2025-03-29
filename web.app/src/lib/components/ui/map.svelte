<script lang="ts">
    import { onMount } from 'svelte';

    declare global {
        interface Window {
            AMap: any;
        }
    }

    export let center: { lat: number; lng: number };
    export let zoom: number = 15;
    export let markers: Array<{ position: { lat: number; lng: number }; title: string }> = [];

    let mapElement: HTMLElement;
    let map: any;
    let marker: any;

    onMount(() => {
        // 确保 AMap 已加载
        if (window.AMap) {
            initMap();
        } else {
            const script = document.createElement('script');
            script.src = `https://webapi.amap.com/maps?v=2.0&key=YOUR_AMAP_KEY`;
            script.onload = initMap;
            document.head.appendChild(script);
        }
    });

    function initMap() {
        map = new window.AMap.Map(mapElement, {
            zoom,
            center: [center.lng, center.lat],
            resizeEnable: true
        });

        markers.forEach(marker => {
            new window.AMap.Marker({
                position: [marker.position.lng, marker.position.lat],
                title: marker.title,
                map: map
            });
        });
    }
</script>

<div bind:this={mapElement} class={$$props.class} />

<style>
    div {
        width: 100%;
        height: 100%;
    }
</style> 