<script lang="ts">
	import { Calendar } from '$lib/components/ui/calendar';
	import * as Popover from '$lib/components/ui/popover';
	import type { DateValue } from '@internationalized/date';
	import { DateFormatter, getLocalTimeZone, parseDate } from '@internationalized/date';

	import type { Snippet } from 'svelte';
	import Textarea from '../ui/textarea/textarea.svelte';
	import * as Card from '$lib/components/ui/card';
	import Button from '../ui/button/button.svelte';
	import Map from '../map/map.svelte';
	import { Input } from '../ui/input';
	import { MapIcon, MapPinHouse } from '@lucide/svelte';

	let { value, onDateChange, children } = $props<{
		value?: string;
		onDateChange?: (e: { date: DateValue }) => void;
		children?: Snippet;
	}>();
</script>

<Popover.Root>
	<Popover.Trigger>
		{@render children()}
	</Popover.Trigger>
	<Popover.Content class="w-[500px] h-[400px] p-0 border-0 bg-transparent " align="start">
		<Card.Root class="w-full h-full pb-0">
			<Card.Header>
				<Card.Title>Event location</Card.Title>
				<Card.Description>Event happens on this location</Card.Description>
				<Card.Action class="gap-2">
                    <Button variant="ghost"><MapPinHouse class="size-4 text-foreground/50" /></Button>
                    <Button variant="secondary">Save</Button>
                </Card.Action>
			</Card.Header>
			<Card.Content >
                <div class="w-full relative">
                    <Input class="placeholder:text-xs w-full pl-8 relative" placeholder="you can select a location or type in an address" >
               
                    </Input>
                    <MapIcon class="text-foreground/50 absolute left-2 top-1/2 transform -translate-y-1/2 size-4" />
                </div>
               

			</Card.Content>
            <Map class="rounded-b-3xl "/>
		</Card.Root>
	</Popover.Content>
</Popover.Root>
