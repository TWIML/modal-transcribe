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