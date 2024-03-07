/** @type {import('./$types').PageLoad} */
import { error } from '@sveltejs/kit';

export async function load({ params, fetch }) {
	const { podcastId, episodeNumber } = params;
	const res = await fetch(`/api/podcast/${podcastId}/episode/${episodeNumber}`);
	
	if (res.status === 404) {
		error(404, {
			message: 'Episode not found'
		});
	}

	const data = await res.json();

	return { data };
}