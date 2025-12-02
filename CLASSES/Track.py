from Duration import checkformat

class Track:
    counter = 0
    def __init__(self, id, title, artist, album, duration):
        self.__id = id
        self.__title = title
        self.__artist = artist
        self.__album = album
        self.__duration = checkformat(duration)

    def getID (self):
        return self.__id

    def getTitle (self):
        return self.__title
    
    def getArtist (self):
        return self.__artist
    
    def getAlbum (self):
        return self.__album
    
    def getDuration (self):
        return self.__duration

    def to_dict(self):
        return {
            "id" : self.__id,
            "title": self.__title,
            "artist": self.__artist,
            "album": self.__album,
            "duration": self.__duration
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
