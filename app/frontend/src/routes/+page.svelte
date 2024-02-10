<script>
  // import { Heading, P } from 'flowbite-svelte';
  import Episodes from './Episodes.svelte';
  // import moment from 'moment';

  export let data;
  const podcast = data.data;
</script>

<div class="mx-auto max-w-4xl py-8 rounded overflow-hidden shadow-lg">
    <div class="px-6 py-4">
      <div class="font-bold text-xl">{podcast.title}</div>
      <div class="text-gray-700 text-md py-1">
        {podcast.description}
      </div>
    </div>
</div>
<div class="mx-auto max-w-4xl py-8">
  <Episodes />
</div>

