<script lang="ts">
    // import { _ } from 'svelte-i18n';
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

<div class="p-6">
    <div class="space-y-6">
        {#each events as event}
            <Card.Root class="event-card p-6 rounded-lg cursor-pointer">
                <Card.Header>
                    <Card.Title>
                        <h3 class="text-xl font-bold text-cyan-400">{event.title}</h3>
                        <span class="text-xs px-3 py-1 rounded-full bg-purple-900/50">{event.type}</span>
                    </Card.Title>
                </Card.Header>
                <Card.Content>
                    <p class="mt-3 text-gray-300">{event.description}</p>
                    <div class="mt-4 flex justify-between text-sm text-gray-400">
                        <span class="flex items-center">
                            <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                                <path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/>
                            </svg>
                            {event.location}
                        </span>
                        <span>{event.date}</span>
                    </div>
                </Card.Content>
            </Card.Root>
        {/each}
    </div>
</div>
