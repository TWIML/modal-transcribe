<script>
  import { podcastEpisodes } from '$lib/podcastStores';
  import ListPlaceholder from '$lib/components/ListPlaceholder.svelte';
  import { Button } from 'flowbite-svelte';
  import { FilePenOutline } from 'flowbite-svelte-icons';
  import { POD_EPISODE_BASE_URL } from '$lib/constants';
  import moment from 'moment';

  // Adjust relative time thresholds
  moment.relativeTimeThreshold('d', 7); // days threshold is up to a week
  moment.relativeTimeThreshold('w', 10); // weeks threshold is up to 10 weeks

  function formatDate(dateString) {
    const date = moment(dateString);
    return date.format('LL');
  }

  $: episodesLoaded = {$podcastEpisodes} && Object.keys($podcastEpisodes).length > 0;
  $: sortedEpisodes = Object.entries($podcastEpisodes).sort((a, b) => b[0] - a[0]);

  // console.log("episodesLoaded", episodesLoaded);
  // console.log("podcastEpisodes", $podcastEpisodes);
  // console.log("sortedEpisodes", sortedEpisodes);

</script>

{#if episodesLoaded}
  <ul>
    {#each sortedEpisodes as [episode_num, episode] (episode.guid_hash)}
      <li class="py-2 w-full rounded-t-lg flex items-center items-start">
        <Button class={(episode.transcribed ? 
                        "bg-blue-900 text-white hover:bg-blue-900 hover:text-white" : 
                        "bg-gray-300 text-blue-900 hover:bg-gray-300 hover:text-blue-900") + 
                        " py-0.5 px-1.5 text-xs mr-2 flex items-center"} pill size="xs">
          {episode_num}
          {#if episode.transcribed}<FilePenOutline size="xs" class="ml-1"/>{/if}
        </Button>
        <div class="truncate flex items-center">
          <a href={`${POD_EPISODE_BASE_URL}/${episode_num}`} 
             class="text-blue-900 no-underline hover:underline">
            {episode.title}
          </a>
        </div><span class="text-gray-300 px-1">|</span>
        <div class="text-gray-400 text-sm w-48 flex items-center">{formatDate(episode.publish_date)}</div>
      </li>
    {/each}
  </ul>
{:else}
  <ListPlaceholder />
{/if}
