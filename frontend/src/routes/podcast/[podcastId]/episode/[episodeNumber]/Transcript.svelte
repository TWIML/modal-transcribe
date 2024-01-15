<script>
	import Segment from "./Segment.svelte";
  export let segments;
</script>
<ul class="transcript-list">
  {#each segments as segment, idx}
    <Segment {segment} {idx} />
  {/each}
</ul>