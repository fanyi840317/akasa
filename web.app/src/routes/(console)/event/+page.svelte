<script lang="ts">
    import type { PageData } from "./$types";
    import { onMount } from "svelte";
    import { get } from "svelte/store";
    import { writable } from "svelte/store";
    import { fade, fly, slide } from "svelte/transition";
    import { _ } from "svelte-i18n";
    import { goto } from "$app/navigation";
    import { base } from "$app/paths";
    import { auth } from "$lib/stores/auth";
    import { theme } from "$lib/stores/theme";
    import { databases } from "$lib/appwrite";
    import { ID } from "appwrite";
    import Map from "$lib/components/Map.svelte";
    import EventList from "$lib/components/EventList.svelte";
    import StepWindow from "$lib/components/StepWindow.svelte";
    import NotionEventCreator from "../../(console)/event/(create-event)/NotionEventCreator.svelte";
    import * as Card from "$lib/components/ui/card";
    import { Input } from "$lib/components/ui/input";
    import { Button } from "$lib/components/ui/button";
    import { Textarea } from "$lib/components/ui/textarea";
    import { Label } from "$lib/components/ui/label";
    import HeaderPage from "$lib/components/console/header-page.svelte";
    import {
        PlusCircle,
        Search,
        MapPin,
        Image,
        Loader2,
        ChevronRight,
        ChevronLeft,
    } from "lucide-svelte";

    import { Pane, Splitpanes } from "svelte-splitpanes";

    let { data }: { data: PageData } = $props();
    let loading = false;
    let title = "";
    let description = "";
    let location = "";
    let imageFile: File | null = null;
    let imagePreview: string | null = null;

    let currentStep = 0;
    let containerWidth = 0;
    let containerRef: HTMLElement;
    let isMobileView = $state(false);
    let searchQuery = "";
    let map: any;
    let splitRatio = $state(1);
    let showCreateEvent = $state(false);

    const totalSteps = 3;
    const searchResults = writable([]);

    const steps = [
        {
            title: $_("events.create.step1_title"),
            description: $_("events.create.step1_desc"),
        },
        {
            title: $_("events.create.step2_title"),
            description: $_("events.create.step2_desc"),
        },
        {
            title: $_("events.create.step3_title"),
            description: $_("events.create.step3_desc"),
        },
    ];

    const categories = [
        {
            name: $_("events.categories.urban"),
            icon: "/icons/urban.svg",
            type: "urban",
        },
        {
            name: $_("events.categories.paranormal"),
            icon: "/icons/paranormal.svg",
            type: "paranormal",
        },
        {
            name: $_("events.categories.supernatural"),
            icon: "/icons/supernatural.svg",
            type: "supernatural",
        },
        {
            name: $_("events.categories.mysterious"),
            icon: "/icons/mysterious.svg",
            type: "mysterious",
        },
        {
            name: $_("events.categories.unexplained"),
            icon: "/icons/unexplained.svg",
            type: "unexplained",
        },
        {
            name: $_("events.categories.phenomena"),
            icon: "/icons/phenomena.svg",
            type: "phenomena",
        },
    ];

    function handleShare() {
        if (!$auth.user) {
            goto(`${base}/login`);
            return;
        }
        showCreateEvent = !showCreateEvent;
    }

    function searchLocation() {
        updateMapLocation(searchQuery);
    }

    function handleKeyPress(event: KeyboardEvent) {
        if (event.key === "Enter") {
            searchLocation();
        }
    }

    async function updateMapLocation(location: string) {
        const response = await fetch(
            `https://api.example.com/geocode?address=${encodeURIComponent(location)}`,
        );
        const data = await response.json();
        if (data && data.results && data.results.length > 0) {
            const { lat, lng } = data.results[0].geometry.location;
            map.setCenter([lng, lat]);
        } else {
            console.error("未找到该位置");
        }
    }

    function updateContainerWidth() {
        if (containerRef) {
            containerWidth = containerRef.clientWidth;
            isMobileView = containerWidth < 600;
        }
    }

    onMount(() => {
        updateContainerWidth();

        const resizeObserver = new ResizeObserver(() => {
            updateContainerWidth();
        });

        if (containerRef) {
            resizeObserver.observe(containerRef);
        }

        return () => {
            if (containerRef) {
                resizeObserver.unobserve(containerRef);
            }
        };
    });
</script>

