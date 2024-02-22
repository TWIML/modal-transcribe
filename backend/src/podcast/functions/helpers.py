def sizeof_fmt(num, suffix="B") -> str:
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)

def sorting_key(item):
    episode_number = item[1].get("episode_number")
    if episode_number is None:
        return (1, 0)
    try:
        # Try to convert the episode number to an integer for sorting
        return (0, int(episode_number))
    except ValueError:
        # If the episode number is a compound number, split it and convert both parts to integers for sorting
        episode, part = map(int, episode_number.split('.'))
        return (0, episode, -part)