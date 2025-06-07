import type { Snippet } from 'svelte';

interface PanelContentProps {
    title: string;
    time: string;
    status: string;
    content: string;
}

export const createPanelContent = (props: PanelContentProps): Snippet => {
    return () => `
        <div class="space-y-4">
            <div class="prose dark:prose-invert">
                <h3 class="text-lg font-medium">${props.title}</h3>
                <div class="flex gap-4 text-sm text-muted-foreground">
                    <span>${props.time}</span>
                    <span>${props.status}</span>
                </div>
                <div class="mt-4">
                    ${props.content}
                </div>
            </div>
        </div>
    `;
}; 