<Splitpanes theme="my-theme" class="h-[calc(100vh-4rem)] w-full">
    <Pane class="flex-1 w-full">
        <HeaderPage title="event" class="w-full h-full flex flex-col">
              <div class="relative flex-1 w-full h-full" bind:this={containerRef}>
                    <div class="absolute inset-0 w-full h-full">
                        <Map locationData={data.location} />
                    </div>
                    {#if !isMobileView}
                        <div
                            class="absolute top-4 left-4 z-20 w-64 space-y-4"
                            transition:fly={{ x: -200, duration: 300, opacity: 1 }}
                        >
                            <Card.Root
                                class="backdrop-blur-sm border-none shadow-lg"
                            >
                                <Card.Content class="p-4">
                                    <h1 class="text-xl font-bold">
                                        {$_("site.events")}
                                    </h1>
                                    <h2 class="text-sm text-muted-foreground mb-4">
                                        {$_("events.subtitle")}
                                    </h2>
                                    <Button
                                        variant="outline"
                                        class="w-full gap-2"
                                        onclick={handleShare}
                                    >
                                        <PlusCircle class="h-4 w-4" />
                                        <span>{$_("events.share")}</span>
                                    </Button>
                                </Card.Content>
                            </Card.Root>
                            <div
                                class="flex flex-wrap gap-2"
                                transition:slide={{ duration: 200 }}
                            >
                                {#each categories as category}
                                    <Card.Root
                                        class="p-2 flex items-center gap-2 cursor-pointer hover:bg-accent/50 transition-colors border-none shadow-sm backdrop-blur-sm"
                                    >
                                        <div
                                            class="w-6 h-6 bg-gradient-to-br from-cyan-400/20 to-purple-400/20 rounded-full p-1 group-hover:from-cyan-400/30 group-hover:to-purple-400/30 transition-all"
                                        >
                                            <img
                                                src="{base}{category.icon}"
                                                alt={category.name}
                                                class="w-full h-full text-cyan-400"
                                            />
                                        </div>
                                        <span class="text-xs text-primary"
                                            >{category.name}</span
                                        >
                                    </Card.Root>
                                {/each}
                            </div>
                        </div>
                    {/if}
                    <div
                        class="absolute top-4 right-4 z-20 space-y-4"
                        transition:slide={{ duration: 200 }}
                    >
                        <Card.Root
                            class="w-80 backdrop-blur-sm border-none shadow-lg"
                        >
                            <Card.Content class="p-4">
                                <div class="relative w-full flex gap-2">
                                    <div class="relative flex-1">
                                        <Search
                                            class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground"
                                        />
                                        <Input
                                            placeholder="Search Location"
                                            class="pl-10"
                                            bind:value={searchQuery}
                                            onkeypress={handleKeyPress}
                                        />
                                    </div>
                                    <Button
                                        variant="outline"
                                        size="icon"
                                        class="shrink-0"
                                        onclick={searchLocation}
                                    >
                                        <MapPin class="h-4 w-4" />
                                    </Button>
                                </div>
                            </Card.Content>
                        </Card.Root>
                        {#if !isMobileView}
                            <div
                                class="w-80"
                                transition:fly={{
                                    x: 200,
                                    duration: 300,
                                    opacity: 1,
                                }}
                            >
                                <Card.Root>
                                    <Card.Content class="p-4">
                                        <h2 class="text-lg font-semibold mb-6">
                                            {$_("events.latest")}
                                        </h2>
                                        <EventList />
                                    </Card.Content>
                                </Card.Root>
                            </div>
                        {/if}
                    </div>
                </div>
        </HeaderPage>
    </Pane>
    {#if showCreateEvent}
        <Pane size={70}>
            <div class="flex h-full flex-col bg-card overflow-hidden">
                <!-- Header with buttons -->
                <div
                    class="flex items-center justify-between px-4 py-2 border-b flex-shrink-0"
                >
                    <Button
                        variant="ghost"
                        size="icon"
                        class="h-6 w-6"
                        onclick={() => {
                            showCreateEvent = false;
                        }}
                    >
                        <div class="flex items-center">
                            <ChevronRight class="h-3 w-3 -mr-3" />
                            <ChevronRight class="h-3 w-3" />
                        </div>
                    </Button>

                    <!-- Footer content moved to header right -->
                    <div class="flex items-center gap-2">
                        <!-- <slot name="footer" /> -->
                    </div>
                </div>

                <!-- Content area -->
                <div class="flex-1 overflow-y-auto">
                    <div class="p-6">
                        <NotionEventCreator />
                    </div>
                </div>
            </div>
        </Pane>
    {/if}
</Splitpanes>

<style global>
    .splitpanes.my-theme {
        height: 100%;
        
        .splitpanes__pane {
            background-color: none;
            overflow: hidden;
        }
        .splitpanes__splitter {
            background-color: #ccc;
            position: relative;
            &:before {
                content: "";
                position: absolute;
                left: 0;
                top: 0;
                transition: opacity 0.4s;
                background-color: rgba(255, 0, 0, 0.3);
                opacity: 0;
                z-index: 1;
            }
            &:hover:before {
                opacity: 1;
            }
            &.splitpanes__splitter__active {
                z-index: 2; /* Fix an issue of overlap fighting with a near hovered splitter */
            }
        }
    }
    .my-theme {
        &.splitpanes--vertical > .splitpanes__splitter:before {
            left: -30px;
            right: -30px;
            height: 100%;
            cursor: col-resize;
        }
        &.splitpanes--horizontal > .splitpanes__splitter:before {
            top: -30px;
            bottom: -30px;
            width: 100%;
            cursor: row-resize;
        }
    }
</style>
