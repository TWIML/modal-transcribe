<script>
    const rands = [0.1449, 0.7331, 0.3427, 0.6372, 0.1494, 0.3656, 0.1603, 0.4295, 0.1853, 0.1115];
    const randomWidths = rands.map(rand => {
        return `calc(${rand * 20 + 55}% - 8px)`;
    });
    const items = randomWidths.map(width => {
        return { width };
    });
</script>

<div role="status" class="w-full animate-pulse space-y-5">
    {#each items as item}
        <div class="flex items-center justify-start w-full gap-x-1.5">
            <div class="h-2.5 bg-gray-300 dark:bg-gray-400 rounded-full" style="flex-basis: calc(4.5% - 8px);"></div> <span class="text-gray-400">|</span>
            <div class="h-2.5 bg-gray-400 dark:bg-gray-500 rounded-full" style={`flex-basis: ${item.width};`}></div> <span class="text-gray-400">|</span>
            <div class="h-2.5 bg-gray-300 dark:bg-gray-400 rounded-full" style="flex-basis: calc(15% - 8px);"></div>
        </div>
    {/each}
    <span class="sr-only">Loading...</span>
</div>