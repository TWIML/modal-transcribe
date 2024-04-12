<script>
	import '../app.pcss';
  import { Breadcrumb, BreadcrumbItem } from 'flowbite-svelte';
  import { podcastMetadata } from '$lib/podcastStores';
  import { page } from '$app/stores'; // Importing page store for current URL

  $: metadataLoaded = {$podcastMetadata} && $podcastMetadata.title;
  // Function to check if we're not on the root page
  $: isNotRootPage = $page.url.pathname !== '/';
  // console.log("page: ", $page.url.pathname);

</script>


<header class="bg-gray-800 text-white py-4">
  <div class="container mx-auto px-4">
    <h1 class="text-2xl font-bold">TWIML-RAG</h1>
  </div>
</header>

<main class="container mx-auto mt-8">
  <div class="max-w-3xl mx-auto pb-8">
    <Breadcrumb>
      <BreadcrumbItem href="/" home>
        {#if metadataLoaded}{$podcastMetadata.title}{/if}
      </BreadcrumbItem>
      {#if isNotRootPage}
        <BreadcrumbItem>Episode</BreadcrumbItem>
      {/if}
    </Breadcrumb>
  </div>
  <div class="max-w-3xl mx-auto">
    <slot />
  </div>
</main>

