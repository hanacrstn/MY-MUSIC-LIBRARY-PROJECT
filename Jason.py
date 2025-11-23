"""
music_json_system.py

JSON System Only for "Listen to the Music" project.

- Provides JSON structure: library (tracks), playlists, queue
- Functions to add tracks, create playlists, add tracks to playlist, init queue, add to queue
- Stores durations as "mm:ss" in JSON but internally converts to seconds for calculations
- No CLI — intended to be imported and used or run for the example usage at the bottom
"""

import json
import os
import uuid
from typing import List, Dict, Optional, Any

JSON_FILE = "music_data.json"


def mmss_to_seconds(mmss: str) -> int:
    """Convert 'mm:ss' (or 'm:ss') to total seconds. Safe if mmss is already 's' or numeric string."""
    mmss = mmss.strip()
    if ":" in mmss:
        parts = mmss.split(":")
        if len(parts) != 2:
            raise ValueError(f"Invalid duration format: {mmss}")
        minutes = int(parts[0])
        seconds = int(parts[1])
        return minutes * 60 + seconds
    else:
        return int(mmss)


def seconds_to_mmss(total_seconds: int) -> str:
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


def default_data_structure() -> Dict[str, Any]:
    """Return the default JSON structure when no file exists."""
    return {
        "library": {
            "tracks": []
        },
        "playlists": [], 
        "queue": {
            "tracks": [],        
            "current_index": 0,  
            "shuffled": False,
            "repeat": False
        }
    }


def load_data(file_path: str = JSON_FILE) -> Dict[str, Any]:
    if not os.path.exists(file_path):
        data = default_data_structure()
        save_data(data, file_path)
        return data
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: Dict[str, Any], file_path: str = JSON_FILE) -> None:

    try:
        data["library"]["tracks"].sort(key=lambda t: t.get("title", "").lower())
    except Exception:
        pass
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def make_track_obj(title: str, artist: str, album: str, duration_mmss: str,
                   additional_artists: Optional[List[str]] = None) -> Dict[str, Any]:
    if additional_artists is None:
        additional_artists = []
    track_id = str(uuid.uuid4())
    duration_mmss = duration_mmss.strip()
    _ = mmss_to_seconds(duration_mmss) 
    return {
        "id": track_id,
        "title": title,
        "artist": artist,
        "additional_artists": additional_artists,
        "album": album,
        "duration": duration_mmss
    }


def add_track_to_library(title: str, artist: str, album: str, duration_mmss: str,
                         additional_artists: Optional[List[str]] = None,
                         file_path: str = JSON_FILE) -> Dict[str, Any]:
    data = load_data(file_path)
    new_track = make_track_obj(title, artist, album, duration_mmss, additional_artists)
    data["library"]["tracks"].append(new_track)
    save_data(data, file_path)
    return new_track


