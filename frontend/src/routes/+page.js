/** @type {import('./$types').PageLoad} */
export async function load({ params, fetch }) {
  	const podcastId = "twiml-ai-podcast";
	const res = await fetch(`/api/podcast/${podcastId}`);
	const data = await res.json();

	return { data: data['pod_metadata'] };
}