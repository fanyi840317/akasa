<script lang="ts">
    import { UserAvatar } from "../ui";
    import type { Event } from "$lib/types/event";

    let { event, isEven ,onclick} = $props<{
        event: Event | null;
        isEven: boolean;
        onclick?: (event: Event) => void;
    }>();
</script>

<button
    class="flex h-[68px] group buttonActiveRing items-stretch
    justify-start pl-4 rounded-xl cursor-pointer
     {isEven ? 'bg-transparent' : 'bg-base-200'}"
     onclick = {() => onclick?.(event)}
>
    <div
        class="relative text-sm leading-snug flex justify-center gap-1 shrink-0 flex-col pr-2 w-4/12 min-w-48 md:min-w-64"
    >
        <div class="flex truncate justify-between w-full">
            <h3 class="font-semibold flex gap-2 text-base-content">
                {event.title}
            </h3>
        </div>
        <p
            class="font-normal w-full shrink text-left truncate text-base-content/50"
        >
            {event.summary||"没有摘要"}
        </p>
    </div>
    <div
        class="w-1/12 min-w-28 border-l-4 border-base-100 dark:border-dark-bg flex-center px-2 shrink-0"
    >
        <UserAvatar
            fallback={event.  creator_name|| "?"}
            class="bg-primary size-8"
            fallbackClass="text-secondary"
        ></UserAvatar>
        <!-- <div class="size-[34px] group/avatar flex-center">
            <span
                class="size-7 ring-2 text-xs relative font-bold leading-none rounded-full bg-white dark:bg-light-200"
            >
                <div
                    class="inset-0 absolute rounded-full"
                    style="background-color: rgba(232, 201, 201, 0.65);"
                ></div>
                <div
                    class="absolute centerAbs mix-blend-color-burn text-light-primary"
                >
                    {users[event.createdBy]?.name?.[0] || "?"}
                </div>
            </span>
        </div> -->
    </div>
    <div
        class="w-1/12 min-w-28 border-l-4 border-base-100 dark:border-dark-bg flex-center"
    >
        <div class="w-14 h-1.5 rounded-full bg-base-200/30">
            <div
                class="h-full rounded-full bg-primary"
                style="width: {event.credibilityScore * 100}%"
            ></div>
        </div>
    </div>
    <div
        class="w-1/12 min-w-28 flex-center border-l-4 border-base-100 dark:border-dark-bg flex items-center pl-2"
    >
        <span class="text-xs"
            >{new Date(event.occurredAt).toLocaleDateString("zh-CN")}</span
        >
    </div>
    <!-- <div class="w-auto ml-2 flex gap-2 items-center">
    {#if event.evidence && event.evidence.length > 0}
      <div class="flex -space-x-2">
        {#each event.evidence.slice(0, 3) as evidence}
          <img src={evidence.url} alt={evidence.description} class="w-8 h-8 rounded-lg border-2 border-base-100 object-cover" />
        {/each}
      </div>
      {#if event.evidence.length > 3}
        <span class="text-xs text-base-content/50">+{event.evidence.length - 3}</span>
      {/if}
    {/if}
  </div> -->
    <div
        class="hidden w-fill grow sm:flex overflow-hidden rounded-lg overflow-hiddenjustify-start items-center relative noScrollbar mr-1.5"
    >
        <div class="flex gap-px rounded-lg overflow-hidden h-14">
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.666667 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/00598361-fcbb-4086-a6e3-d95a430949ef/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="00598361-fcbb-4086-a6e3-d95a430949ef"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/2b0f8460-c33f-4cad-8320-9b8ec35a7d76/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="2b0f8460-c33f-4cad-8320-9b8ec35a7d76"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/ff91b34e-3784-4284-9868-3108394635d6/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="ff91b34e-3784-4284-9868-3108394635d6"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.666667 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/b1bb962c-88a9-4be5-9835-a6bf2cba7946/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="b1bb962c-88a9-4be5-9835-a6bf2cba7946"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.666667 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/a9cf0f90-f173-4dcc-9106-682415dcc124/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="a9cf0f90-f173-4dcc-9106-682415dcc124"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.666667 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/357f7972-709b-4a96-8283-cab973724406/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="357f7972-709b-4a96-8283-cab973724406"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.666667 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/03c58ee0-7a40-466c-a367-c63958b6f170/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="03c58ee0-7a40-466c-a367-c63958b6f170"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.666667 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/92139b7a-e34b-46ed-be9a-909fe21c3f27/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="92139b7a-e34b-46ed-be9a-909fe21c3f27"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.666667 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/002539e3-46e2-4c84-96b7-fb0227993c02/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="002539e3-46e2-4c84-96b7-fb0227993c02"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.666667 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/31d9585d-a24f-4ef8-8778-db7dbe8e018b/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="31d9585d-a24f-4ef8-8778-db7dbe8e018b"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.666667 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/51c9c534-bab5-4fd8-b066-3c93c633ac11/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="51c9c534-bab5-4fd8-b066-3c93c633ac11"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.666667 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/5b715336-1b9b-4a89-83b7-565cc59f5539/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="5b715336-1b9b-4a89-83b7-565cc59f5539"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.666667 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/e6af9a97-67a4-40f1-8dc8-ae419e7c1778/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="e6af9a97-67a4-40f1-8dc8-ae419e7c1778"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.753247 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/48e2444e-4b3c-4304-b1aa-aa6d0f81d8c4/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="48e2444e-4b3c-4304-b1aa-aa6d0f81d8c4"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.666667 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/8d23187a-07f9-4861-aff5-095f0da2edd5/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="8d23187a-07f9-4861-aff5-095f0da2edd5"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.666667 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/16f5940b-c3ae-4f2d-ac19-1bc57fecad86/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="16f5940b-c3ae-4f2d-ac19-1bc57fecad86"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.666667 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/1eb7c60b-0029-4130-9b62-c5f49d8b215b/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="1eb7c60b-0029-4130-9b62-c5f49d8b215b"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.666667 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/c859edb1-514d-48ba-ac46-140fc18763b0/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="c859edb1-514d-48ba-ac46-140fc18763b0"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.666667 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/43283c85-890c-4364-b0fa-465e3764c9ac/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="43283c85-890c-4364-b0fa-465e3764c9ac"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1.5 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/1366da19-8154-46c1-ac6c-d29dbbc85dfe/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="1366da19-8154-46c1-ac6c-d29dbbc85dfe"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1.5 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/cdfd140c-1e57-40fa-aa22-e9c322e539c4/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="cdfd140c-1e57-40fa-aa22-e9c322e539c4"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1.5 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/b41b5bdb-3752-4dab-9a9e-5aabd188f47b/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="b41b5bdb-3752-4dab-9a9e-5aabd188f47b"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.666667 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/a578f9d6-989a-4090-8255-65bec1927404/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="a578f9d6-989a-4090-8255-65bec1927404"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.666667 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/63d04623-2b0b-42a7-9977-e9a401137827/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="63d04623-2b0b-42a7-9977-e9a401137827"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1.32759 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/18539e5a-1152-458c-9797-6af718bfa903/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="18539e5a-1152-458c-9797-6af718bfa903"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/c6df27c7-3119-47d6-b082-b594fe030523/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="c6df27c7-3119-47d6-b082-b594fe030523"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/95402817-923e-4b1e-a157-f1a31c7233ce/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="95402817-923e-4b1e-a157-f1a31c7233ce"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.753247 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/32d81624-6f1d-4d46-baf9-a10c55aa44d0/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="32d81624-6f1d-4d46-baf9-a10c55aa44d0"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/bd73c6f6-3307-44db-8a53-ba959dfc0777/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="bd73c6f6-3307-44db-8a53-ba959dfc0777"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.56044 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/45f41946-b69b-46df-84a7-491e59dae651/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="45f41946-b69b-46df-84a7-491e59dae651"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/c1009da1-a4df-455b-81f1-71d0715382fd/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="c1009da1-a4df-455b-81f1-71d0715382fd"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/c44fbcda-e14a-4bca-b7f2-db84c84f3f5e/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="c44fbcda-e14a-4bca-b7f2-db84c84f3f5e"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/ff8f169a-0b68-4576-b2f3-ab00c5b6bfd8/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="ff8f169a-0b68-4576-b2f3-ab00c5b6bfd8"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.56044 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/53dd1edc-8d0c-4efe-86ad-afbe159b94ec/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="53dd1edc-8d0c-4efe-86ad-afbe159b94ec"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.56044 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/d6577389-31b6-4f17-ab1b-f7911a42ee03/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="d6577389-31b6-4f17-ab1b-f7911a42ee03"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.56044 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/9179f76c-8217-4c32-bf35-2a8f1b746301/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="9179f76c-8217-4c32-bf35-2a8f1b746301"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.56044 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/79a89135-f02b-4089-a100-9a7432ae0566/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="79a89135-f02b-4089-a100-9a7432ae0566"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.56044 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/45ffc900-6478-4f84-9dbb-d43a274a9d1b/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="45ffc900-6478-4f84-9dbb-d43a274a9d1b"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/808c3f42-f8dc-4e46-b8d0-e31da5cc7563/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="808c3f42-f8dc-4e46-b8d0-e31da5cc7563"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/2f83d1fe-7ef2-44c6-a5c1-d1902ae5222e/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="2f83d1fe-7ef2-44c6-a5c1-d1902ae5222e"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/137c74f0-b580-418f-b68c-652c32d1ca57/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="137c74f0-b580-418f-b68c-652c32d1ca57"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/a8f82d87-9a2b-432c-90a5-1a6c2fb010dc/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="a8f82d87-9a2b-432c-90a5-1a6c2fb010dc"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/ed2799d0-4a99-41f3-b812-81982b9ffb57/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="ed2799d0-4a99-41f3-b812-81982b9ffb57"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/3b27a767-e358-462e-89f3-715ae5b70748/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="3b27a767-e358-462e-89f3-715ae5b70748"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/4b50dcb4-1fa2-4920-96c3-8cf98fe096e5/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="4b50dcb4-1fa2-4920-96c3-8cf98fe096e5"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.753247 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/033eff84-a1ab-4707-8d40-5cfb7b5e5f8c/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="033eff84-a1ab-4707-8d40-5cfb7b5e5f8c"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.56044 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/4879ea12-afae-4c4f-9dbb-f8e9dbf02c07/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="4879ea12-afae-4c4f-9dbb-f8e9dbf02c07"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/256b54b3-1aad-492e-a05d-d6949e94e5fa/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="256b54b3-1aad-492e-a05d-d6949e94e5fa"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/8a744764-7d3a-4fd4-a5a7-d2c484fae22a/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="8a744764-7d3a-4fd4-a5a7-d2c484fae22a"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/ff38edb2-5500-43a8-8a4b-6e89a06b93fa/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="ff38edb2-5500-43a8-8a4b-6e89a06b93fa"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.56044 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/cbe224d5-2da3-4295-b160-14b463a1687d/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="cbe224d5-2da3-4295-b160-14b463a1687d"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/b84f7a7f-bf18-4e10-ac64-b4137287e885/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="b84f7a7f-bf18-4e10-ac64-b4137287e885"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.56044 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/2766d4b4-e451-40b8-8957-1e9fe7cbdcf6/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="2766d4b4-e451-40b8-8957-1e9fe7cbdcf6"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/6a239b68-83e4-4ffb-a667-c94b096b3d14/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="6a239b68-83e4-4ffb-a667-c94b096b3d14"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.56044 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/4a276dba-fed1-401a-9806-948839e5ce10/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="4a276dba-fed1-401a-9806-948839e5ce10"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/2f0d50ba-19d2-4875-9b07-15de669b860e/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="2f0d50ba-19d2-4875-9b07-15de669b860e"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/db88d8ee-ba63-4d28-b917-99fe1b45e1d0/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="db88d8ee-ba63-4d28-b917-99fe1b45e1d0"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.56044 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/1b9795e8-542b-44d1-85cf-50972c8f000f/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="1b9795e8-542b-44d1-85cf-50972c8f000f"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/e227ea94-af65-47de-bee9-51fd1db58114/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="e227ea94-af65-47de-bee9-51fd1db58114"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.56044 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/17ec99b1-deef-4b41-a20f-55fb559043a2/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="17ec99b1-deef-4b41-a20f-55fb559043a2"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/9069ebb3-a569-47a3-b89b-4e8f109dfe2a/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="9069ebb3-a569-47a3-b89b-4e8f109dfe2a"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/3e96be6e-993b-4841-be6c-fbff0381bcf5/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="3e96be6e-993b-4841-be6c-fbff0381bcf5"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/c0620714-8f46-4ec1-b158-9d1cccbce385/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="c0620714-8f46-4ec1-b158-9d1cccbce385"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/ab5cbd9d-7c86-4a53-ac93-c1e86d1ee2df/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="ab5cbd9d-7c86-4a53-ac93-c1e86d1ee2df"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 1 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/42bda04d-def8-4075-a995-c16bf9c86575/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="42bda04d-def8-4075-a995-c16bf9c86575"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.56044 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/49be850b-c942-4059-8d33-638912871c3e/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="49be850b-c942-4059-8d33-638912871c3e"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.56044 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/9eaaba04-4b1c-49e7-ab5a-6cb777801c2b/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="9eaaba04-4b1c-49e7-ab5a-6cb777801c2b"
                    style="opacity: 0.8;"
                />
            </div>
            <div
                class="flex shrink-0 gap-px bg-light-skeleton dark:bg-dark-skeleton first:rounded-l-lg last:rounded-r-lg .rounded-lg overflow-hidden"
                style="aspect-ratio: 0.56044 / 1;"
            >
                <img
                    class=""
                    src="https://cdn.midjourney.com/fd9cee20-d649-46bc-9511-b0d4d0529467/0_0_384_N.webp?method=shortest&amp;qst=6&amp;quality=15"
                    alt="fd9cee20-d649-46bc-9511-b0d4d0529467"
                    style="opacity: 0.8;"
                />
            </div>
        </div>
    </div>
</button>