def get_track_by_id(track_id: str, data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    if data is None:
        data = load_data()
    for t in data["library"]["tracks"]:
        if t.get("id") == track_id:
            return t
    return None


def search_tracks_by_title(query: str, file_path: str = JSON_FILE) -> List[Dict[str, Any]]:
    data = load_data(file_path)
    q = query.strip().lower()
    results = []
    for t in data["library"]["tracks"]:
        if q in t.get("title", "").lower():
            results.append(t)
    return results


def playlist_exists(name: str, data: Optional[Dict[str, Any]] = None) -> bool:
    if data is None:
        data = load_data()
    for p in data["playlists"]:
        if p.get("name", "").lower() == name.lower():
            return True
    return False


def create_playlist(name: str, file_path: str = JSON_FILE) -> Dict[str, Any]:
    data = load_data(file_path)
    if playlist_exists(name, data):
        raise ValueError(f"A playlist with the name '{name}' already exists.")
    playlist = {
        "id": str(uuid.uuid4()),
        "name": name,
        "created_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "tracks": [],  # store track IDs
        "total_duration": "00:00"
    }
    data["playlists"].append(playlist)
    save_data(data, file_path)
    return playlist


def add_track_to_playlist(playlist_id: str, track_id: str, file_path: str = JSON_FILE) -> None:
    data = load_data(file_path)
    playlist = None
    for p in data["playlists"]:
        if p.get("id") == playlist_id:
            playlist = p
            break
    if playlist is None:
        raise ValueError("Playlist not found.")

    track = get_track_by_id(track_id, data)
    if track is None:
        raise ValueError("Track ID not found in library.")

    if track_id in playlist["tracks"]:
        return  # no-op silently; or raise if you prefer

    playlist["tracks"].append(track_id)

    total_seconds = 0
    for tid in playlist["tracks"]:
        t = get_track_by_id(tid, data)
        if t:
            total_seconds += mmss_to_seconds(t["duration"])
    playlist["total_duration"] = seconds_to_mmss(total_seconds)

    save_data(data, file_path)


def get_playlist_by_id(playlist_id: str, data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    if data is None:
        data = load_data()
    for p in data["playlists"]:
        if p.get("id") == playlist_id:
            return p
    return None


def init_queue_from_library(file_path: str = JSON_FILE) -> None:
    """Initialize queue with all library tracks in current library order."""
    data = load_data(file_path)
    track_ids = [t["id"] for t in data["library"]["tracks"]]
    data["queue"]["tracks"] = track_ids
    data["queue"]["current_index"] = 0 if track_ids else -1
    data["queue"]["shuffled"] = False
    data["queue"]["repeat"] = False
    save_data(data, file_path)


def init_queue_from_playlist(playlist_id: str, file_path: str = JSON_FILE) -> None:
    data = load_data(file_path)
    playlist = get_playlist_by_id(playlist_id, data)
    if playlist is None:
        raise ValueError("Playlist not found.")
    data["queue"]["tracks"] = list(playlist["tracks"])
    data["queue"]["current_index"] = 0 if playlist["tracks"] else -1
    data["queue"]["shuffled"] = False
    data["queue"]["repeat"] = False
    save_data(data, file_path)


def add_track_to_queue(track_id: str, file_path: str = JSON_FILE) -> None:
    data = load_data(file_path)
    if get_track_by_id(track_id, data) is None:
        raise ValueError("Track ID not found in library.")
    data["queue"]["tracks"].append(track_id)
    if data["queue"].get("current_index", -1) == -1:
        data["queue"]["current_index"] = 0
    save_data(data, file_path)


def queue_current_track(file_path: str = JSON_FILE) -> Optional[Dict[str, Any]]:
    data = load_data(file_path)
    idx = data["queue"].get("current_index", -1)
    if idx == -1 or idx >= len(data["queue"].get("tracks", [])):
        return None
    tid = data["queue"]["tracks"][idx]
    return get_track_by_id(tid, data)


def queue_next(file_path: str = JSON_FILE) -> Optional[Dict[str, Any]]:
    data = load_data(file_path)
    if not data["queue"]["tracks"]:
        return None
    idx = data["queue"].get("current_index", -1)
    if idx == -1:
        idx = 0
    else:
        idx += 1
    if idx >= len(data["queue"]["tracks"]):
        if data["queue"].get("repeat", False):
            idx = 0
        else:
            data["queue"]["current_index"] = -1
            save_data(data, file_path)
            return None
    data["queue"]["current_index"] = idx
    save_data(data, file_path)
    return queue_current_track(file_path)


def queue_previous(file_path: str = JSON_FILE) -> Optional[Dict[str, Any]]:
    data = load_data(file_path)
    if not data["queue"]["tracks"]:
        return None
    idx = data["queue"].get("current_index", -1)
    if idx == -1:
        if data["queue"].get("repeat", False):
            idx = len(data["queue"]["tracks"]) - 1
        else:
            return None
    else:
        idx -= 1
    if idx < 0:
        if data["queue"].get("repeat", False):
            idx = len(data["queue"]["tracks"]) - 1
        else:
            data["queue"]["current_index"] = -1
            save_data(data, file_path)
            return None
    data["queue"]["current_index"] = idx
    save_data(data, file_path)
    return queue_current_track(file_path)


def set_queue_repeat(value: bool, file_path: str = JSON_FILE) -> None:
    data = load_data(file_path)
    data["queue"]["repeat"] = bool(value)
    save_data(data, file_path)


def set_queue_shuffled(value: bool, file_path: str = JSON_FILE) -> None:
    data = load_data(file_path)
    data["queue"]["shuffled"] = bool(value)
    save_data(data, file_path)


def queue_total_duration(file_path: str = JSON_FILE) -> str:
    data = load_data(file_path)
    total = 0
    for tid in data["queue"].get("tracks", []):
        t = get_track_by_id(tid, data)
        if t:
            total += mmss_to_seconds(t["duration"])
    return seconds_to_mmss(total)


def import_tracks_from_json(import_file: str, file_path: str = JSON_FILE) -> List[Dict[str, Any]]:
    """
    Import tracks from another JSON (expects a list of track dicts with title/artist/album/duration).
    This will auto-create track IDs for each imported track and append to library.
    """
    if not os.path.exists(import_file):
        raise FileNotFoundError("Import file not found.")
    with open(import_file, "r", encoding="utf-8") as f:
        payload = json.load(f)
    candidates = []
    if isinstance(payload, dict):
        candidates = payload.get("tracks", [])
    elif isinstance(payload, list):
        candidates = payload
    else:
        raise ValueError("Unrecognized JSON format for import.")

    added = []
    for entry in candidates:
        title = entry.get("title") or entry.get("name") or "Untitled"
        artist = entry.get("artist") or "Unknown"
        album = entry.get("album") or "Unknown Album"
        duration = entry.get("duration") or "00:00"
        additional = entry.get("additional_artists") or []
        try:
            newt = add_track_to_library(title, artist, album, duration, additional, file_path)
            added.append(newt)
        except Exception:
            continue
    return added


if _name_ == "_main_":
    data = load_data()

    # Add example tracks (id auto-generated)
    t1 = add_track_to_library("Gangnam Style", "PSY", "Psy 6 (Six Rules), Part 1", "03:39")
    t2 = add_track_to_library("Counting Stars", "OneRepublic", "Native", "04:17")
    t3 = add_track_to_library("GAS GAS GAS EXTENDED MIX", "Manuel", "Default Album", "04:21")

    print("Added tracks:")
    print(t1)
    print(t2)
    print(t3)

    pl = create_playlist("My Playlist")
    print("\nCreated playlist:", pl["name"], "id=", pl["id"])
    add_track_to_playlist(pl["id"], t1["id"])
    add_track_to_playlist(pl["id"], t2["id"])

    init_queue_from_playlist(pl["id"])
    print("\nQueue total duration:", queue_total_duration())
    print("Currently playing:", queue_current_track())

    nxt = queue_next()
    print("After next, currently playing:", nxt)

    final = load_data()
    print("\nSaved JSON snapshot:")
    print(json.dumps(final, indent=2, ensure_ascii=False))