from Duration import sec_to_min
from Track import Track
from Pagination import Pagination  
from Util_Jason import save_queue, load_queue
import random

class Node:
    def __init__(self, track=None):
        self.track = track
        self.next = None
        self.prev = None  

class Queue:
    def __init__(self):
        self.front = None  
        self.rear = None   
        self.current = None  
        self.size = 0
        self.shuffle_ = False
        self.repeat_ = False
        self.playing_ = False
        self.queuelist = []

    def save_state(self):
        """Save queue state to JSON"""
        if self.size == 0:
            save_queue(None)
            return
        
        # Get current track index
        current_index = None
        if self.current:
            for i, node in enumerate(self.queuelist):
                if node == self.current:
                    current_index = i
                    break
        
        # Collect all tracks
        tracks = [node.track for node in self.queuelist]
        
        queue_state = {
            "tracks": tracks,
            "current_index": current_index,
            "shuffle": self.shuffle_,
            "repeat": self.repeat_,
            "playing": self.playing_
        }
        save_queue(queue_state)

    def load_state(self):
        """Load queue state from JSON"""
        state = load_queue()
        if not state:
            return False
        
        # Clear current queue
        self.__init__()
        
        # Rebuild queue
        for track in state["tracks"]:
            self.enqueue(track)
        
        # Restore current position
        if state["current_index"] is not None and state["current_index"] < len(self.queuelist):
            self.current = self.queuelist[state["current_index"]]
        
        # Restore settings
        self.shuffle_ = state.get("shuffle", False)
        self.repeat_ = state.get("repeat", False)
        self.playing_ = state.get("playing", False)
        
        return True

    def enqueue(self, track):
        new_node = Node(track)
        if self.size == 0:
            # First node - points to itself
            self.front = self.rear = new_node
            new_node.next = new_node
            new_node.prev = new_node
            self.current = new_node  # Auto-play first track
        else:
            # Add at the end
            new_node.next = self.front
            new_node.prev = self.rear
            self.rear.next = new_node
            self.front.prev = new_node
            self.rear = new_node
        
        self.size += 1
        self.queuelist.append(new_node)
        return True
    
    def enqueue_playlist(self, playlist_tracks):
        for track in playlist_tracks:
            self.enqueue(track)

    def current_play(self):
        if self.size == 0 or self.current is None:
            return "No track is currently playing."
        track = self.current.track
        return f"{track['title']} by {track['artist']} ({track['duration']})"

    def next(self):
        """O(1) time complexity - uses prev/next pointers"""
        if self.size == 0:
            return "Queue is empty. No tracks to play."

        if self.shuffle_:
            return self.shuffle()

        if self.current is None:
            self.current = self.front
        else:
            if self.current == self.rear:
                # At last track
                if self.repeat_:
                    # Repeat ON - go to first track
                    self.current = self.front
                else:
                    # Repeat OFF - stay at last track
                    return self.rear.track  
            else:
                # Move to next track - O(1)
                self.current = self.current.next

        self.save_state()  # Save after each operation
        return self.current.track
    
    def prev(self):
        """O(1) time complexity - uses prev pointer"""
        if self.size == 0:
            return "Queue is empty. No tracks to play."

        if self.current is None:
            self.current = self.front
        else:
            if self.current == self.front:
                # At first track
                if self.repeat_:
                    # Repeat ON - go to last track
                    self.current = self.rear
                else:
                    # Repeat OFF - stay at first track
                    return "No previous track. You're at the first track."
            else:
                # Move to previous track - O(1) using prev pointer!
                self.current = self.current.prev

        self.save_state()  # Save after each operation
        return self.current.track

    def toggle_playing(self):
        self.playing_ = not self.playing_
        self.save_state()
        return self.playing_
    
    def playing_status(self):
        return "Playing" if self.playing_ else "Paused"       

    # Shuffle Functions
    def toggle_shuffle(self):
        self.shuffle_ = not self.shuffle_
        self.save_state()
        return self.shuffle_
    
    def shuffle_status(self):
        return "ON" if self.shuffle_ else "OFF"        

    def shuffle(self):
        if self.size == 0:
            return "Queue is empty. No tracks to play."
        random_index = random.randint(0, self.size - 1)
        self.current = self.queuelist[random_index]
        self.shuffle_ = True
        self.save_state()
        return self.current.track

    # Repeat Functions
    def toggle_repeat(self):
        self.repeat_ = not self.repeat_
        self.save_state()
        return self.repeat_

    def repeat_status(self):
        return "ON" if self.repeat_ else "OFF"  

    def repeat(self):
        if self.size == 0:
            return "Queue is empty. No tracks to play."
        if self.repeat_ and self.current == self.rear: 
            self.current = self.front  
        return self.current.track
    
    def clear_queue(self):
        """Clear queue and delete saved state"""
        self.__init__()
        save_queue(None)

    def display(self):
        tracks = []
        if self.size > 0:
            tracks.append("Tracks:")
            temp = self.front
            index = 1
            for _ in range(self.size):
                is_current = " ▶" if temp == self.current else ""
                tracks.append(f"    [{index}] {temp.track['title']} by {temp.track['artist']} - {temp.track['album']} ({sec_to_min(temp.track['duration'])}){is_current}")
                temp = temp.next
                index += 1
        return '\n'.join(tracks)

    def __str__(self):
        if self.size == 0:
            return "Queue is empty."

        queue = "Tracks:\n"  
        current = self.front
        for i in range(self.size):
            track = current.track
            is_current = " ▶" if current == self.current else ""
            queue += f"\t[{(i + 1)}] {track['title']} by {track['artist']} - {track['album']} ({sec_to_min(track['duration'])}){is_current}\n"
            current = current.next 

        return queue.strip()
