#MAIN Class

from Track import Track
from Library import MusicLibrary
from Playlist import Playlist
from Util_Jason import load, save
from Duration import total_duration
from Queues import Queue
from Sorting import merge_sort
from Pagination import Pagination

class main:
    def __init__(self):
        self.library = MusicLibrary()
        self.playlist = Playlist()
        self.data = load()
        self.queue = Queue()
        
        # Try to load saved queue state
        if self.queue.load_state():
            print("\n" + "=" * 60)
            print("Previous queue session restored!".center(60))
            print("=" * 60)

    @staticmethod
    def prompt(args: str) -> str:
        return input(args).lower()

    def banner(self, title):
        print("\n" + "╔" * 60)
        print(title.center(60))
        print("╔" * 60)

    def main(self):
        while True:
            self.banner("WELCOME")
            print("Press [M] to Open Music Player".center(60))
            print("╔" * 60)

            print("MAIN MENU")
            print("-" * 45)
            print("  1 → Create New Track")
            print("  2 → View All Tracks")
            print("  3 → Delete Track")
            print("  4 → Create Playlist")
            print("  5 → View All Playlists")
            print("  0 → Exit Program")
            print("-" * 45)

            choice = main.prompt("Enter choice: ")

            if choice == "m":
                while True:
                    self.banner("MUSIC PLAYER")
                    
                    # Check if queue exists from previous session
                    if self.queue.size > 0:
                        print("R → Resume Previous Queue")
                    
                    print("1 → Play Music From Library (All Tracks)")
                    print("2 → Play Music From Playlist")
                    print("3 → Clear Queue")
                    print("0 → Return to Main Menu")

                    choice = main.prompt("Enter choice: ")
                    
                    if choice == 'r' and self.queue.size > 0:
                        # Resume existing queue
                        print(f"\nResuming: {self.queue.current_play()}\n")
                        
                        while True:
                            print(f"Shuffle: {self.queue.shuffle_status()} | Repeat: {self.queue.repeat_status()}\n")
                            print(self.queue)
                            print("\nOPTIONS:")
                            print("  N → Next Track")
                            print("  P → Previous Track")
                            print("  1 → Playback Settings (Shuffle / Repeat)")
                            print("  2 → Exit Player")

                            choice = main.prompt("Enter choice: ")

                            if choice == '2': 
                                break
                            elif choice == 'n':
                                track = self.queue.next()
                                if isinstance(track, dict):
                                    print(f"NOW PLAYING: {self.queue.current_play()}")
                                else:
                                    print(track)
                            elif choice == 'p':
                                track = self.queue.prev()
                                if isinstance(track, dict):
                                    print(f"NOW PLAYING: {self.queue.current_play()}")
                                else:
                                    print(track)
                            elif choice == '1':
                                print("\nPlayback Options:")
                                print("  1 → Toggle Shuffle")
                                print("  2 → Toggle Repeat")
                                opt = main.prompt("Choose: ")
                                if opt == '1': 
                                    self.queue.toggle_shuffle()
                                    print(f"Shuffle: {self.queue.shuffle_status()}")
                                elif opt == '2': 
                                    self.queue.toggle_repeat()
                                    print(f"Repeat: {self.queue.repeat_status()}")

                    elif choice == '1':
                        try:
                            self.data = load()
                            tracks = merge_sort(self.data["Tracks"][:], "title")
                            self.queue = Queue()  # Create new queue

                            self.banner("PLAYING FROM LIBRARY")
                            print(f"Total Duration: {total_duration(self.data, 'Tracks')}\n")

                            for t in tracks:
                                self.queue.enqueue(t)

                            current = self.queue.current_play()
                            print(f"NOW PLAYING: {current}\n")

                            while True:
                                print(f"Shuffle: {self.queue.shuffle_status()} | Repeat: {self.queue.repeat_status()}\n")
                                print(self.queue)
                                print("\nOPTIONS:")
                                print("  N → Next Track")
                                print("  P → Previous Track")
                                print("  1 → Playback Settings (Shuffle / Repeat)")
                                print("  2 → Exit Player")

                                choice = main.prompt("Enter choice: ")

                                if choice == '2': 
                                    break
                                elif choice == 'n':
                                    track = self.queue.next()
                                    if isinstance(track, dict):
                                        print(f"NOW PLAYING: {self.queue.current_play()}")
                                    else:
                                        print(track)
                                elif choice == 'p':
                                    track = self.queue.prev()
                                    if isinstance(track, dict):
                                        print(f"NOW PLAYING: {self.queue.current_play()}")
                                    else:
                                        print(track)
                                elif choice == '1':
                                    print("\nPlayback Options:")
                                    print("  1 → Toggle Shuffle")
                                    print("  2 → Toggle Repeat")
                                    opt = main.prompt("Choose: ")
                                    if opt == '1': 
                                        self.queue.toggle_shuffle()
                                        print(f"Shuffle: {self.queue.shuffle_status()}")
                                    elif opt == '2': 
                                        self.queue.toggle_repeat()
                                        print(f"Repeat: {self.queue.repeat_status()}")

                        except Exception as e:
                            print(f"Error: {e}")
                            if main.prompt("Try again? (y/n): ") != 'y': 
                                break

                    elif choice == '2':
                        self.banner("PLAYING FROM PLAYLIST")
                        print("Select a playlist:\n")

                        self.playlist.displayPlaylists()
                        print("0 → Go Back")

                        try:
                            playlist_choice = int(main.prompt("Enter number: "))
                            self.playlist.updatePlaylistList()

                            if playlist_choice == 0:
                                continue
                            if playlist_choice < 0 or playlist_choice > len(self.playlist.list):
                                print("Invalid playlist number.")
                                continue

                            playlist_name = self.playlist.list[playlist_choice - 1]
                            playlist_tracks = []

                            for playlist in self.playlist.data["Playlists"]:
                                if playlist_name in playlist:
                                    playlist_tracks = playlist[playlist_name]
                                    break

                            if not playlist_tracks:
                                print("This playlist has no tracks.")
                                continue

                            sorted_tracks = merge_sort(playlist_tracks, key="title")
                            self.queue = Queue()  # Create new queue
                            self.queue.enqueue_playlist(sorted_tracks)

                            print(f"NOW PLAYING FROM: {playlist_name}\n")
                            print(f"NOW PLAYING: {self.queue.current_play()}\n")

                            while True:
                                print(f"Shuffle: {self.queue.shuffle_status()} | Repeat: {self.queue.repeat_status()}\n")
                                print(self.queue.display())

                                print("\nOPTIONS:")
                                print("  N → Next Track")
                                print("  P → Previous Track")
                                print("  1 → Playback Options")
                                print("  2 → Exit Player")

                                choice = main.prompt("Choose: ")

                                if choice == 'n':
                                    track = self.queue.next()
                                    if isinstance(track, dict):
                                        print(f"NOW PLAYING: {self.queue.current_play()}")
                                    else:
                                        print(track)
                                elif choice == 'p':
                                    track = self.queue.prev()
                                    if isinstance(track, dict):
                                        print(f"NOW PLAYING: {self.queue.current_play()}")
                                    else:
                                        print(track)
                                elif choice == '1':
                                    print("1 → Toggle Shuffle\n2 → Toggle Repeat")
                                    opt = main.prompt("Choose: ")
                                    if opt == '1': 
                                        self.queue.toggle_shuffle()
                                        print(f"Shuffle: {self.queue.shuffle_status()}")
                                    elif opt == '2': 
                                        self.queue.toggle_repeat()
                                        print(f"Repeat: {self.queue.repeat_status()}")
                                elif choice == '2': 
                                    break

                        except ValueError:
                            print("Invalid input. Enter a valid number.")
                    
                    elif choice == '3':
                        # Clear queue
                        confirm = input("Clear queue? All data will be lost. (y/n): ").lower()
                        if confirm == 'y':
                            self.queue.clear_queue()
                            print("\nQueue cleared successfully!")
                    
                    elif choice == '0': 
                        break

            elif choice == '1':
                self.library.createTrack()
                self.data = load()

            elif choice == '2':
                self.banner("MUSIC LIBRARY")
                print(f"Total Duration: {self.library.getTotalDuration()}\n")
                self.library.displayTracks()

            elif choice == '3':
                self.banner("DELETE TRACK")
                self.library.deleteTrack()
                self.data = load()

            elif choice == '4':
                self.playlist.createPlaylist()

            elif choice == '5':
                while True:
                    self.banner("PLAYLIST MANAGER")
                    print("\nV → View All Playlists (Paginated)")
                    print("A → Add Tracks to Playlist")
                    print("R → Remove Track from Playlist")
                    print("D → Delete Playlist")
                    print("S → Select Playlist to View Tracks")
                    print("E → Exit to Main Menu")

                    choice = main.prompt("Choose: ")

                    if choice == 'v':
                        self.playlist.displayPlaylists(with_pagination=True)
                    
                    elif choice == 's':
                        print("\nSelect a playlist:")
                        self.playlist.displayPlaylists()
                        try:
                            index = int(input("Enter number: "))
                            self.playlist.displayTracks(index)
                        except:
                            print("Invalid selection.")
                    
                    elif choice == 'r':
                        print("\nSelect a playlist:")
                        self.playlist.displayPlaylists()
                        try:
                            idx = int(input("Enter number: ")) - 1
                            if idx < 0 or idx >= len(self.playlist.list):
                                print("Invalid playlist.")
                                continue
                            playlist_name = self.playlist.list[idx]
                            self.playlist.removeTrackFromPlaylist(playlist_name)
                        except ValueError:
                            print("Invalid input.")
                    
                    elif choice == 'd':
                        self.playlist.deletePlaylist()
                    
                    elif choice == 'a':
                        print("\nSelect a playlist:")
                        self.playlist.displayPlaylists()
                        try:
                            idx = int(input("Enter number: ")) - 1
                            if idx < 0 or idx >= len(self.playlist.list): 
                                raise ValueError
                            playlist_name = self.playlist.list[idx]
                        except ValueError:
                            print("Invalid playlist.")
                            continue

                        while True:
                            print("\n1 → Add From All Tracks")
                            print("2 → Search Tracks")
                            print("0 → Cancel")
                            
                            choice_input = input("Choose: ").strip()
                            
                            if not choice_input:
                                print("Invalid input. Please enter a valid choice.")
                                continue
                            
                            try:
                                opt = int(choice_input)
                                if opt == 1:
                                    self.playlist.addTrack(playlist_name)
                                    break
                                elif opt == 2:
                                    query = input("Search: ").strip()
                                    if not query:
                                        print("Search query cannot be empty.")
                                        continue
                                    matches = self.playlist.searchTrack(query)
                                    if matches is None:
                                        # User cancelled search
                                        break
                                    if not matches:
                                        print("No matching tracks.")
                                        continue
                                    
                                    print("\n1 → Add One")
                                    print("2 → Add All")
                                    print("0 → Cancel")
                                    
                                    sub_input = input("Choose: ").strip()
                                    if not sub_input:
                                        print("Invalid input. Please enter a valid choice.")
                                        continue
                                    
                                    sub = int(sub_input)
                                    result = self.playlist.searchedTracks(sub, playlist_name, matches)
                                    if result or sub == 0:
                                        break
                                elif opt == 0:
                                    print("Operation cancelled.")
                                    break
                                else:
                                    print("Invalid option. Please choose 1, 2, or 0.")
                            except ValueError:
                                print("Invalid input. Please enter a number.")

                    elif choice == 'e': 
                        break
                    else:
                        try:
                            index = int(choice)
                            self.playlist.displayTracks(index)
                        except:
                            print("Invalid selection.")

            elif choice == '0':
                print("Goodbye!")
                break

if __name__ == "__main__":
    run = main()
    run.main()
