<script>
  import PodcastInfo from '$lib/components/PodcastInfo.svelte';
  import Episodes from '$lib/components/Episodes.svelte';

  import { updatePodData } from '$lib/podcastStores';
  import { onMount } from 'svelte';

  onMount(async () => {
    await updatePodData();
  })
</script>

<div class="overflow-hidden pb-8">
  <PodcastInfo />
</div>
<div>
  <Episodes />
</div>

