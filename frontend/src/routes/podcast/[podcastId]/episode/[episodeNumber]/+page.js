/** @type {import('./$types').PageLoad} */
export async function load({ params, fetch }) {
  const { podcastId, episodeNumber } = params;
	const res = await fetch(`/api/podcast/${podcastId}/episode/${episodeNumber}`);
	const data = await res.json();

	return { data };
}