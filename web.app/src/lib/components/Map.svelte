<script lang="ts">
  import { onMount, mount } from 'svelte';
  import mapboxgl from 'mapbox-gl';
  import 'mapbox-gl/dist/mapbox-gl.css';
  import MapMarker from './MapMarker.svelte';
  import { markers } from '$lib/markers';

  let container: HTMLDivElement;
  let map: mapboxgl.Map;

  mapboxgl.accessToken = 'pk.eyJ1IjoiZmFueWk4NDAzMTciLCJhIjoiY202cDE4OW9wMHZxMzJscTBtbW82NDNxdCJ9.90mwfIpA62nmCY0_C7IkUw';

  onMount(() => {
    map = new mapboxgl.Map({
      container,
      style: 'mapbox://styles/mapbox/satellite-v9',
      projection: 'globe',
      zoom: 8,
      center: [104.06, 30.67],
      pitch: 45,
      antialias: true
    });

    map.on('style.load', () => {
      map.setFog({
        color: 'rgb(186, 210, 235)',
        'high-color': 'rgb(36, 92, 223)',
        'horizon-blend': 0.02,
        'space-color': 'rgb(11, 11, 25)',
        'star-intensity': 0.6
      });
    });

    map.addControl(new mapboxgl.NavigationControl());

    markers.forEach(markerData => {
      const markerElement = document.createElement('div');
      const marker = new mapboxgl.Marker({
        element: markerElement,
        anchor: 'bottom',
        offset: [0, -15]
      })
        .setLngLat(markerData.coordinates)
        .addTo(map);

      mount(MapMarker, {
        target: markerElement,
        props: {
          marker: markerData
        }
      });
    });

    return () => {
      map.remove();
    };
  });
</script>

<div bind:this={container} class="mapContainer">
  <div id="coords" class="coordinates-info"></div>
</div>

<style>
  .mapContainer {
    width: 100%;
    height: 100%;
    position: relative;
  }

  .coordinates-info {
    position: absolute;
    top: 20px;
    left: 20px;
    background: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 10px;
    border-radius: 5px;
    font-size: 14px;
    z-index: 1000;
  }

  :global(.mapboxgl-ctrl-bottom-right) {
    display: none;
  }
</style> 