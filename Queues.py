from Duration import sec_to_min
from Util_Jason import save_queue, load_queue
import random

class Node:
    def __init__(self, track=None):
        self.track = track
        self.next = None
        self.prev = None

class Queue:
    def __init__(self):
        self.front = self.rear = self.current = None
        self.size = 0
        self.shuffle_ = self.repeat_ = self.playing_ = False
        self.queuelist = []

    def save_state(self):
        """Save queue state to JSON"""
        if self.size == 0:
            save_queue(None)
            return
        
        current_index = next((i for i, node in enumerate(self.queuelist) if node == self.current), None)
        save_queue({
            "tracks": [node.track for node in self.queuelist],
            "current_index": current_index,
            "shuffle": self.shuffle_,
            "repeat": self.repeat_,
            "playing": self.playing_
        })

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
            self.front = self.rear = self.current = new_node
            new_node.next = new_node.prev = new_node
        else:
            new_node.next = self.front
            new_node.prev = self.rear
            self.rear.next = self.front.prev = new_node
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
        
        # Store next node before removing
        next_node = self.front.next
        
        self.queuelist.remove(self.front)
        self.front.prev.next = self.front.next
        self.front.next.prev = self.front.prev
        
        if self.current == self.front:
            self.current = next_node
        
        self.front = next_node
        self.size -= 1
        self.save_state()
        return removed_track

    def remove_current(self):
        """Remove the currently playing track"""
        if self.size == 0 or not self.current:
            return None
        
        removed_track = self.current.track
        if self.size == 1:
            self.__init__()
            self.save_state()
            return removed_track
        
        self.queuelist.remove(self.current)
        self.current.prev.next = self.current.next
        self.current.next.prev = self.current.prev
        
        if self.current == self.front:
            self.front = self.current.next
        if self.current == self.rear:
            self.rear = self.current.prev
        
        self.size -= 1
        self.save_state()
        return removed_track

    def current_play(self):
        """Return formatted string of currently playing track"""
        if self.size == 0 or not self.current:
            return "No track is currently playing."
        track = self.current.track
        feat = f" (ft. {track.get('featured_artist', '')})" if track.get('featured_artist') else ""
        return f"{track['title']}{feat} by {track['artist']} ({sec_to_min(track['duration'])})"

    def next(self):
        """Move to next track and remove the current one (FIFO)"""
        if self.size == 0:
            return "Queue is empty. No tracks to play."

        if self.shuffle_:
            if self.current:
                self.remove_current()
            if self.size > 0:
                self.current = self.queuelist[random.randint(0, self.size - 1)]
                return self.current.track
            return "Queue is now empty."

        if self.current:
            self.dequeue()
            if self.size > 0:
                self.current = self.front
                self.save_state()
                return self.current.track
            return "Queue is now empty."
        
        self.current = self.front
        self.save_state()
        return self.current.track
    
    def prev(self):
        """Move to previous track (not available in FIFO mode)"""
        return "Previous track is not available in FIFO mode. Tracks are removed after playing."

    def toggle_playing(self):
        self.playing_ = not self.playing_
        self.save_state()
        return self.playing_
    
    def playing_status(self):
        return "Playing" if self.playing_ else "Paused"

    def toggle_shuffle(self):
        self.shuffle_ = not self.shuffle_
        self.save_state()
        return self.shuffle_
    
    def shuffle_status(self):
        return "ON" if self.shuffle_ else "OFF"

    def toggle_repeat(self):
        self.repeat_ = not self.repeat_
        self.save_state()
        return self.repeat_

    def repeat_status(self):
        return "ON" if self.repeat_ else "OFF"
    
    def clear_queue(self):
        self.__init__()
        save_queue(None)

    def display(self):
        """Display queue tracks as string"""
        if self.size == 0:
            return ""
        
        tracks = ["Tracks:"]
        for i, node in enumerate(self.queuelist, 1):
            is_current = " ▶" if node == self.current else ""
            feat = f" (ft. {node.track.get('featured_artist', '')})" if node.track.get('featured_artist') else ""
            tracks.append(f"    [{i}] {node.track['title']}{feat} by {node.track['artist']} - "
                         f"{node.track['album']} ({sec_to_min(node.track['duration'])}){is_current}")
        return '\n'.join(tracks)

    def __str__(self):
        if self.size == 0:
            return "Queue is empty."
        
        lines = ["Tracks:"]
        current = self.front
        for i in range(self.size):
            track = current.track
            is_current = " ▶" if current == self.current else ""
            feat = f" (ft. {track.get('featured_artist', '')})" if track.get('featured_artist') else ""
            lines.append(f"\t[{i + 1}] {track['title']}{feat} by {track['artist']} - "
                        f"{track['album']} ({sec_to_min(track['duration'])}){is_current}")
            current = current.next
        return '\n'.join(lines)
