
#TRACK CLASS

class Track:
    def __init__(self, title, artist, feat, album, duration):
        self.title = title
        self.artist = artist
        self.feat = feat
        self.album = album
        self.duration = duration

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