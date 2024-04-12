<script>
  import moment from 'moment';
	import Transcript from '$lib/components/Transcript.svelte';
  import { Button } from 'flowbite-svelte';
  import { HeadphonesSolid, FilePenSolid } from 'flowbite-svelte-icons';
  import { updatePodData, podcastMetadata, podcastEpisodes, fetchMetadata } from '$lib/podcastStores';
  import { POD_API_TRANSCRIBE_URL } from '$lib/constants.js';
  import { onMount } from 'svelte';

  export let data;
  const episode = data.data.metadata;
  export let segments = data.data.segments || [];
  
  // Adjust relative time thresholds
  moment.relativeTimeThreshold('d', 7); // days threshold is up to a week
  moment.relativeTimeThreshold('w', 10); // weeks threshold is up to 10 weeks

  function formatDate(dateString) {
    const date = moment(dateString);
    return date.format('LL');
  }

  async function postTranscribe(ep_no) {
    const payload =   {
      "podcast_id": $podcastMetadata.id,
      "episode_number": ep_no,
      "overwrite_download": false,
      "overwrite_diarisation": false,
      "overwrite_transcription": false
    };

    try {
      const res = await fetch(POD_API_TRANSCRIBE_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });
      segments = res.data; // Update segments with the response data
    } catch (error) {
      console.error(error);
    }
  }

  onMount(async () => {
    await updatePodData();
  })
  
  // function to check if there are transcript segments
  $: hasTranscript = segments && segments.length > 0;
</script>

<div class="w-full">
  <div class="pb-8">
    <h1 class="text-xl pb-3 font-medium text-black"><span class="text-gray-400">{episode.episode_number} | </span>{episode.title}</h1>
    <p class="pb-2 text-gray-400">{formatDate(episode.publish_date)}</p>
    <p class="pb-2 text-gray-800">{episode.html_description}</p>
  </div>
  <div class="pb-8">
    
    <Button color="dark" pill on:click={() => postTranscribe(episode.episode_number)} disabled={hasTranscript}>
      <FilePenSolid class="w-3.5 h-3.5 me-2" /> Transcribe
    </Button>

    <Button color="dark" pill href="{episode.episode_url}">
      <HeadphonesSolid class="w-3.5 h-3.5 me-2" /> Listen
    </Button>
  </div>
  <div class="pb-8">
    {#if hasTranscript}
      <Transcript {segments}/>
    {/if}
  </div>
</div>