<script lang="ts">
    import { _ } from 'svelte-i18n';
    import StepWindow from "$lib/components/StepWindow.svelte";
    import BasicInfo from "./BasicInfo.svelte";
    import LocationPicker from "./LocationPicker.svelte";
    import ImageUpload from "./ImageUpload.svelte";
    import { Button } from "$lib/components/ui/button";
    import { ChevronRight, ChevronLeft } from "lucide-svelte";

    export let showStepWindow = false;
    export let title = "";
    export let description = "";
    export let location = "";
    export let imageFile: File | null = null;
    export let imagePreview: string | null = null;
    export let onClose :() => void = () => {};

    let currentStep = 0;
    const totalSteps = 3;

    const stepComponents = [
        { component: BasicInfo, props: { title, description } },
        { component: LocationPicker, props: { location } },
        { component: ImageUpload, props: { imageFile, imagePreview } }
    ];

    const steps = [
        { title: $_('events.create.step1_title'), description: $_('events.create.step1_desc') },
        { title: $_('events.create.step2_title'), description: $_('events.create.step2_desc') },
        { title: $_('events.create.step3_title'), description: $_('events.create.step3_desc') }
    ];

    function nextStep() {
        if (currentStep < totalSteps - 1) {
            currentStep++;
        }
    }

    function prevStep() {
        if (currentStep > 0) {
            currentStep--;
        }
    }

    function handleClose() {
        currentStep = 0;
        title = "";
        description = "";
        location = "";
        imageFile = null;
        imagePreview = null;
        onClose();
    }
</script>

{#if showStepWindow}
    <StepWindow
        {steps}
        {currentStep}
        closeWind={handleClose}
    >
        <div class="space-y-8">
            {#each stepComponents as { component, props }, index}
                {#if index === currentStep}
                    <svelte:component 
                        this={component} 
                        {...props}
                        bind:title
                        bind:description
                        bind:location
                        bind:imageFile
                        bind:imagePreview
                    />
                {/if}
            {/each}
        </div>
    </StepWindow>
{/if}