<script>
  import moment from 'moment';
	import Transcript from './Transcript.svelte';
 
  export let data;
  const episode = data.data.metadata;
  const segments = data.data.segments;

  // Adjust relative time thresholds
  moment.relativeTimeThreshold('d', 7); // days threshold is up to a week
  moment.relativeTimeThreshold('w', 10); // weeks threshold is up to 10 weeks

  function formatDate(dateString) {
    const date = moment(dateString);
    return date.format('LL');
  }
</script>

<div class="w-full">
  <div class="mx-auto max-w-4xl mt-4 py-8 rounded overflow-hidden shadow-lg">
      <div class="px-6 py-4">
        <div class="text-xl pb-3 font-medium text-black">{episode.title}</div>
        <p class="pb-2 text-gray-500">Episode Number: {episode.episode_number}</p>
        <p class="pb-2 text-gray-500">Publish Date: {formatDate(episode.publish_date)}</p>
        <p class="pb-2 text-gray-500">Description: {episode.html_description}</p>
        <a href="{episode.episode_url}" class="text-blue-500">Listen to Episode</a>
      </div>
  </div>
  <div class="mx-auto max-w-4xl mt-4 py-8 rounded overflow-hidden shadow-lg">
    <div class="px-6 py-4">
      <div class="text-xl pb-3 font-medium text-black">Transcript</div>
      <Transcript {segments}/>
    </div>
  </div>
</div>