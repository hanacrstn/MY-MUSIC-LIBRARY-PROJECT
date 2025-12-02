

from Duration import checkformat

class Track:
    counter = 0
    def __init__(self, id, title, artist, album, duration):
        self.id = id
        self.title = title.strip() if title else ""
        self.artist = artist.strip() if artist else ""
        self.album = album.strip() if album else ""
        self.duration = checkformat(duration)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "duration": self.duration
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"], 
            data["title"], 
            data["artist"], 
            data["album"], 
            data["duration"]
        )
    
    def __str__(self):
        from Duration import sec_to_min
        return f"{self.title} by {self.artist} ({sec_to_min(self.duration)})"


class Playlist:
    
    def __init__(self, name, tracks=None):
        self.name = name
        self.tracks = tracks if tracks is not None else []
    
    def add_track(self, track):
        if track not in self.tracks:
            self.tracks.append(track)
            return True
        return False
    
    def remove_track(self, track):
        if track in self.tracks:
            self.tracks.remove(track)
            return True
        return False
    
    def get_duration(self):
        return sum(int(track.duration) for track in self.tracks)
    
    def to_dict(self):
        return {
            self.name: [
                track.to_dict() if isinstance(track, Track) else track
                for track in self.tracks
            ]
        }
    
    def __str__(self):
        return f"Playlist: {self.name} ({len(self.tracks)} tracks)"
