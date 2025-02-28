<script lang="ts">
  import { onMount, mount } from 'svelte';
  import mapboxgl from 'mapbox-gl';
  import 'mapbox-gl/dist/mapbox-gl.css';
  import MapMarker from './MapMarker.svelte';
  import { mode } from 'mode-watcher';
  import { get } from 'svelte/store';
  import { goto } from '$app/navigation';

  export let longitude = 104.06;
  export let latitude = 30.67;
  export let showUserLocation = true;

  let container: HTMLDivElement;
  let map: mapboxgl.Map;

  mapboxgl.accessToken = 'pk.eyJ1IjoiZmFueWk4NDAzMTciLCJhIjoiY202cDE4OW9wMHZxMzJscTBtbW82NDNxdCJ9.90mwfIpA62nmCY0_C7IkUw';

  onMount(() => {
    map = new mapboxgl.Map({
      container,
      style: get(mode) === 'light' ? 'mapbox://styles/mapbox/light-v10' : 'mapbox://styles/mapbox/dark-v11',
      zoom: 8,
      center: [longitude, latitude],
      pitch: 0,
      antialias: true
    });

    if (showUserLocation) {
      const userMarkerElement = document.createElement('div');
      userMarkerElement.className = 'user-location-marker';
      new mapboxgl.Marker({
        element: userMarkerElement,
        anchor: 'center'
      })
        .setLngLat([longitude, latitude])
        .addTo(map);
    }


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

    // markers.forEach(markerData => {
    //   const markerElement = document.createElement('div');
    //   const marker = new mapboxgl.Marker({
    //     element: markerElement,
    //     anchor: 'bottom',
    //     offset: [0, -15],
    //     clickTolerance: 3
    //   })
    //     .setLngLat(markerData.coordinates)
    //     .addTo(map);

    //   mount(MapMarker, {
    //     target: markerElement,
    //     props: {
    //       marker: markerData,
    //       onMarkerClick: (marker) => {
    //         console.log('Marker click event received:', marker);
    //         if (marker && marker.id) {
    //           goto(`/events/${marker.id}`);
    //         } else {
    //           console.error('Invalid marker data:', marker);
    //         }
    //       }
    //     }
    //   });
    // });

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

  :global(.user-location-marker) {
    width: 15px;
    height: 15px;
    background-color: rgb(37, 99, 235);
    border: 3px solid rgba(255, 255, 255, 0.8);
    border-radius: 50%;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.3);
    cursor: pointer;
    position: relative;
  }
  :global(.user-location-marker::after) {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 100%;
    height: 100%;
    background-color: rgba(37, 99, 235, 0.6);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    animation: pulse-scale 2s infinite;
  }
  @keyframes pulse-scale {
    0% {
      transform: translate(-50%, -50%) scale(1);
      opacity: 1;
    }
    70% {
      transform: translate(-50%, -50%) scale(18);
      opacity: 0;
    }
    100% {
      transform: translate(-50%, -50%) scale(1);
      opacity: 0;
    }
  }
  @keyframes pulse {
    0% {
      box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.6);
    }
    70% {
      box-shadow: 0 0 0 100px rgba(37, 99, 235, 0);
    }
    100% {
      box-shadow: 0 0 0 0 rgba(37, 99, 235, 0);
    }
  }
</style>