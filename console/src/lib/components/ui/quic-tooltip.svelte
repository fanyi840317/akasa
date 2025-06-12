<script lang="ts">
	import { buttonVariants } from './button/index.js';
	import * as Tooltip from '$lib/components/ui/tooltip/index.js';
	let { content, children } = $props();
</script>

<Tooltip.Provider>
	<Tooltip.Root>
		<Tooltip.Trigger>
			{@render children()}
		</Tooltip.Trigger>
		<Tooltip.Content>
			{@render content()}
		</Tooltip.Content>
	</Tooltip.Root>
</Tooltip.Provider>
