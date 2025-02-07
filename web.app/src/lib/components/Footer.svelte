<script lang="ts">
	import { siteConfig } from "$lib/config/site.js";
	import { _ } from 'svelte-i18n';
</script>

<footer class="border-t py-6 md:py-0">
	<div class="container flex flex-col items-center justify-between gap-4 md:h-24 md:flex-row">
		<div class="flex flex-col items-center gap-4 px-8 md:flex-row md:gap-2 md:px-0">
			<p class="text-center text-sm leading-loose text-muted-foreground md:text-left">
				{$_('footer.copyright')}
			</p>
			<nav class="flex items-center space-x-4 text-sm">
				<a href="/terms" class="text-muted-foreground hover:text-foreground">
					{$_('footer.terms')}
				</a>
				<a href="/privacy" class="text-muted-foreground hover:text-foreground">
					{$_('footer.privacy')}
				</a>
			</nav>
		</div>
	</div>
</footer>