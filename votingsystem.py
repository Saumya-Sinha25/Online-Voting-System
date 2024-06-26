import os
import tkinter as tk
from tkinter import filedialog
from pygame import mixer

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("500x400")

        mixer.init()

        self.songs_list = tk.Listbox(root, selectmode=tk.SINGLE, bg="lightgray", selectbackground="gray", width=50)
        self.songs_list.pack(pady=10)

        self.add_btn = tk.Button(root, text="➕ Add Songs", command=self.add_songs)
        self.add_btn.pack(pady=5)

        self.add_playlist_btn = tk.Button(root, text="📂 Add Playlist", command=self.add_playlist)
        self.add_playlist_btn.pack(pady=5)

        self.play_btn = tk.Button(root, text="▶️ Play", command=self.play)
        self.play_btn.pack(side=tk.LEFT, padx=5)

        self.pause_btn = tk.Button(root, text="⏸ Pause", command=self.pause)
        self.pause_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = tk.Button(root, text="⏹ Stop", command=self.stop)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        self.next_btn = tk.Button(root, text="➡ Next", command=self.next_song)
        self.next_btn.pack(side=tk.LEFT, padx=5)

        self.prev_btn = tk.Button(root, text="⬅ Previous", command=self.prev_song)
        self.prev_btn.pack(side=tk.LEFT, padx=5)

        self.volume_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume", command=self.set_volume,
                                     troughcolor="#282C35", sliderlength=15, bg="#FFFFFF")
        self.volume_scale.set(70)
        mixer.music.set_volume(0.7)  # Set default volume
        self.volume_scale.pack(pady=5)

        self.bass_scale = tk.Scale(root, from_=-12, to=12, orient=tk.HORIZONTAL, label="Bass", command=self.adjust_bass,
                                   troughcolor="#282C35", sliderlength=15, bg="#FFFFFF")
        self.bass_scale.set(0)
        self.bass_scale.pack(pady=5)

        self.treble_scale = tk.Scale(root, from_=-12, to=12, orient=tk.HORIZONTAL, label="Treble", command=self.adjust_treble,
                                     troughcolor="#282C35", sliderlength=15, bg="#FFFFFF")
        self.treble_scale.set(0)
        self.treble_scale.pack(pady=5)

        self.status_label = tk.Label(root, text="", bg="#282C35", fg="white", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

        self.load_songs()

    def add_songs(self):
        songs = filedialog.askopenfilenames(title="Choose a song", filetypes=[("MP3 Files", "*.mp3")])
        for song in songs:
            self.songs_list.insert(tk.END, song)

    def add_playlist(self):
        playlist = filedialog.askopenfilename(title="Choose a playlist file", filetypes=[("Playlist Files", "*.m3u")])
        if playlist:
            with open(playlist, "r") as file:
                songs = file.read().splitlines()
                for song in songs:
                    self.songs_list.insert(tk.END, song)

    def play(self):
        selected_song = self.songs_list.curselection()
        if selected_song:
            selected_song = int(selected_song[0])
            song_path = self.songs_list.get(selected_song)
            mixer.music.load(song_path)
            mixer.music.play()
            self.update_status(f"Now playing: {os.path.basename(song_path)}")

    def pause(self):
        mixer.music.pause()
        self.update_status("Paused")

    def stop(self):
        mixer.music.stop()
        self.update_status("Stopped")

    def next_song(self):
        current_song = self.songs_list.curselection()
        if current_song:
            next_song = int(current_song[0]) + 1
            if next_song < self.songs_list.size():
                self.songs_list.selection_clear(0, tk.END)
                self.songs_list.selection_set(next_song)
                self.play()

    def prev_song(self):
        current_song = self.songs_list.curselection()
        if current_song:
            prev_song = int(current_song[0]) - 1
            if prev_song >= 0:
                self.songs_list.selection_clear(0, tk.END)
                self.songs_list.selection_set(prev_song)
                self.play()

    def set_volume(self, val):
        volume = int(val)
        mixer.music.set_volume(volume / 100)

    def adjust_bass(self, val):
        bass = int(val)
        mixer.music.set_volume(0.7 + bass / 20)  # Adjust bass by changing overall volume

    def adjust_treble(self, val):
        treble = int(val)
        mixer.music.set_volume(0.7 - treble / 20)  # Adjust treble by changing overall volume

    def load_songs(self):
        if os.path.exists("songs.txt"):
            with open("songs.txt", "r") as file:
                songs = file.read().splitlines()
                for song in songs:
                    self.songs_list.insert(tk.END, song)

    def update_status(self, message):
        self.status_label.config(text=message)

    def save_songs(self):
        songs = self.songs_list.get(0, tk.END)
        with open("songs.txt", "w") as file:
            for song in songs:
                file.write(song + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()