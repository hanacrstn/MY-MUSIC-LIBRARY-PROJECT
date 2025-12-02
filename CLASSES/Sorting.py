
def merge_sort(tracks, key):
    if len(tracks) <= 1:
        return tracks

    mid = len(tracks) // 2
    left = merge_sort(tracks[:mid], key)
    right = merge_sort(tracks[mid:], key)

    return merge(left, right, key)

def merge(left, right, key):
    sorted_tracks = []

    while left and right:
        comparison = compare_tracks(left[0], right[0], key)

        if comparison < 0:
            sorted_tracks.append(left.pop(0))
        elif comparison > 0:
            sorted_tracks.append(right.pop(0))
        else:
            sorted_tracks.append(left.pop(0)) 

    sorted_tracks.extend(left)
    sorted_tracks.extend(right)

    return sorted_tracks

def compare_tracks(track1, track2, key):
    def normalize(value):
        return value.lower() if isinstance(value, str) else value

    if normalize(track1[key]) != normalize(track2[key]):
        return (normalize(track1[key]) > normalize(track2[key])) - (normalize(track1[key]) < normalize(track2[key]))

    attributes = ['title', 'artist', 'album', 'duration', 'id']
    for attribute in attributes:
        if attribute != key and normalize(track1[attribute]) != normalize(track2[attribute]):
            return (normalize(track1[attribute]) > normalize(track2[attribute])) - (normalize(track1[attribute]) < normalize(track2[attribute]))

    return 0
