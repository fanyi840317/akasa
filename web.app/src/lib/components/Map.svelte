<script lang="ts">
  import { onMount, mount } from 'svelte';
  import mapboxgl from 'mapbox-gl';
  import 'mapbox-gl/dist/mapbox-gl.css';
  import MapMarker from './MapMarker.svelte';
  import { markers } from '$lib/markers';
  import { mode } from 'mode-watcher'; // 引入主题存储
  import { get } from 'svelte/store';
  import { goto } from '$app/navigation';

  let container: HTMLDivElement;
  let map: mapboxgl.Map;

  mapboxgl.accessToken = 'pk.eyJ1IjoiZmFueWk4NDAzMTciLCJhIjoiY202cDE4OW9wMHZxMzJscTBtbW82NDNxdCJ9.90mwfIpA62nmCY0_C7IkUw';

  onMount(() => {
    const currentTheme = get(mode); // 获取当前主题

    map = new mapboxgl.Map({
      container,
      style: currentTheme === 'light' ? 'mapbox://styles/mapbox/light-v10' : 'mapbox://styles/mapbox/dark-v11',
  
      zoom: 8,
      center: [104.06, 30.67],
      pitch: 0,
      antialias: true
    });

    // 添加3D和2D切换图标
    // const toggle3D2DControl = new mapboxgl.NavigationControl({
    //   visualizePitch: true
    // });
    // map.addControl(toggle3D2DControl, 'top-right');

    // map.on('style.load', () => {
    //   map.setFog({
    //     color: 'rgb(186, 210, 235)',
    //     'high-color': 'rgb(36, 92, 223)',
    //     'horizon-blend': 0.02,
    //     'space-color': 'rgb(11, 11, 25)',
    //     'star-intensity': 0.6
    //   });
    // });

    // map.addControl(new mapboxgl.NavigationControl());

    markers.forEach(markerData => {
      const markerElement = document.createElement('div');
      const marker = new mapboxgl.Marker({
        element: markerElement,
        anchor: 'bottom',
        offset: [0, -15],
        clickTolerance: 3
      })
        .setLngLat(markerData.coordinates)
        .addTo(map);

      mount(MapMarker, {
        target: markerElement,
        props: {
          marker: markerData,
          onMarkerClick: (marker) => {
            console.log('Marker click event received:', marker);
            if (marker && marker.id) {
              goto(`/events/${marker.id}`);
            } else {
              console.error('Invalid marker data:', marker);
            }
          }
        }
      });
    });

    // 监听模式变化
    const unsubscribe = mode.subscribe(currentMode => {
      map.setStyle(currentMode === 'light' ? 'mapbox://styles/mapbox/light-v10' : 'mapbox://styles/mapbox/dark-v11');
    });

    return () => {
      map.remove();
      unsubscribe();
    };
  });
</script>

<div bind:this={container} class="mapContainer">
</div>

<style>
  .mapContainer {
    width: 100%;
    height: 100%;
    position: relative;
  }

  :global(.mapboxgl-ctrl-bottom-right) {
    display: none;
  }
</style> 