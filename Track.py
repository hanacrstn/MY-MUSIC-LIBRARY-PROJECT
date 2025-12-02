from Duration import checkformat

class Track:
    def __init__(self, id, title, artist, album, duration, featured_artist=""):
        self.id = id
        self.title = title.strip() if title else ""
        self.artist = artist.strip() if artist else ""
        self.featured_artist = featured_artist.strip() if featured_artist else ""
        self.album = album.strip() if album else ""
        self.duration = checkformat(duration)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "featured_artist": self.featured_artist,
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
            data["duration"],
            data.get("featured_artist", "")
        )
    
    def __str__(self):
        from Duration import sec_to_min
        feat = f" (ft. {self.featured_artist})" if self.featured_artist else ""
        return f"{self.title}{feat} by {self.artist} ({sec_to_min(self.duration)})"