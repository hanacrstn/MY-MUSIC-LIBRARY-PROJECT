
#MAIN CLASS

from Track import Track
from Playlist import Playlist
from Queues import Queue

class MusicLibrary:
    def __init__(self):
        self.__tracks = []
        self.__playlists = []
        self.__queue = Queue()
        self.__load_data()
    
    # Getter methods
    def getAllTracks(self):
        return self.__tracks.copy()
    
    def getAllPlaylists(self):
        return self.__playlists.copy()
    
    def getQueue(self):
        return self.__queue
    
    def getPlaylistByName(self, name):
        for playlist in self.__playlists:
            if playlist.getName() == name:
                return playlist
        return None
    
    # Track management
    def addTrack(self, title, artist, feat, album, duration):
        new_track = Track(title, artist, feat, album, duration)
        self.__tracks.append(new_track)
        self.__sort_tracks()
        self.__save_data()
        return new_track
    
    def searchTracks(self, query):
        results = []
        for track in self.__tracks:
            if (query.lower() in track.getTitle().lower() or 
                query.lower() in track.getArtist().lower() or
                query.lower() in track.getAlbum().lower()):
                results.append(track)
        return results
    
    # Playlist management
    def createPlaylist(self, name):
        # Check for duplicate names
        for playlist in self.__playlists:
            if playlist.getName() == name:
                return None
        
        new_playlist = Playlist(name)
        self.__playlists.append(new_playlist)
        self.__save_data()
        return new_playlist
    
    def deletePlaylist(self, playlist):
        if playlist in self.__playlists:
            self.__playlists.remove(playlist)
            self.__save_data()
            return True
        return False
    
    # Private helper methods
    def __sort_tracks(self):
        self.__tracks.sort(key=lambda track: (
            track.getTitle(),
            track.getArtist(),
            track.getAlbum(),
            track.getDuration()
        ))
    
    # Data persistence
    def __load_data(self):
        try:
            with open('music_data.json', 'r') as f:
                import json
                data = json.load(f)
                
                self.__tracks = [Track.fetch_dict(track_data) for track_data in data['tracks']]
                self.__playlists = [Playlist.fetch_dict(playlist_data) for playlist_data in data['playlists']]
                self.__queue = Queue.fetch_dict(data['queue'])
                
        except FileNotFoundError:
            # First run, initialize empty
            self.__tracks = []
            self.__playlists = []
            self.__queue = Queue()
    
    def __save_data(self):
        data = {
            'tracks': [track.store_dict() for track in self.__tracks],
            'playlists': [playlist.store_dict() for playlist in self.__playlists],
            'queue': self.__queue.store_dict()
        }
        
        with open('music_data.json', 'w') as f:
            import json
            json.dump(data, f, indent=2)


"""
def main_menu():
    while True:
        print("\tMAIN MENU")
        print("[1] Music Player")
        print("[2] Add New Track")
        print("[3] View All Tracks")
        print("[4] Create Playlist")
        print("[5] Exit")
        try:
            choose = int(input("Choose operation(1-5): "))
            if choose == 1:
                while True:
                    print("\tMUSIC PLAYER")
                    print("[1] Music Library")
                    print("[2] Playlist")
                    print("[3] Go back")
                    try:
                        operation = int(input("Choose operation(1-3): "))
                        if operation == 1:
                            print("\tMUSIC LIBRARY")
                            print()
                            pass
                        elif operation == 2:
                            print("\tPLAYLIST")
                            print()
                            pass
                        elif operation == 3:
                            break
                        else:
                             print("Invalid input!")
                    except Exception as e:
                        print("Invalid input!")
                        print()
    
            elif choose == 2:
                print("\tADD NEW TRACKS")
                print()
                pass
            elif choose == 3:
                print("\tVIEW ALL TRACKS")
                print()
                pass
            elif choose == 4:
                print("\tCREATE PLAYLIST")
                print()
                pass
            elif choose == 5:
                print("Goodbye...")
                break
            else:
                print("Invalid input!")
        
        except Exception as e:
            print("Invalid input")
            print()
main_menu()
"""