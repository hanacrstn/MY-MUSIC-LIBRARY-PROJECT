from Duration import sec_to_min
from Track import Track
from Pagination import Pagination  
import random

class Node:
    def __init__(self, track=None):
        self.track = track
        self.next = None 

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

    def enqueue(self, track):
        new_node = Node(track)
        if self.size == 0:
            self.front = self.rear = new_node
            new_node.next = new_node 
        else:
            self.rear.next = new_node
            self.rear = new_node
            self.rear.next = self.front  
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
        if self.size == 0:
            return "Queue is empty. No tracks to play."

        if self.shuffle_:
            return self.shuffle()

        if self.current is None:
            self.current = self.front
        else:
            if self.current == self.rear:
                if not self.repeat_:
                    return self.rear.track  
                else:
                    self.current = self.front 
            else:
                self.current = self.current.next 

        return self.current.track
    
    def prev(self):
        if self.size == 0:
            return "Queue is empty. No tracks to play."

        if self.current is None:
            self.current = self.front
        else:
            if self.current == self.front:
                if self.repeat_:
                    self.current = self.rear
                else:
                    return "No previous track. You're at the first track."
            else:
                temp = self.front
                while temp.next != self.current:
                    temp = temp.next
                self.current = temp

        return self.current.track


    def toggle_playing(self):
        self.playing_ = not self.playing_
        return self.playing_
    
    def playing_status(self):
        return "Playing" if self.playing_ else "Paused"       

    # Shuffle Functions
    def toggle_shuffle(self):
        self.shuffle_ = not self.shuffle_
        return self.shuffle_
    
    def shuffle_status(self):
        return "ON" if self.shuffle_ else "OFF"        

    def shuffle(self):
        if self.size == 0:
            return "Queue is empty. No tracks to play."
        random_index = random.randint(0, self.size - 1)
        self.current = self.queuelist[random_index]
        self.shuffle_ = True
        return self.current.track


    # Repeat Funtions
    def toggle_repeat(self):
        self.repeat_ = not self.repeat_  
        return self.repeat_

    def repeat_status(self):
        return "ON" if self.repeat_ else "OFF"  

    def repeat(self):
        if self.size == 0:
            return "Queue is empty. No tracks to play."
        if self.repeat_ and self.current == self.rear: 
            self.current = self.front  
        return self.current.track

    def display(self):
        tracks = []
        if self.size > 0:
            tracks.append("Tracks:")
            temp = self.front
            index = 1
            while temp != self.rear:
                tracks.append(f"    [{index}] {temp.track['title']} by {temp.track['artist']} - {temp.track['album']} ({sec_to_min(temp.track['duration'])})")
                temp = temp.next
                index += 1
            # Include the rear track
            tracks.append(f"    [{index}] {self.rear.track['title']} by {self.rear.track['artist']} - {self.rear.track['album']} ({sec_to_min(self.rear.track['duration'])})")
        return '\n'.join(tracks)

    
    def __str__(self):
        if self.size == 0:
            return "Queue is empty."

        queue = "Tracks:\n"  
        current = self.front
        for i in range(self.size):
            track = current.track
            queue += f"\t[{(i + 1)}] {track['title']} by {track['artist']} - {track['album']} ({sec_to_min(track['duration'])})\n"
            current = current.next 

        return queue.strip()
