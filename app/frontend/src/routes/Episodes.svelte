<script>
  import { onMount } from 'svelte';
  import { browser } from '$app/environment';

  import moment from 'moment';

  // Adjust relative time thresholds
  moment.relativeTimeThreshold('d', 7); // days threshold is up to a week
  moment.relativeTimeThreshold('w', 10); // weeks threshold is up to 10 weeks

  function formatDate(dateString) {
    const date = moment(dateString);
    return date.format('LL');
  }
  
  let episodes = {};
  const podcastId = 'twiml-ai-podcast'; // Replace with your podcast ID

  async function fetchEpisodes() {
    const response = await fetch(`/api/podcast/${podcastId}`);
    if (response.ok) {
      const data = await response.json();
      episodes = data['episodes'];
    } else {
      console.error('Error fetching episodes');
    }
  }

  if (browser) {
    onMount(fetchEpisodes);
  }
</script>

{#if episodes && Object.keys(episodes).length > 0}
  <ul>
    {#each Object.entries(episodes).sort((a, b) => b[0] - a[0]) as [episodeNumber, episode] (episode.guid_hash)}
      <li class="px-6 py-2 w-full rounded-t-lg">
        <span class="text-gray-400">{episode.episode_number} | </span>
        <a href={`/podcast/${podcastId}/episode/${episode.episode_number}`} class="text-blue-900 no-underline hover:underline">
          {episode.title}
        </a> 
        <span class="text-gray-400"> | {formatDate(episode.publish_date)}</span>
        {episode.transcribed ? "📃 " : "  "}
      </li>
      <!-- Add more episode details here -->
    {/each}
  </ul>
{:else}
  <p>Loading episodes...</p>
{/if}
