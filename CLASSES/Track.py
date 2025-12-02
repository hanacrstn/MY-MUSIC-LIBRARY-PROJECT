
from Duration import checkformat

class Track:
    counter = 0
    def __init__(self, id, title, artist, album, duration):
        self.id = id
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = checkformat(duration)

    def to_dict(self):
        return {
            "id" : self.id,
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "duration": self.duration
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["title"], data["artist"], data["album"], data["duration"])
    
    def __str__(self):
        return f"{self.__title} by {self.__artist} ({self.get_duration()})"


class Playlist_:
    def __init__(self, id, playlist):
        self.id = id
        self.playlist = playlist

    def convertList (self):
        return {
            "id" : self.id,
            self.playlist : []
            }
