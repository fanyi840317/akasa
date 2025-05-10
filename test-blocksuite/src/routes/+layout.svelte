<script lang="ts">
    import { effects as blocksEffects } from '@blocksuite/affine/effects';
    import { registerStoreSpecs } from '@blocksuite/affine/extensions';
    import { effects as presetsEffects } from '@blocksuite/integration-test/effects';

    registerStoreSpecs();
    blocksEffects();
    presetsEffects();
    let { children } = $props();
    
</script>

{@render children()}
