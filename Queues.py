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
        
        current_index = None
        if self.current:
            for i, node in enumerate(self.queuelist):
                if node == self.current:
                    current_index = i
                    break
        
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
        
        self.__init__()
        
        for track in state["tracks"]:
            self.enqueue(track, save=False)
        
        if state["current_index"] is not None and state["current_index"] < len(self.queuelist):
            self.current = self.queuelist[state["current_index"]]
        
        self.shuffle_ = state.get("shuffle", False)
        self.repeat_ = state.get("repeat", False)
        self.playing_ = state.get("playing", False)
        
        self.save_state()
        return True

    def enqueue(self, track, save=True):
        """Add track to queue"""
        new_node = Node(track)
        if self.size == 0:
            self.front = self.rear = new_node
            new_node.next = new_node
            new_node.prev = new_node
            self.current = new_node
        else:
            new_node.next = self.front
            new_node.prev = self.rear
            self.rear.next = new_node
            self.front.prev = new_node
            self.rear = new_node
        
        self.size += 1
        self.queuelist.append(new_node)
        
        if save:
            self.save_state()
        return True
    
    def enqueue_playlist(self, playlist_tracks):
        """Add multiple tracks from playlist"""
        for track in playlist_tracks:
            self.enqueue(track, save=False)
        self.save_state()

    def dequeue(self):
        """Remove and return the front track (FIFO)"""
        if self.size == 0:
            return None
        
        removed_track = self.front.track
        
        if self.size == 1:
            self.__init__()
            self.save_state()
            return removed_track
        
        # Remove front node
        next_node = self.front.next
        prev_node = self.front.prev
        
        # Remove from queuelist
        self.queuelist.remove(self.front)
        
        # Update circular linked list pointers
        prev_node.next = next_node
        next_node.prev = prev_node
        
        # Update front pointer
        self.front = next_node
        
        # Update current if it was pointing to removed node
        if self.current == self.front:
            self.current = self.front
        
        self.size -= 1
        self.save_state()
        
        return removed_track

    def remove_current(self):
        """Remove the currently playing track (used for shuffle mode)"""
        if self.size == 0 or self.current is None:
            return None
        
        removed_track = self.current.track
        
        if self.size == 1:
            self.__init__()
            self.save_state()
            return removed_track
        
        # Store adjacent nodes
        next_node = self.current.next
        prev_node = self.current.prev
        
        # Remove from queuelist
        self.queuelist.remove(self.current)
        
        # Update circular linked list pointers
        prev_node.next = next_node
        next_node.prev = prev_node
        
        # Update front and rear if needed
        if self.current == self.front:
            self.front = next_node
        if self.current == self.rear:
            self.rear = prev_node
        
        self.size -= 1
        self.save_state()
        
        return removed_track

    def current_play(self):
        """Return formatted string of currently playing track"""
        if self.size == 0 or self.current is None:
            return "No track is currently playing."
        track = self.current.track
        feat = f" (ft. {track.get('featured_artist', '')})" if track.get('featured_artist') else ""
        return f"{track['title']}{feat} by {track['artist']} ({sec_to_min(track['duration'])})"

    def next(self):
        """Move to next track and remove the current one (FIFO)"""
        if self.size == 0:
            return "Queue is empty. No tracks to play."

        if self.shuffle_:
            # In shuffle mode, remove the current track and play random
            if self.current:
                self.remove_current()
            if self.size > 0:
                random_index = random.randint(0, self.size - 1)
                self.current = self.queuelist[random_index]
                return self.current.track
            else:
                return "Queue is now empty."

        # Standard FIFO: Remove current track and play next
        if self.current:
            removed = self.dequeue()
            if self.size > 0:
                self.current = self.front
                self.save_state()
                return self.current.track
            else:
                return "Queue is now empty."
        else:
            self.current = self.front
            self.save_state()
            return self.current.track
    
    def prev(self):
        """Move to previous track (not available in FIFO mode)"""
        return "Previous track is not available in FIFO mode. Tracks are removed after playing."

    def toggle_playing(self):
        """Toggle play/pause state"""
        self.playing_ = not self.playing_
        self.save_state()
        return self.playing_
    
    def playing_status(self):
        """Return playing status string"""
        return "Playing" if self.playing_ else "Paused"       

    def toggle_shuffle(self):
        """Toggle shuffle mode"""
        self.shuffle_ = not self.shuffle_
        self.save_state()
        return self.shuffle_
    
    def shuffle_status(self):
        """Return shuffle status string"""
        return "ON" if self.shuffle_ else "OFF"        

    def toggle_repeat(self):
        """Toggle repeat mode"""
        self.repeat_ = not self.repeat_
        self.save_state()
        return self.repeat_

    def repeat_status(self):
        """Return repeat status string"""
        return "ON" if self.repeat_ else "OFF"  
    
    def clear_queue(self):
        """Clear queue and delete saved state"""
        self.__init__()
        save_queue(None)

    def display(self):
        """Display queue tracks as string"""
        tracks = []
        if self.size > 0:
            tracks.append("Tracks:")
            temp = self.front
            index = 1
            for _ in range(self.size):
                is_current = " ▶" if temp == self.current else ""
                feat = f" (ft. {temp.track.get('featured_artist', '')})" if temp.track.get('featured_artist') else ""
                tracks.append(f"    [{index}] {temp.track['title']}{feat} by {temp.track['artist']} - {temp.track['album']} ({sec_to_min(temp.track['duration'])}){is_current}")
                temp = temp.next
                index += 1
        return '\n'.join(tracks)

    def __str__(self):
        """String representation of queue"""
        if self.size == 0:
            return "Queue is empty."

        queue = "Tracks:\n"  
        current = self.front
        for i in range(self.size):
            track = current.track
            is_current = " ▶" if current == self.current else ""
            feat = f" (ft. {track.get('featured_artist', '')})" if track.get('featured_artist') else ""
            queue += f"\t[{i + 1}] {track['title']}{feat} by {track['artist']} - {track['album']} ({sec_to_min(track['duration'])}){is_current}\n"
            current = current.next 

        return queue.strip()
