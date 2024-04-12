<script>
  function formatTimestamp(total_seconds) {
        let milliseconds = Math.round(total_seconds * 1000.0);

        let hours = Math.floor(milliseconds / 3_600_000);
        milliseconds -= hours * 3_600_000;

        let minutes = Math.floor(milliseconds / 60_000);
        milliseconds -= minutes * 60_000;

        let seconds = Math.floor(milliseconds / 1_000);
        milliseconds -= seconds * 1_000;

        const pad = (n, d = 2) => n.toString().padStart(d, "0");

        return `${pad(hours)}:${pad(minutes)}:${pad(seconds)}.${pad(
            milliseconds,
            3
        )}`;
    }
    export let segment;
    export let idx;
</script>

<li class="pb-3 sm:pb-4 py-2 border-b border-gray-200 w-full rounded-t-lg flex items-center space-x-4" key={idx}>
  <div class="flex-1 min-w-0">
    <p class="text-black-500">{segment.speaker}</p>
    <p class="text-gray-500">{segment.text}</p>
  </div>
  <div class="sm:inline-flex sm:flex-row items-center text-xs bg-gray-100 text-gray-900 dark:text-white">
    <a href={`#t=${Math.floor(segment.start)}`} class="hover:bg-gray-200 text-gray-800 py-1 px-1 rounded-l text-right" title="listen" target="_blank" rel="noopener noreferrer">
      🎙 {formatTimestamp(segment.start)}
    </a>
    <span class="text-gray-800 py-1 px-1">-</span>
    <a href={`#t=${Math.floor(segment.end)}`} class="hover:bg-gray-200 text-gray-800 py-1 px-1 rounded-r text-right" title="listen" target="_blank" rel="noopener noreferrer">
      {formatTimestamp(segment.end)}
    </a>
  </div>
</li>