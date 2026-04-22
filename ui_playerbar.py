import random
import pygame
import tkinter as tk
from tkinter import ttk


class PlayerBar():
    def create_song_bar(self):
        self.song_frame = tk.Frame(self.root, bg="gray15", height=100)

        self.progressb = ttk.Progressbar(
            self.song_frame,
            orient="horizontal",
            length=1000,
            mode="determinate",
            variable=self.progress_value,
            maximum=100
        )
        self.progressb.bind("<Button-1>", self.seek_song)
        self.progressb.place(relx=0.5, rely=0.78, anchor="center")

        self.info_frame = tk.Frame(self.song_frame, bg="gray15")
        self.info_frame.place(relx=0.5, rely=0.35, anchor="center")

        self.shuffle_btn = self.create_mode_button(self.info_frame, self.shuffle_off, self.toggle_shuffle)
        self.shuffle_btn.pack(side=tk.LEFT, padx=6)

        self.previous_btn = tk.Button(
            self.info_frame,
            image=self.previous_icon,
            command=self.previous_song,
            bg="gray15",
            activebackground="gray15",
            bd=0
        )
        self.previous_btn.pack(side=tk.LEFT, padx=6)

        self.play_btn = tk.Button(
            self.info_frame,
            image=self.play_icon,
            command=self.music_activity,
            bg="gray15",
            activebackground="gray15",
            bd=0
        )
        self.play_btn.pack(side=tk.LEFT, padx=6)

        

        self.next_btn = tk.Button(
            self.info_frame,
            image=self.next_icon,
            command=self.next_song,
            bg="gray15",
            activebackground="gray15",
            bd=0
        )
        self.next_btn.pack(side=tk.LEFT, padx=6)

        self.stop_btn = self.create_mode_button(self.info_frame, self.stop_icon, self.stop_song)
        self.stop_btn.pack(side=tk.LEFT, padx=6)

        self.loop_btn = self.create_mode_button(self.info_frame, self.loop, self.toggle_loop)
        self.loop_btn.pack(side=tk.LEFT, padx=6)

        self.volume_frame = tk.Frame(self.song_frame, bg="gray15")
        self.volume_frame.place(relx=0.8, rely=0.25, anchor="e")

        self.volume_label = tk.Label(
            self.volume_frame,
            text="Volume 70%",
            bg="gray15",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.volume_label.pack(anchor="e")

        self.volume_slider = ttk.Scale(
            self.volume_frame,
            from_=0,
            to=100,
            orient="horizontal",
            length=170,
            variable=self.volume_value,
            command=self.change_volume
        )
        self.volume_slider.pack(anchor="e", pady=(4, 0))

        self.sync_control_states()

    def create_mode_button(self, parent, img, command):
        return tk.Button(
            parent,
            image = img,
            command=command,
            bg="gray15",
            activebackground="gray15",
            relief=tk.FLAT,
            bd=0,
            padx=10,
            pady=6,
        )

    def set_play_button_state(self, is_playing):
        if is_playing:
            icon = self.pause_icon
        else:
            icon = self.play_icon

        if hasattr(self, "play_btn") and self.play_btn is not None:
            self.play_btn.configure(image=icon)

        if hasattr(self, "play_btn2") and self.play_btn2 is not None:
            self.play_btn2.configure(image=icon)

    def sync_control_states(self):
        print(self.shuffle_enabled)

        if self.shuffle_enabled:
            icon = self.shuffle_on
        else:
            icon = self.shuffle_off
        
        if hasattr(self, "shuffle_btn") and self.shuffle_btn is not None:
            self.shuffle_btn.configure(image=icon)
        
        if hasattr(self, "shuffle_btn2") and self.shuffle_btn2 is not None:
            self.shuffle_btn2.configure(image= icon)
        
        
        volume_text = f"Volume {int(round(self.volume_value.get()))}%"
        for attr_name in ("volume_label", "volume_label2"):
            label = getattr(self, attr_name, None)
            if label is not None:
                label.configure(text=volume_text)

    def change_volume(self, value):
        volume = float(value)
        self.volume_value.set(volume)
        pygame.mixer.music.set_volume(volume / 100)
        self.sync_control_states()

    def toggle_shuffle(self):

        self.current_mode = self.check_mode()

        if self.current_mode == None or self.current_mode == "shuffle":

            if self.shuffle_enabled:
                self.shuffle_enabled = False
                self.current_mode = None
                #sync --------------
            else:
                self.shuffle_enabled = True
                self.current_mode = "shuffle"

            self.sync_control_states()

    def toggle_loop(self):

        self.current_mode = self.check_mode()

        if self.current_mode == None or self.current_mode == "loop":
            if self.loop_enabled:
                self.loop_enabled = False
                self.current_mode = None
            else:
                self.loop_enabled = True
                self.current_mode = "loop"

            self.sync_control_states()
        
    def check_mode(self):
        self.root.after(500, self.check_mode)
        

    def stop_song(self):
        if self.progress_job is not None:
            try:
                self.root.after_cancel(self.progress_job)
            except tk.TclError:
                pass
            self.progress_job = None

        pygame.mixer.music.stop()
        self.play_song(self.current_path)
        self.playback_offset = 0
        self.progress_value.set(0)
        self.is_playing = True
        self.is_paused = False
        self.set_play_button_state(True)
        
    def get_shuffle_index(self, songs):
        if not songs:
            return -1

        if len(songs) == 1:
            return 0

        total = len(songs)
        indices = range(total)

        candidates = []

        for index in indices:
            if index != self.current_index:
                candidates.append(index)
                
        e = random.choice(candidates)
        return e

    def show_song_bar(self):
        if self.song_frame.winfo_manager() == "":
            self.song_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)

    def hide_song_bar(self):
        if self.song_frame.winfo_manager() == "pack":
            self.song_frame.pack_forget()

    def next_song(self):
        songs = self.get_current_song()

        if not songs:
            return

        if self.shuffle_enabled:
            next_index = self.get_shuffle_index(songs)
        elif self.current_index >= 0 and  self.current_index < len(songs) - 1:
            next_index = self.current_index + 1
        else:
            next_index = -1

        if next_index != -1:
            self.play_song_by_index(next_index)

    def previous_song(self):
        if self.current_index > 0:
            self.play_song_by_index(self.current_index - 1)

    def play_song_by_index(self, index):
        songs = self.get_current_song()

        if 0 <= index < len(songs):
            song = songs[index]
            self.current_index = index
            self.selected_song = song

            if self.selected_song_frame is not None:
                self.set_song_frame_state(self.selected_song_frame, active=False)

            song_frame = self.song_frames.get(index)
            self.set_song_frame_state(song_frame, active=True)
            self.selected_song_frame = song_frame

            path = song.get("path", "")
            self.current_path = path

            self.update_selected_song_display(song)
            self.play_song(path)

    def play_song(self, path):
        if self.progress_job is not None:
            try:
                self.root.after_cancel(self.progress_job)
            except tk.TclError:
                pass
            self.progress_job = None

        self.current_path = path
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.volume_value.get() / 100)
        pygame.mixer.music.play()

        self.total_seconds = pygame.mixer.Sound(path).get_length()
        self.playback_offset = 0

        self.progress_value.set(0)
        self.is_playing = True
        self.is_paused = False
        self.set_play_button_state(True)
        self.check_song_act()

    def check_song_act(self):
        self.progress_job = None

        if not self.is_playing or self.is_paused:
            return

        if not pygame.mixer.music.get_busy():
            songs = self.get_current_song()

            if self.loop_enabled and 0 <= self.current_index < len(songs):
                self.play_song_by_index(self.current_index)
            elif self.shuffle_enabled and songs:
                self.play_song_by_index(self.get_shuffle_index(songs))
            elif 0 <= self.current_index < len(songs) - 1:
                self.next_song()
            else:
                self.is_playing = False
                self.is_paused = False
                self.playback_offset = 0
                self.progress_value.set(0)
                self.set_play_button_state(False)
            return

        current_seconds = max(pygame.mixer.music.get_pos() / 1000, 0)
        current_seconds += self.playback_offset

        if self.total_seconds > 0:
            percent = min((current_seconds / self.total_seconds) * 100, 100)
            self.progress_value.set(percent)

        self.progress_job = self.root.after(500, self.check_song_act)

    def music_activity(self):
        if self.current_path is None:
            return

        if not self.is_playing and not self.is_paused:
            pygame.mixer.music.load(self.current_path)
            pygame.mixer.music.set_volume(self.volume_value.get() / 100)
            pygame.mixer.music.play()

            self.is_playing = True
            self.is_paused = False
            self.set_play_button_state(True)
            self.check_song_act()
            return

        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            if self.progress_job is not None:
                try:
                    self.root.after_cancel(self.progress_job)
                except tk.TclError:
                    pass
                self.progress_job = None
            self.is_paused = True
            self.is_playing = False
            self.set_play_button_state(False)
            return

        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.is_playing = True
            self.set_play_button_state(True)
            self.check_song_act()

    def seek_song(self, event):
        if self.current_path is None or self.total_seconds <= 0:
            return

        widget = event.widget
        width = max(widget.winfo_width(), 1)
        click_x = min(max(event.x, 0), width)
        target_seconds = (click_x / width) * self.total_seconds

        if self.progress_job is not None:
            try:
                self.root.after_cancel(self.progress_job)
            except tk.TclError:
                pass
            self.progress_job = None

        self.playback_offset = target_seconds

        pygame.mixer.music.load(self.current_path)
        pygame.mixer.music.set_volume(self.volume_value.get() / 100)
        try:
            pygame.mixer.music.play(start=target_seconds)
        except pygame.error:
            pygame.mixer.music.play()
            try:
                pygame.mixer.music.set_pos(target_seconds)
            except pygame.error:
                self.playback_offset = 0

        percent = min((target_seconds / self.total_seconds) * 100, 100)
        self.progress_value.set(percent)

        self.is_playing = True
        self.is_paused = False
        self.set_play_button_state(True)
        self.check_song_act()
