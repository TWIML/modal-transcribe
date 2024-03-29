import { writable } from 'svelte/store';
import { browser } from '$app/environment';
import { POD_API_BASE_URL, POD_API_EPISODES_URL } from '$lib/constants';

export const podcastMetadata = writable({});

export async function fetchMetadata() {
  // console.log("fetching metadata");
  const response = await fetch(POD_API_BASE_URL);
  if (response.ok) {
    const data = await response.json();
    podcastMetadata.set(data[0]);
    // console.log("metadata fetched");
  } else {
    console.error('Error fetching podcast metadata.');
  }
}

export const podcastEpisodes = writable({});

export async function fetchEpisodes() {
  // console.log("fetching episodes");
  const response = await fetch(POD_API_EPISODES_URL);
  if (response.ok) {
    let data = await response.json();
    data = data['episodes'];
    // console.log(data);
    podcastEpisodes.set(data);
    // console.log(`${Object.keys(data).length} episodes fetched`);
  } else {
    console.error('Error fetching podcast episodes.');
  }
}

export async function updatePodData() {
  if (!browser) return; // Ensure fetch is only called in the browser
  // console.log("Updating podcast data");
  await fetchMetadata();
  await fetchEpisodes();
}

// // Debugging: Subscribe to the metadata store and log its current value
// podcastMetadata.subscribe(value => {
//   console.log("Metadata store updated:", value);
// });

// // Debugging: Subscribe to the store and log its current value
// podcastEpisodes.subscribe(value => {
//   console.log("Episode store updated:", value);
// });