# MAIN Class 

from Track import Track
from Library import MusicLibrary  
from Playlist import Playlist  
from Util_Jason import load, save  
from Duration import total_duration, sec_to_min, format_duration  
from Queues import Queue  
from Sorting import merge_sort  


class main:
    def __init__(self):
        self.library = MusicLibrary()
        self.playlist = Playlist()
        self.data = load()

    @staticmethod
    def prompt(args: str) -> str:
        return input(args).lower()

    def banner(self, title):
        print("\n" + "═" * 60)
        print(title.center(60))
        print("═" * 60)

    def main(self):
        while True:
            self.banner("WELCOME")
            print("Press [M] to Open Music Player".center(60))
            print("═" * 60)

            print("MAIN MENU")
            print("-" * 45)
            print("  1 → Create New Track")
            print("  2 → View All Tracks")
            print("  3 → Create Playlist")
            print("  4 → View All Playlists")
            print("  0 → Exit Program")
            print("-" * 45)

            choice = main.prompt("Enter choice: ")

            if choice == "m":
                while True:
                    self.banner("MUSIC PLAYER")
                    print("1 → Play Music From Library (All Tracks)")
                    print("2 → Play Music From Playlist")
                    print("0 → Return to Main Menu")

                    choice = main.prompt("Enter choice: ")

                    if choice == '1':
                        while True:
                            try:
                                self.data = load()
                                tracks = merge_sort(self.data["Tracks"][:], "title")
                                queue = Queue()

                                self.banner("PLAYING FROM LIBRARY")
                                print(f"Total Duration: {total_duration(self.data, 'Tracks')}\n")

                                for t in tracks:
                                    queue.enqueue(t)

                                current = queue.current_play()
                                print(f"NOW PLAYING: {current}\n")

                                while True:
                                    print(f"Shuffle: {queue.shuffle_status()} | Repeat: {queue.repeat_status()}\n")
                                    print(queue)
                                    print("\nOPTIONS:")
                                    print("  N → Next Track")
                                    print("  P → Previous Track")
                                    print("  1 → Playback Settings (Shuffle / Repeat)")
                                    print("  2 → Exit Player")

                                    choice = main.prompt("Enter choice: ")

                                    if choice == '2': 
                                        break
                                    elif choice == 'n':
                                        queue.next()
                                        print(f"NOW PLAYING: {queue.current_play()}")
                                    elif choice == 'p':
                                        queue.prev()
                                        print(f"NOW PLAYING: {queue.current_play()}")
                                    elif choice == '1':
                                        print("\nPlayback Options:")
                                        print("  1 → Toggle Shuffle")
                                        print("  2 → Toggle Repeat")
                                        opt = main.prompt("Choose: ")
                                        if opt == '1': 
                                            queue.toggle_shuffle()
                                        elif opt == '2': 
                                            queue.toggle_repeat()

                            except Exception as e:
                                print(f"Error: {e}")
                                if main.prompt("Try again? (y/n): ") != 'y': 
                                    break
                            break

                    elif choice == '2':
                        queue = Queue()
                        self.banner("PLAYING FROM PLAYLIST")
                        print("Select a playlist:\n")

                        self.playlist.displayPlaylists()
                        print("0 → Go Back")

                        try:
                            playlist_choice = int(main.prompt("Enter number: "))
                            self.playlist.updatePlaylistList()

                            if playlist_choice == 0:
                                break
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
                            queue.enqueue_playlist(sorted_tracks)

                            print(f"NOW PLAYING FROM: {playlist_name}\n")
                            print(f"NOW PLAYING: {queue.current_play()}\n")

                            while True:
                                print(f"Shuffle: {queue.shuffle_status()} | Repeat: {queue.repeat_status()}\n")
                                print(queue.display())

                                print("\nOPTIONS:")
                                print("  N → Next Track")
                                print("  P → Previous Track")
                                print("  1 → Playback Options")
                                print("  2 → Exit Player")

                                choice = main.prompt("Choose: ")

                                if choice == 'n':
                                    queue.next()
                                    print(f"NOW PLAYING: {queue.current_play()}")
                                elif choice == 'p':
                                    queue.prev()
                                    print(f"NOW PLAYING: {queue.current_play()}")
                                elif choice == '1':
                                    print("1 → Toggle Shuffle\n2 → Toggle Repeat")
                                    opt = main.prompt("Choose: ")
                                    if opt == '1': 
                                        queue.toggle_shuffle()
                                    elif opt == '2': 
                                        queue.toggle_repeat()
                                elif choice == '2': 
                                    break

                        except ValueError:
                            print("Invalid input. Enter a valid number.")

                    elif choice == '0': 
                        break

            elif choice == '1':
                self.library.createTrack()
                self.data = load()

            elif choice == '2':
                self.banner("MUSIC LIBRARY")
                print(f"Total Duration: {self.library.getTotalDuration()}\n")
                self.library.displayTracks()
                input("\nPress Enter to continue...")

            elif choice == '3':
                self.playlist.createPlaylist()

            elif choice == '4':
                while True:
                    self.banner("PLAYLIST MANAGER")
                    self.data = load()
                    
                    if "Playlists" not in self.data or not self.data["Playlists"]:
                        print("No playlists available.")
                        print("\nE → Exit to Main Menu")
                        choice = main.prompt("Choose: ")
                        if choice == 'e': 
                            break
                        continue
                    
                    print("Available Playlists:\n")
                    
                    # Display each playlist with its tracks and duration
                    counter = 1
                    self.playlist.updatePlaylistList()
                    
                    for playlist_dict in self.data["Playlists"]:
                        for playlist_name, tracks in playlist_dict.items():
                            # Calculate duration for this playlist
                            playlist_duration = total_duration(tracks)
                            track_count = len(tracks)
                            
                            print(f"  [{counter}] {playlist_name}")
                            print(f"      Duration: {playlist_duration} | Tracks: {track_count}")
                            
                            if tracks:
                                # Sort and display tracks
                                sorted_tracks = merge_sort(tracks[:], key="title")
                                for idx, track in enumerate(sorted_tracks, 1):
                                    print(f"      {idx}. {track['title']} by {track['artist']} ({sec_to_min(track['duration'])})")
                            else:
                                print("      (No tracks)")
                            print()
                            counter += 1
                    
                    print("-" * 60)
                    print("A → Add Tracks to Playlist")
                    print("E → Exit to Main Menu")

                    choice = main.prompt("Choose: ")

                    if choice == 'a':
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
                            print("\n1 → Add From All Tracks\n2 → Search Tracks")
                            try:
                                opt = int(input("Choose: "))
                                if opt == 1:
                                    self.playlist.addTrack(playlist_name)
                                    break
                                elif opt == 2:
                                    query = input("Search: ")
                                    matches = self.playlist.searchTrack(query)
                                    if not matches:
                                        print("No matching tracks.")
                                        break
                                    print("1 → Add One\n2 → Add All")
                                    sub = int(input("Choose: "))
                                    self.playlist.searchedTracks(sub, playlist_name, matches)
                                    break
                            except ValueError:
                                print("Invalid input.")

                    elif choice == 'e': 
                        break
                    else:
                        print("Invalid selection.")

            elif choice == '0':
                print("Goodbye!")
                break


if __name__ == "__main__":
    run = main()
    run.main()
