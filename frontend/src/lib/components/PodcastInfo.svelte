<script>
  import { podcastMetadata } from '$lib/podcastStores';
  import ImagePlaceholder from '$lib/components/ImagePlaceholder.svelte';

  $: metadataLoaded = {$podcastMetadata} && $podcastMetadata.title;

</script>

{#if metadataLoaded}
  <div class="grid grid-cols-[auto_1fr] gap-4">
    <div class="flex justify-start">
      <img src="{$podcastMetadata.image_url}" alt="{$podcastMetadata.title}" class="w-40 h-40 object-contain">
    </div>
    <div>
      <div class="font-bold text-xl">{$podcastMetadata.title}</div>
      <div class="text-gray-700 text-md py-1">
        {$podcastMetadata.description}
      </div>
    </div>
  </div>
{:else}
  <ImagePlaceholder />
{/if}