<script>
	import { page } from '$app/stores';
</script>

<div class="mx-auto max-w-4xl py-8 rounded overflow-hidden shadow-lg">
    <div class="px-6 py-4">
      <div class="font-bold text-xl">Error: {$page?.error?.message}</div>
      <div class="text-gray-700 text-md py-1">
        <h1>It seems there has been an error, sorry about that.</h1>
        {#if $page?.error}
            <div class="mt-4 p-4 border-y-2">
                {#if $page?.status}
                    <p>Page status: {$page?.status} +++</p>
                {/if}
                {#if $page?.error?.message}
                    <p>Error message: {$page?.error?.message}</p>
                {/if}
            </div>
        {/if}
      </div>
    </div>
</div>
