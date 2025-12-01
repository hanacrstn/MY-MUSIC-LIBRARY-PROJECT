
#QUEUES CLASS

class Queue:
    def __init__(self):
        pass

    def save_queue(self):
        pass

    def load_queue(self):
        pass

    def save_current_track(self):
        pass

    def shuffle(self):
        pass

    def unshuffle(self):
        pass

    def repeat(self):
        pass

    def next_track(self):
        pass

    def previous_track(self):
        pass

    def play(self):
        pass

    def add_track(self, track):
       if track is None:
            print("Cannot add None as a track.")
            return False
    #wala pa 
            
    def add_play(self, playlist):
     if playlist is None:
            print("Cannot add None as a playlist.")
            return False
        
        try:
            tracks_to_add = []
            
            if hasattr(playlist, 'getTracks'):
                tracks_to_add = playlist.getTracks()
            elif isinstance(playlist, list):
                tracks_to_add = playlist
            else:
                print(" Playlist format not recognized.")
                return False
           #wala pa nahuman 

    def queue_pagination(self, , items_per_page=10):
        try:
            if items_per_page <= 0:
                items_per_page = 10
            return Pagination(self.tracks, items_per_page)
        except Exception as e:
            print(f"Failed to create pagination: {e}")
            return Pagination([], 10)
    
    def total_duration(self):
        pass

    def clear_queue(self):
        pass

