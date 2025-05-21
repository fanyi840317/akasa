<script lang="ts">
  // import { Card, CardContent } from "$lib/components/ui/card";
  import { cn } from "$lib/utils";
  import type { Category } from "$lib/types/category";
  import type { Location } from "$lib/types/map";
  import CategoryCard from "./property-cards/category-card.svelte";
  import DateCard from "./property-cards/date-card.svelte";
  import LocationCard from "./property-cards/location-card.svelte";
  let {
    eventDate = $bindable(undefined),
    locationData = $bindable(null),
    selectedCategories = $bindable([]),
    categories = [],
    isLocation = $bindable(false),
    class: className = "",
    style = "", // For dynamic positioning by parent
  } = $props<{
    eventDate?: string;
    locationData?: Location | null;
    selectedCategories: string[];
    categories: Category[];
    isLocation?: boolean;
    className?: string;
    class?: string; // New class prop
    style?: string; // For dynamic positioning by parent
  }>();

  let dragOffsetX: number;
  let dragOffsetY: number;

  function handleDragStart(event: DragEvent) {
    if (event.dataTransfer && event.target instanceof HTMLElement) {
      event.dataTransfer.effectAllowed = "move";
      // Calculate offset from the top-left corner of the dragged element
      const rect = event.target.getBoundingClientRect();
      dragOffsetX = event.clientX - rect.left;
      dragOffsetY = event.clientY - rect.top;
      // Set the drag offset data for the parent component to use
      event.dataTransfer.setData(
        "application/json",
        JSON.stringify({ dragOffsetX, dragOffsetY }),
      );
    }
  }

  // The parent component will handle ondragover and ondrop to update the position
</script>

<div
  class={cn(
    "w-70 flex-shrink-0 cursor-grab", // Removed absolute positioning, added cursor
    className,
  )}
  {style}
>
  <div class="relative group">
    <LocationCard class="w-full h-full z-30 " {locationData} {isLocation} ></LocationCard>
    <DateCard
      class="absolute -bottom-3 left-0 w-full z-20 transition-all duration-300 ease-out transform scale-[0.98] group-hover:scale-100 group-hover:translate-y-[6rem] transition-transform"
      {eventDate}
    ></DateCard>
    <CategoryCard
      class="absolute -bottom-6 left-0 w-full z-10 transition-all duration-300 ease-out transform scale-[0.96] group-hover:scale-100 group-hover:translate-y-[11rem] transition-transform"
      {categories}
      {selectedCategories}
    ></CategoryCard>
    <!-- <CoverCard class="absolute -bottom-9 left-0 w-full z-0 transition-all duration-300 ease-out transform scale-[0.94] group-hover:scale-100 group-hover:translate-y-[24rem] transition-transform" ></CoverCard> -->
  </div>
</div>
