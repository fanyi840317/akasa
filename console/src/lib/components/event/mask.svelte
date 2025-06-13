<!-- 背景蒙层 -->
<script lang="ts">
	let {
		show = $bindable(false),
		onCancel,
		class: className
	} = $props<{
		class?: string;
		show?: boolean;
		onCancel?: () => void;
	}>();
</script>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
{#if show}
	<div class="fixed inset-0 bg-black/50 z-40 {className}" onclick={onCancel}></div>
{/if}
