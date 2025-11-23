
#TRACK CLASS

class track:
    def __init__(self,title, artist, album,additional_artist):
        self.title = title
        self.artist = artist 
        self.album = album
        self.additional_artist = additional_artist 

    def additional_artist(self,artist_name):
        return self.additional_artist.append(artist_name)
    
    def __str__(self):
        feat = ""
        if self.additional_artist:
            feat = "(ft." +", ".join(self.additional_artist)+")"
            return f"Title: {self.title}{feat} | Artist: {self.artist} | Album: {self.album}"
        
class duration(track):
    def __init__(self,title,artist,album,additional_artist,duration):
        super().__init__(title,artist,album,additional_artist)
        self.duration_second = self.duration_seconds(duration)

    def duration_seconds(self,duration):
        minutes, seconds = [int(x) for x in duration.split(":")]
        return minutes * 60 + seconds
    
    def get_duration(self):
        minutes = self.duration_second // 60
        seconds = self.duration_second % 60
        return f"{minutes:02}:{seconds:02}"
    
    def __str__(self):
        return f"{super().__str__()} | Duration: {self.duration_second}"
    
