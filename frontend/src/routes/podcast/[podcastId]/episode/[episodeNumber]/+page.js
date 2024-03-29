/** @type {import('./$types').PageLoad} */
import { error } from '@sveltejs/kit';
import { POD_API_EPISODE_BASE_URL } from '$lib/constants';

export async function load({ params, fetch }) {
	const { episodeNumber } = params;
	const res = await fetch(`${POD_API_EPISODE_BASE_URL}/${episodeNumber}`);
	
	if (res.status === 404) {
		error(404, {
			message: 'Episode not found'
		});
	}

	const data = await res.json();

	return { data };
}