
#PLAYLIST CLASS

from Track import Track

class Playlist:
    def __init__(self, name):
        self.__name = name
        self.__tracks = []  # List of Track objects
        self.__total_duration = "0:00"
        self.__calculate_total_duration()

    def getName(self):
        return self.__name
    def getTracks(self):
        return self.__tracks.copy()
    def getTotalDuration(self):
        return self.__total_duration
    def getTrackCount(self):
        return len(self.__tracks)

    def setName(self, newName):
        self.__name = newName

    def addTrack(self, track):
        if not self.__containsTrack(track):
            self.__tracks.append(track)
            self.__calculate_total_duration()
            return True
        return False
    
    def removeTrack(self, track):
        for i, existing_track in enumerate(self.__tracks):
            if self.__tracksEqual(existing_track, track):
                self.__tracks.pop(i)
                self.__calculate_total_duration()
                return True
        return False
    
    def containsTrack(self, track):
        return self.__containsTrack(track)

    def __containsTrack(self, track):
        for existing_track in self.__tracks:
            if self.__tracksEqual(existing_track, track):
                return True
        return False
    
    def __tracksEqual(self, track1, track2):
        return (track1.getTitle() == track2.getTitle() and 
                track1.getArtist() == track2.getArtist() and 
                track1.getAlbum() == track2.getAlbum())
    
    def __calculate_total_duration(self):
        total_seconds = 0
        for track in self.__tracks:
            min, sec = map(int, track.getDuration().split(':'))
            total_seconds += min * 60 + sec
        
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        self.__total_duration = f"{minutes}:{seconds:02d}"

    def store_dict(self):
        return {
            'name': self.__name,
            'tracks': [track.store_dict() for track in self.__tracks],
            'total_duration': self.__total_duration
        }
    
    @classmethod
    def fetch_dict(cls, data):
        playlist = cls(data['name'])
        playlist.__tracks = [Track.fetch_dict(track_data) for track_data in data['tracks']]
        playlist.__total_duration = data['total_duration']
        return playlist