<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { cn } from '$lib/utils';
  import createGlobe from 'cobe';
  import { Motion } from 'svelte-motion';
  import { tweened } from 'svelte/motion';
  import { cubicOut } from 'svelte/easing';
  import Avatar from '../avatar/avatar.svelte';
  import { AvatarFallback, AvatarImage } from '../avatar';
  import { eventStore } from '$lib/stores/event'; // Assuming eventStore is needed and accessible

  let className = '';
  export { className as class };

  let canvasRef: HTMLCanvasElement;
  let globeInstance: ReturnType<typeof createGlobe> | null = null;
  let phi = 0;
  let width = 0;
  let height = 0;
  let animationFrame: number;

  // Added from GlobeLeftContent
  let contributors: { id: string; avatarUrl: string }[] = [];
  const tweenedOptions = { duration: 1000, easing: cubicOut };
  const animatedTotalEvents = tweened(0, tweenedOptions);
  const animatedTotalContributors = tweened(0, tweenedOptions);

  onMount(async () => { // Added async
   

    // Original Globe onMount logic continues here
    if (!canvasRef) return;

    const pixelRatio = window.devicePixelRatio || 1;
    width = canvasRef.offsetWidth;
    height = canvasRef.offsetHeight;
    
    globeInstance = createGlobe(canvasRef, {
      devicePixelRatio: pixelRatio,
      width: width * pixelRatio,
      height: height * pixelRatio,
      phi: 0,
      theta: 0.3,
      dark: 1,
      diffuse: 1.2,
      mapSamples: 16000,
      mapBrightness: 6,
      baseColor: [0.3, 0.3, 0.3],
      markerColor: [0.1, 0.8, 1],
      glowColor: [0.1, 0.6, 1.0],
      markers: [
        // Add some markers for major cities
        { location: [37.7595, -122.4367], size: 0.05 }, // San Francisco
        { location: [40.7128, -74.006], size: 0.05 },   // New York
        { location: [51.5074, -0.1278], size: 0.05 },   // London
        { location: [35.6762, 139.6503], size: 0.05 },  // Tokyo
        { location: [39.9042, 116.4074], size: 0.05 },  // Beijing
      ],
      onRender: (state) => {
        // Slowly rotate the globe
        state.phi = phi;
        phi += 0.003;
      },
    });

    return () => {
      if (globeInstance) {
        globeInstance.destroy();
      }
      cancelAnimationFrame(animationFrame);
    };
  });

  onDestroy(() => {
    if (globeInstance) {
      globeInstance.destroy();
    }
    cancelAnimationFrame(animationFrame);
  });
</script>

<canvas 
  bind:this={canvasRef} 
  class={cn("w-full h-full", className)}
/>

