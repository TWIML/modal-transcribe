import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://kit.svelte.dev/docs/integrations#preprocessors
	// for more information about preprocessors
	preprocess: [vitePreprocess({})],

	kit: {
		// user node adapter
		adapter: adapter(),
		// adapter-static allows you to customize the output directory and assets path
		// See https://kit.svelte.dev/docs#adapters for more information about adapters.
		// adapter: adapter({
		// 	pages: 'dist',
		// 	assets: 'dist',
		// 	fallback: 'index.html',
		// 	strict: false
		// })
	}
};

export default config;