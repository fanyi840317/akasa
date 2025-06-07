import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import { vanillaExtractPlugin } from '@vanilla-extract/vite-plugin';
import swc from 'unplugin-swc';
import wasm from 'vite-plugin-wasm';

export default defineConfig({
	plugins: [
		sveltekit(),
		wasm(),
		swc.vite({
			jsc: {
			  preserveAllComments: true,
			  parser: {
				syntax: 'typescript',
				dynamicImport: true,
				tsx: true,
				decorators: true,
			  },
			  target: 'es2022',
			  externalHelpers: false,
			  transform: {
				react: {
				  runtime: 'automatic',
				},
				useDefineForClassFields: false,
				decoratorVersion: '2022-03',
			  },
			},
			sourceMaps: true,
			inlineSourcesContent: true,
		  }),
		vanillaExtractPlugin(),
	],
  
});


