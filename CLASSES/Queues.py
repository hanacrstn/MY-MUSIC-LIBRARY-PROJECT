
#QUEUES CLASS

class Node:
    def __init__(self, track=None):
        self.track = track
        self.next = None


class Queue:
    def __init__(self):
        self.t_first = None
        self.t_last = None
        self.t_current = None
        self.n_tracks = 0

       
        self.shuffle_ = False
        self.repeat_ = False
        self.playing_ = False

        
        self.queuelist = []

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
        
        if self.n_tracks == 0:
            return "Queue is empty. No tracks to play."

        if self.shuffle_:
            return self.shuffle()

        if not self.current:
            self.current = self.t_first
            
        else:
            if self.current == self.t_last and not self.repeat_:
                return self.rear.track
            self.current = self.current.next if self.current != self.t_last else self.t_first

        return self.current.track

    def previous_track(self):
        if self.n_tracks == 0:
            return "Queue is empty. No tracks to play."

        if not self.current:
            self.current = self.front
            return self.current.track

        if self.current == self.front:
            if self.repeat_:
                self.current = self.rear
                return self.current.track
            return "No previous track. You're at the first track."

        temp = self.front
        while temp.next != self.current:
            temp = temp.next

        self.current = temp
        return self.current.track

    def play(self):
        
        if not self.current:
            return "No track is currently playing."

        t = self.current.track
        return f"{t['title']} by {t['artist']} ({t['duration']})"

    def add_track(self, track):
         new_node = Node(track)

        if self.n_tracks == 0:
            self.t_first = self.rear = new_node
            new_node.next = new_node
        else:
            self.t_last.next = new_node
            self.t_last = new_node
            self.t_last.next = self.t_first

        self.n_tracks += 1
        self.queuelist.append(new_node)
        return True
            
            
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

