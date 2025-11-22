
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
    def from_dict(cls, data):
        return cls(
            title=data['title'],
            artist=data['artist'],
            feat=data['feat'],
            album=data['album'],
            duration=data['duration']
        )
    
    def __str__(self):
        if self.feat:
            return f"{self.title} - {self.artist} ft. {self.feat} ({self.duration})"
        else:
            return f"{self.title} - {self.artist} ({self.duration})"
    
    def __repr__(self):
        return f"Track('{self.title}', '{self.artist}', '{self.feat}', '{self.album}', '{self.duration}')"