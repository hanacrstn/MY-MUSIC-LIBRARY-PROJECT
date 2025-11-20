
#TRACK CLASS

class Track:
    def __init__(self, title, artist, feat, album, duration):
        self.__title = title
        self.__artist = artist
        self.__feat = feat
        self.__album = album
        self.__duration = duration

    def getTitle(self):
        return self.__title
    def getArtist(self):
        return self.__artist
    def getFeat(self):
        return self.Feat
    def getAlbum(self):
        return self.__album
    def getDuration(self):
        return self.__duration
    
    def setTitle(self, newTitle):
        self.__title = newTitle
    def setArtist(self, newArtist):
        self.__artist = newArtist
    def setFeat(self, newFeat):
        self.__feat = newFeat
    def setAlbum(self, newAlbum):
        self.__album = newAlbum
    def setDuration(self, newDuration):
        self.__duration = newDuration

    def store_dict(self):
        return {
            'title': self.__title,
            'artist': self.__artist,
            'featuring': self.__feat,
            'album': self.__album,
            'duration': self.__duration
        }
    
    @classmethod
    def fetch_dict(cls, data):
        return cls(
            data['title'],
            data['artist'],
            data['featuring'],
            data['album'],
            data['duration']
        )