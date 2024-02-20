import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

console.log('Current Directory:', __dirname);

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		proxy: {
			'/api': {
				target: 'https://vshlemon--whisper-pod-transcriber-fastapi-app-dev.modal.run',
				changeOrigin: true,
				secure: false,
				// rewrite: (path) => path.replace(/^\/api/, '')
			}
		}
	},
	build: {
		minify: false,
	}
});
