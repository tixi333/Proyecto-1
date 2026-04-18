import pygame
import tkinter as tk
from tkinter import ttk

class PlayerBar():
    
    def create_song_bar(self):
        
        self.song_frame = tk.Frame(self.root, bg = self.menu_bg, height=125)
        
        self.play_btn = tk.Button(self.song_frame,
                        image= self.play_icon,
                        command= self.music_activity,
                        bg = self.menu_bg,
                        activebackground = self.menu_bg,
                        bd =0)
        
        self.next_btn = tk.Button(self.song_frame,
                        image= self.next_icon,
                        command= self.next_song,
                        bg = self.menu_bg,
                        activebackground = self.menu_bg,
                        bd =0)
        
        self.previous_btn = tk.Button(self.song_frame,
                        image= self.previous_icon,
                        command= self.previous_song,
                        bg = self.menu_bg,
                        activebackground = self.menu_bg,
                        bd =0)
        
        self.progressb = ttk.Progressbar(self.song_frame, 
                                         orient= "horizontal",
                                         length= 1000)
        
        self.progressb.place(relx=0.5, rely=0.75, anchor="center")
        
        self.play_btn.place(relx=0.5, rely=0.35, anchor="center")
        self.next_btn.place(in_= self.play_btn, relx=2.5, x=5) 
        self.previous_btn.place(in_= self.play_btn, relx=-2.5, x=-5) 
    
    def show_song_bar(self):
        if self.song_frame.winfo_manager() == "":
            self.song_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)
    
    def hide_song_bar(self):
        if self.song_frame.winfo_manager() == "pack":
            self.song_frame.pack_forget()
    
    def next_song(self):
        songs = self.get_current_song()
        

        if 0 <= self.current_index < len(songs) - 1:
            self.play_song_by_index(self.current_index + 1)
    
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
            
            title = song.get("title", "Unknown")
            artist = song.get("artist", "Unknown")
            if self.selected_song_label is not None:
                self.selected_song_label.configure(text=f"Selected: {title} - {artist}")

            path = song.get("path", "")
            self.current_path = path

            if self.canvas_selected_song is not None:
                self.selected_song_cover = self.load_cover(path, size=420)
                self.canvas_selected_song.delete("all")
                self.canvas_selected_song.create_image(300, 300, image=self.selected_song_cover)

            self.play_song(path)
            
        
    def play_song(self, path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

        self.is_playing = True
        self.is_paused = False
        self.current_path = path

        self.play_btn.configure(image=self.pause_icon)
    
    def music_activity(self):
        
        if self.current_path is None:
            return

        if not self.is_playing and not self.is_paused:
            pygame.mixer.music.load(self.current_path)
            pygame.mixer.music.play()

            self.is_playing = True
            self.is_paused = False
            self.play_btn.configure(image=self.pause_icon)
            return

        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.is_playing = False
            self.play_btn.configure(image=self.play_icon)
            return

        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.is_playing = True
            self.play_btn.configure(image=self.pause_icon)
          
