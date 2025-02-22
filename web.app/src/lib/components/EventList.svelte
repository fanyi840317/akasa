<script lang="ts">
    import * as Card from "$lib/components/ui/card";

    const events = [
        {
            id: 1,
            title: '神秘灯光事件',
            description: '多位目击者报告在成都市区上空看到不明飞行物发出的奇异光芒。',
            location: '成都市中心',
            date: '2024-04-15',
            type: 'supernatural',
            coordinates: [104.0633, 30.6516]
        },
        {
            id: 2,
            title: '古寺异响调查',
            description: '文殊院内多次传出神秘钟声，但寺内钟铃未曾敲响。',
            location: '文殊院',
            date: '2024-04-20',
            type: 'paranormal',
            coordinates: [104.1444, 30.7348]
        },
        {
            id: 3,
            title: '都江堰水文异象',
            description: '都江堰水系出现反常水流现象，专家无法解释。',
            location: '都江堰',
            date: '2024-05-01',
            type: 'unexplained',
            coordinates: [103.6192, 30.9984]
        }
    ];
</script>

<div >
    <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
        {#each events as event}
            <Card.Root class="cursor-pointer hover:bg-accent/50 transition-colors flex items-start p-3 gap-3">
                <div class="w-10 h-10 bg-gradient-to-br from-cyan-400/20 to-purple-400/20 rounded-full p-2 flex-shrink-0">
                    <svg class="w-full h-full text-cyan-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/>
                    </svg>
                </div>
                <div class="flex-1">
                    <h3 class="text-cyan-400 text-sm font-medium mb-1">{event.title}</h3>
                    <p class="text-gray-300 text-xs mb-2 line-clamp-2">{event.description}</p>
                    <div class="flex items-center justify-between text-[10px] text-gray-400">
                        <span class="flex items-center gap-1">
                            <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/>
                            </svg>
                            {event.location}
                        </span>
                        <span>{event.date}</span>
                    </div>
                </div>
            </Card.Root>
        {/each}
    </div>
</div>
