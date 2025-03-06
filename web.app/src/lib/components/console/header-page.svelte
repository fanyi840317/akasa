<script lang="ts">
    import * as Sidebar from "$lib/components/ui/sidebar";
    import * as Breadcrumb from "$lib/components/ui/breadcrumb";
    import {Separator} from "$lib/components/ui/separator";
	import { cn } from "$lib/utils.js";

    let {
		ref = $bindable(null),
        title:title,
		...restProps
	} = $props();
</script>
<header class="flex  h-16 shrink-0 items-center gap-2 justify-between">
    <div class="flex items-center gap-2 px-4">
        <Sidebar.Trigger class="-ml-1" />
        <Separator orientation="vertical" class="mr-2 h-4" />
        <Breadcrumb.Root>
            <Breadcrumb.List>
                <Breadcrumb.Item class="hidden md:block">
                    <Breadcrumb.Link href="#"
                        >Building Your Application</Breadcrumb.Link
                    >
                </Breadcrumb.Item>
                <Breadcrumb.Separator class="hidden md:block" />
                <Breadcrumb.Item>
                    <Breadcrumb.Page>{title}</Breadcrumb.Page>
                </Breadcrumb.Item>
            </Breadcrumb.List>
        </Breadcrumb.Root>
    </div>
    <div class="pr-4">
       
    </div>
</header>
<div class="flex flex-1 w-full h-full p-0">
   <slot></slot>
</div>