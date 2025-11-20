
#QUEUES CLASS

from Track import Track
from Playlist import Playlist

class Node:
    def __init__(self, track):
        self.__track = track
        self.__next = None
        self.__prev = None

    def getTrack(self):
        return self.__track
    def getNext(self):
        return self.__next
    def getPrev(self):
        return self.__prev

    def setNext(self, new_next):
        self.__next = new_next    
    def setPrev(self, new_prev):
        self.__prev = new_prev


class Queue:
    def __init__(self):
        self.__head = None
        self.__tail = None
        self.__current = None
        self.__size = 0
        self.__is_shuffled = False
        self.__is_repeat = False
        self.__original_order = [] 

    def getCurrentTrack(self):
        return self.__current.getTrack() if self.__current else None
    def getSize(self):
        return self.__size
    def isEmpty(self):
        return self.__size == 0
    def isShuffled(self):
        return self.__is_shuffled
    def isRepeat(self):
        return self.__is_repeat


    def addTrack(self, track):
        new_node = Node(track)
        
        if self.__head is None:
            self.__head = new_node
            self.__tail = new_node
            self.__current = new_node
        else:
            self.__tail.setNext(new_node)
            new_node.setPrev(self.__tail)
            self.__tail = new_node
        
        self.__size += 1
        if not self.__is_shuffled:
            self.__original_order.append(track)
    

    def addPlaylist(self, playlist):
        for track in playlist.getTracks():
            self.addTrack(track)
    

    def nextTrack(self):
        if self.__current is None:
            return None
        
        if self.__is_repeat and self.__current == self.__tail:
            self.__current = self.__head
        else:
            self.__current = self.__current.getNext()
        
        return self.getCurrentTrack()
    

    def previousTrack(self):
        if self.__current is None:
            return None
        
        if self.__is_repeat and self.__current == self.__head:
            self.__current = self.__tail
        else:
            self.__current = self.__current.getPrev()
        
        return self.getCurrentTrack()
    

    def removeCurrentTrack(self):
        if self.__current is None:
            return False
        
        current_node = self.__current
        prev_node = current_node.getPrev()
        next_node = current_node.getNext()
        
        # Update links
        if prev_node:
            prev_node.setNext(next_node)
        else:  # Removing head
            self.__head = next_node
        
        if next_node:
            next_node.setPrev(prev_node)
        else:  # Removing tail
            self.__tail = prev_node
        
        # Update current pointer
        if next_node:
            self.__current = next_node
        elif prev_node:
            self.__current = prev_node
        else:  # Queue is now empty
            self.__current = None
        
        self.__size -= 1
        return True


    def shuffle(self):
        if self.__is_shuffled or self.__size <= 1:
            return
        
        current_track = self.getCurrentTrack()
        tracks = []
        current = self.__head
        while current:
            tracks.append(current.getTrack())
            current = current.getNext()
        
        import random
        random.shuffle(tracks)
        
        self.__head = None
        self.__tail = None
        self.__size = 0
        
        for track in tracks:
            self.addTrack(track)
        
        self.__setCurrentByTrack(current_track)
        self.__is_shuffled = True
    
    def unshuffle(self):
        if not self.__is_shuffled:
            return
        
        current_track = self.getCurrentTrack()
        
        self.__head = None
        self.__tail = None
        self.__size = 0
        
        for track in self.__original_order:
            self.addTrack(track)
        
        self.__setCurrentByTrack(current_track)
        self.__is_shuffled = False
    
    def enableRepeat(self):
        self.__is_repeat = True
    
    def disableRepeat(self):
        self.__is_repeat = False

    def __setCurrentByTrack(self, track):
        """Set current pointer to node containing specific track"""
        current = self.__head
        while current:
            if current.getTrack() == track:
                self.__current = current
                break
            current = current.getNext()

    def getTracksPage(self, page=1, tracks_per_page=10):
        """Get paginated list of tracks for display"""
        start_idx = (page - 1) * tracks_per_page
        end_idx = start_idx + tracks_per_page
        
        tracks = []
        current = self.__head
        index = 0
        
        while current and index < end_idx:
            if index >= start_idx:
                tracks.append(current.getTrack())
            current = current.getNext()
            index += 1
        
        total_pages = (self.__size + tracks_per_page - 1) // tracks_per_page
        return tracks, page, total_pages

    def store_dict(self):
        tracks_data = []
        current = self.__head
        while current:
            tracks_data.append(current.getTrack().store_dict())
            current = current.getNext()
        
        current_track_data = self.__current.getTrack().store_dict() if self.__current else None
        
        return {
            'tracks': tracks_data,
            'current_track': current_track_data,
            'is_shuffled': self.__is_shuffled,
            'is_repeat': self.__is_repeat,
            'original_order': [track.store_dict() for track in self.__original_order]
        }
    
    @classmethod
    def fetch_dict(cls, data):
        queue = cls()
        
        for track_data in data['tracks']:
            track = Track.fetch_dict(track_data)
            queue.addTrack(track)
        
        queue.__is_shuffled = data['is_shuffled']
        queue.__is_repeat = data['is_repeat']
        
        # Restore original order
        queue.__original_order = [Track.fetch_dict(track_data) for track_data in data['original_order']]
        
        # Restore current track
        if data['current_track']:
            current_track = Track.fetch_dict(data['current_track'])
            queue.__setCurrentByTrack(current_track)
        
        return queue