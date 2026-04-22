import tkinter as tk
from tkinter import messagebox, ttk
import tkinterdnd2 as tkdnd

class Screens:
    def create_home_screen(self):

        frame = tk.Frame(self.page_frame, bg=self.root_bg)
        self.create_song_slide_bar(frame)

        self.load_info_tree()

        self.container_frame = tk.Frame(frame, bg=self.tree_bg, width=400, height=400)
        self.container_frame.pack(side=tk.LEFT, fill=tk.Y, pady=20, padx=20)
        self.container_frame.pack_propagate(False)
        
        self.list_container_frame = tk.Frame(self.container_frame, bg=self.tree_bg)
        self.list_container_frame.pack(fill=tk.BOTH, expand=True,padx=18, pady=(0, 18))
        
        self.canvas = tk.Canvas(self.list_container_frame, bg= self.tree_bg, highlightthickness=0, bd=0)
        
        self.scrollbar = ttk.Scrollbar(
            self.list_container_frame,
            orient=tk.VERTICAL,
            command=self.canvas.yview,
            style="Visible.Vertical.TScrollbar"
        )
        
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.tree_bg)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        self.canvas.configure(yscrollcommand= self.scrollbar.set)
        
        self.canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind(
            "<Configure>", lambda e: self.canvas.itemconfigure(self.canvas_window, width=e.width)
        )
        
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel)
        self.canvas.bind("<Button-5>", self._on_mousewheel)
        
        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<Button-4>", self._on_mousewheel)
        self.scrollable_frame.bind("<Button-5>", self._on_mousewheel)

        self.home_playlist_frame = tk.LabelFrame(
            frame,
            text="Load Playlist",
            fg="white",
            bg="grey10",
            width=420,
            height=300
        )
        self.home_playlist_frame.pack(side=tk.LEFT, padx=(0, 20), pady=20)
        self.home_playlist_frame.pack_propagate(False)

        self.current_source_label = tk.Label(
            self.home_playlist_frame,
            text="Saved Songs",
            bg="grey10",
            fg="white",
            font=("Arial", 11, "bold")
        )
        self.current_source_label.pack(anchor="w", padx=14, pady=(14, 8))

        tk.Label(
            self.home_playlist_frame,
            text="Search playlists",
            bg="grey10",
            fg="white",
            font=("Arial", 10)
        ).pack(anchor="w", padx=14)

        self.saved_playlist_search_entry = tk.Entry(
            self.home_playlist_frame,
            textvariable=self.saved_playlist_search_var,
            font=("Arial", 11),
            fg="grey15"
        )
        self.saved_playlist_search_entry.pack(fill=tk.X, padx=14, pady=(0, 10))
        self.saved_playlist_search_entry.bind("<KeyRelease>", lambda e: self.refresh_saved_playlists_list())

        self.saved_playlists_list = tk.Listbox(
            self.home_playlist_frame,
            bg="grey10",
            fg="white",
            selectbackground="PaleVioletRed3",
            selectforeground="black",
            activestyle="none",
            font=("Arial", 12),
            exportselection=False,
            height=8
        )
        self.saved_playlists_scrollbar = tk.Scrollbar(
            self.home_playlist_frame,
            orient=tk.VERTICAL,
            command=self.saved_playlists_list.yview
        )
        self.saved_playlists_list.configure(yscrollcommand=self.saved_playlists_scrollbar.set)
        self.saved_playlists_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(14, 0), pady=(0, 14))
        self.saved_playlists_scrollbar.pack(side=tk.LEFT, fill=tk.Y, padx=(8, 14), pady=(0, 14))

        self.home_playlist_buttons = tk.Frame(self.home_playlist_frame, bg="grey10", width=140)
        self.home_playlist_buttons.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 14), pady=(0, 14))
        self.home_playlist_buttons.pack_propagate(False)

        self.load_original_btn = tk.Button(
            self.home_playlist_buttons,
            text="Original",
            command=self.load_original_library,
            bg="gray70",
            activebackground="gray55",
            fg="black",
            font=("Arial", 11, "bold"),
            bd=0,
            padx=14,
            pady=10
        )
        self.load_original_btn.pack(fill=tk.X, pady=(24, 12))

        self.load_playlist_btn = tk.Button(
            self.home_playlist_buttons,
            text="Load Playlist",
            command=self.load_selected_playlist,
            bg="PaleVioletRed3",
            activebackground="PaleVioletRed4",
            fg="black",
            font=("Arial", 11, "bold"),
            bd=0,
            padx=14,
            pady=10,
        )
        self.load_playlist_btn.pack(fill=tk.X)

        self.refresh_saved_playlists_list()
        self.update_current_source_label()
        self.show_songs()
        return frame
    
    def create_playlist_screen(self):
        frame = tk.Frame(self.page_frame, bg=self.root_bg)

        tk.Label(
            frame,
            text="Create Playlist",
            font=("Arial", 24, "bold"),
            bg=self.root_bg,
            fg="white"
        ).pack(anchor="nw", padx=20, pady=(20, 0))

        self.playlist_setting(frame=frame)
        return frame
    
    def playlist_setting (self,frame):
        if hasattr(self, "self.setting_f"):
            self.setting_f.destroy()
        #==================================================================================================================
        
        self.setting_f = tk.Frame(frame, 
                                  bg = "grey15",
                                  height= 700,
                                  width= 800)
        
        self.setting_f.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20, anchor="nw")
        self.setting_f.pack_propagate(False)
        #==================================================================================================================
        self.name_frame = tk.LabelFrame(self.setting_f,
                                   text = "Playlist Name",
                                    fg = "white",
                                    bg = "grey25",
                                    width = 500,
                                    height= 150)
    
        
        self.name_frame.pack(side=tk.TOP, anchor="nw", padx=20, pady=20)
        self.name_frame.pack_propagate(False)
       
        self.name_entry= tk.Entry(self.name_frame, justify= tk.LEFT, width= 50, font=("Arial", 20), fg = "grey10")
        self.name_entry.pack(side=tk.TOP, anchor="nw", padx=40, pady=40)
        
        #==================================================================================================================
        self.playlist_lists_frame = tk.Frame(self.setting_f, bg="grey15")
        self.playlist_lists_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        #==================================================================================================================
        self.available_frame = tk.LabelFrame(
            self.playlist_lists_frame,
            text="Available Songs",
            fg="white",
            bg="grey25",
            width=520,
            height=420
        )
        self.available_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.available_frame.pack_propagate(False)

        tk.Label(
            self.available_frame,
            text="Search available songs",
            bg="grey25",
            fg="white",
            font=("Arial", 10)
        ).pack(anchor="w", padx=12, pady=(12, 0))

        self.available_search_entry = tk.Entry(
            self.available_frame,
            textvariable=self.available_song_search_var,
            font=("Arial", 11),
            fg="grey15"
        )
        self.available_search_entry.pack(fill=tk.X, padx=12, pady=(4, 0))
        self.available_search_entry.bind("<KeyRelease>", lambda e: self.refresh_playlist_builder_lists())

        self.available_songs_list = tk.Listbox(
            self.available_frame,
            bg="grey10",
            fg="white",
            selectbackground="PaleVioletRed3",
            selectforeground="black",
            activestyle="none",
            font=("Arial", 12),
            exportselection=False,
            selectmode=tk.EXTENDED
        )
        self.available_songs_scrollbar = tk.Scrollbar(
            self.available_frame,
            orient=tk.VERTICAL,
            command=self.available_songs_list.yview
        )
        self.available_songs_list.configure(yscrollcommand=self.available_songs_scrollbar.set)
        self.available_songs_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(12, 0), pady=12)
        self.available_songs_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(8, 12), pady=12)
        
        #==================================================================================================================
        self.playlist_actions_frame = tk.Frame(self.playlist_lists_frame, bg="grey15", width=150)
        self.playlist_actions_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20)
        self.playlist_actions_frame.pack_propagate(False)

        self.add_song_to_playlist_btn = tk.Button(
            self.playlist_actions_frame,
            text="Add ->",
            command=self.add_selected_songs_to_playlist,
            bg="PaleVioletRed3",
            activebackground="PaleVioletRed4",
            fg="black",
            font=("Arial", 12, "bold"),
            bd=0,
            padx=16,
            pady=10
        )
        self.add_song_to_playlist_btn.pack(pady=(140, 12), fill=tk.X)

        self.remove_song_from_playlist_btn = tk.Button(
            self.playlist_actions_frame,
            text="<- Remove",
            command=self.remove_selected_songs_from_playlist,
            bg="gray70",
            activebackground="gray55",
            fg="black",
            font=("Arial", 12, "bold"),
            bd=0,
            padx=16,
            pady=10
        )
        self.remove_song_from_playlist_btn.pack(fill=tk.X)
        #==================================================================================================================
        self.selected_frame = tk.LabelFrame(
            self.playlist_lists_frame,
            text="Selected Songs",
            fg="white",
            bg="grey25",
            width=520,
            height=420
        )
        self.selected_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.selected_frame.pack_propagate(False)

        tk.Label(
            self.selected_frame,
            text="Search playlist songs",
            bg="grey25",
            fg="white",
            font=("Arial", 10)
        ).pack(anchor="w", padx=12, pady=(12, 0))

        self.selected_search_entry = tk.Entry(
            self.selected_frame,
            textvariable=self.selected_playlist_search_var,
            font=("Arial", 11),
            fg="grey15"
        )
        self.selected_search_entry.pack(fill=tk.X, padx=12, pady=(4, 0))
        self.selected_search_entry.bind("<KeyRelease>", lambda e: self.refresh_playlist_builder_lists())

        self.selected_playlist_list = tk.Listbox(
            self.selected_frame,
            bg="grey15",
            fg="white",
            selectbackground="PaleVioletRed3",
            selectforeground="black",
            activestyle="none",
            font=("Arial", 12),
            exportselection=False,
            selectmode=tk.EXTENDED
        )
        self.selected_playlist_scrollbar = tk.Scrollbar(
            self.selected_frame,
            orient=tk.VERTICAL,
            command=self.selected_playlist_list.yview
        )
        self.selected_playlist_list.configure(yscrollcommand=self.selected_playlist_scrollbar.set)
        self.selected_playlist_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(12, 0), pady=12)
        self.selected_playlist_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(8, 12), pady=12)

        self.playlist_savef = tk.Frame(self.setting_f, bg="grey15")
        self.playlist_savef.pack(fill=tk.X, padx=20, pady=(0, 20))
        

        self.save_playlist_btn = tk.Button(
            self.playlist_savef,
            text="Save Playlist",
            command=self.save_playlist_selection,
            bg="PaleVioletRed3",
            activebackground="PaleVioletRed4",
            fg="black",
            font=("Arial", 12, "bold"),
            bd=0,
            padx=18,
            pady=10
        )
        self.save_playlist_btn.pack(side=tk.RIGHT)

        self.refresh_playlist_builder_lists()

    def get_playlist_song_text(self, song):
        title = song.get("title", "Unknown")
        artist = song.get("artist", "Unknown")
        return f"{title} - {artist}"

    def refresh_playlist_builder_lists(self):
        if not hasattr(self, "available_songs_list"):
            return

        self.playlist_library_songs = self.load_songs()["songs"]
        available_query = self.available_song_search_var.get().strip().lower()
        selected_query = self.selected_playlist_search_var.get().strip().lower()

        self.filtered_playlist_library_songs = [
            song for song in self.playlist_library_songs
            if available_query in self.get_playlist_song_text(song).lower()
        ]

        self.filtered_playlist_selected_songs = [
            song for song in self.playlist_selected_songs
            if selected_query in self.get_playlist_song_text(song).lower()
        ]

        self.available_songs_list.delete(0, tk.END)
        for song in self.filtered_playlist_library_songs:
            self.available_songs_list.insert(tk.END, self.get_playlist_song_text(song))

        self.selected_playlist_list.delete(0, tk.END)
        for song in self.filtered_playlist_selected_songs:
            self.selected_playlist_list.insert(tk.END, self.get_playlist_song_text(song))

    def refresh_saved_playlists_list(self):
        if not hasattr(self, "saved_playlists_list"):
            return

        self.saved_playlists = self.list_saved_playlists()
        query = self.saved_playlist_search_var.get().strip().lower()
        self.filtered_saved_playlists = [
            playlist for playlist in self.saved_playlists
            if query in playlist["name"].lower()
        ]
        self.saved_playlists_list.delete(0, tk.END)

        for playlist in self.filtered_saved_playlists:
            self.saved_playlists_list.insert(tk.END, playlist["name"])

    def update_current_source_label(self):
        if not hasattr(self, "current_source_label"):
            return

        if self.active_playlist is None:
            source_text = "Canciones guardadas"
        else:
            source_name = self.active_playlist
            for playlist in getattr(self, "saved_playlists", []):
                if playlist["path"] == self.active_playlist:
                    source_name = playlist["name"]
                    break
            source_text = f"{source_name}"

        self.current_source_label.configure(text=source_text)

    def add_selected_songs_to_playlist(self):
        if not hasattr(self, "available_songs_list"):
            return

        selected_indexes = self.available_songs_list.curselection()
        selected_paths = {song.get("path") for song in self.playlist_selected_songs}

        for index in selected_indexes:
            song = self.filtered_playlist_library_songs[index]
            path = song.get("path")
            if path not in selected_paths:
                self.playlist_selected_songs.append(song)
                selected_paths.add(path)

        self.refresh_playlist_builder_lists()

    def remove_selected_songs_from_playlist(self):
        if not hasattr(self, "selected_playlist_list"):
            return

        selected_indexes = list(self.selected_playlist_list.curselection())
        selected_paths = {
            self.filtered_playlist_selected_songs[index].get("path")
            for index in selected_indexes
        }
        self.playlist_selected_songs = [
            song for song in self.playlist_selected_songs
            if song.get("path") not in selected_paths
        ]

        self.refresh_playlist_builder_lists()

    def save_playlist_selection(self):
        playlist_name = self.name_entry.get().strip()

        if not playlist_name:
            messagebox.showwarning("Playlist", "Enter a playlist name first.")
            return

        if not self.playlist_selected_songs:
            messagebox.showwarning("Playlist", "Select at least one song.")
            return

        playlist_path = self.save_playlist_data(playlist_name, self.playlist_selected_songs)
        self.playlist_selected_songs.clear()
        self.name_entry.delete(0, tk.END)
        self.refresh_playlist_builder_lists()
        self.refresh_saved_playlists_list()
        self.update_current_source_label()

        self.playlist_status_label.configure(
            text=f"Playlist '{playlist_name}' saved. Load it from the home screen."
        )
        messagebox.showinfo("Playlist", f"Playlist saved to {playlist_path}")

    def load_original_library(self):
        self.active_playlist = None
        self.current_index = -1
        self.progress_value.set(0)
        self.show_songs()
        self.update_current_source_label()
        if hasattr(self, "playlist_status_label") and self.playlist_status_label is not None:
            self.playlist_status_label.configure(text="Original library loaded.")

    def load_selected_playlist(self):
        if not hasattr(self, "saved_playlists_list"):
            return

        selected_indexes = self.saved_playlists_list.curselection()
        if not selected_indexes:
            messagebox.showwarning("Playlist", "Select a saved playlist to load.")
            return

        playlist = self.filtered_saved_playlists[selected_indexes[0]]
        self.active_playlist = playlist["path"]
        self.current_index = -1
        self.progress_value.set(0)
        self.show_songs()
        self.update_current_source_label()
        if hasattr(self, "playlist_status_label") and self.playlist_status_label is not None:
            self.playlist_status_label.configure(
                text=f"Playlist '{playlist['name']}' loaded."
            )
         
         
    def create_load_screen(self):
    
        frame = tk.Frame(self.page_frame, bg=self.root_bg)

        tk.Label(
        frame,
        text="Cargá el archivo desde:",
        font=("Arial", 14),
        bg=self.root_bg,
        fg="white"
        ).pack(pady=10)
        
        tk.Button(
        frame,
        text="Abrir desde archivos",
        command=self.load_file
        ).pack(pady=10)

        tk.Label(
            frame, 
            text= "Arrastrá y soltá tu canción aquí",
            font=("Arial", 14),
            bg=self.root_bg,
            fg = "white"
        ). pack(pady =10, padx=0)
        
        drop_frame = tk.Frame(frame, bg="gray30", width=800, height=400)
        drop_frame.pack(pady=20)
        drop_frame.pack_propagate(False)

        # Define el frame que debe aceptar archivos para el drag and drop.
        drop_frame.drop_target_register(tkdnd.DND_FILES)
        
        drop_frame.dnd_bind("<<Drop>>", self.handle_drop)

        return frame
    ##================================ SCROLL CON MOUSEWHEEL ==================================
    def _on_mousewheel(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")
        else:
            self.canvas.yview_scroll(int(-event.delta / 120), "units")
   
   ##================================ MOSTRAR CANCIONES EN SCROLLABLE FRAME ===================
        
    def show_songs(self):
        self._cancel_song_render_jobs()

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.song_frames.clear()
        
        for index, song in enumerate(self.get_current_song()):
            title = song.get("title", "Unknown")
            artist = song.get("artist", "Unknown")
            album = song.get("album", "Unknown")
            path = song.get("path", "")
            
            song_frame = tk.Frame(self.scrollable_frame, bg=self.tree_bg, pady=5)
            
            self.song_frames[index] = song_frame
            
            cover = self.load_cover(path)
            cover_label = tk.Label(song_frame, image=cover, bg=self.tree_bg)
            cover_label.image = cover
            cover_label.pack(side=tk.LEFT, padx=5)
            
            tk.Label(song_frame, text=title, fg="white", bg="#121212").pack(anchor="w")
            tk.Label(song_frame, text=artist, fg="gray", bg="#121212").pack(anchor="w")
            tk.Label(song_frame, text=album, fg="gray", bg="#121212").pack(anchor="w")

            song_frame.bind("<Button-1>", lambda e, f=song_frame, s=song: self.select_song(f, s))
            
            
            for widget in song_frame.winfo_children():
                widget.bind("<Button-1>", lambda e, f=song_frame, s=song: self.select_song(f, s))
            
            song_frame.bind("<MouseWheel>", self._on_mousewheel)
            song_frame.bind("<Button-4>", self._on_mousewheel)
            song_frame.bind("<Button-5>", self._on_mousewheel)

            delay = min(index * 45, 360)
            job_id = self.root.after(
                delay,
                lambda f=song_frame: self._show_song_frame(f)
            )
            self.song_render_jobs.append(job_id)

        self.sync_selected_song_state()
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _show_song_frame(self, song_frame):
        song_frame.pack(fill="x", padx=5, pady=5)
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _cancel_song_render_jobs(self):
        for job_id in self.song_render_jobs:
            try:
                self.root.after_cancel(job_id)
            except tk.TclError:
                pass

        self.song_render_jobs.clear()

    def set_song_frame_state(self, frame, active=False):
        if frame is None:
            return

        try:
            if not frame.winfo_exists():
                return
        except tk.TclError:
            return

        bg_color = "gray30" if active else self.tree_bg
        try:
            frame.configure(bg=bg_color)
        except tk.TclError:
            return

        for widget in frame.winfo_children():
            try:
                widget.configure(bg=bg_color)
            except tk.TclError:
                continue

    def find_song_index(self, song, songs=None):
        if song is None:
            return -1

        if songs is None:
            songs = self.get_current_song()

        song_path = song.get("path")
        for index, current_song in enumerate(songs):
            if current_song.get("path") == song_path:
                return index

        return -1

    def update_selected_song_display(self, song=None):
        if self.selected_song_label is not None:
            if song is None:
                self.selected_song_label.configure(text="No song selected")
            else:
                title = song.get("title", "Unknown")
                artist = song.get("artist", "Unknown")
                self.selected_song_label.configure(text=f"{title} - {artist}")

        if self.canvas_selected_song is not None:
            path = "" if song is None else song.get("path", "")
            self.selected_song_cover = self.load_cover(path, size=420)
            self.canvas_selected_song.delete("all")
            self.canvas_selected_song.create_image(300, 300, image=self.selected_song_cover)

    def sync_selected_song_state(self):
        songs = self.get_current_song()
        selected_index = self.find_song_index(self.selected_song, songs)

        if selected_index == -1:
            if self.current_path is not None:
                self.stop_song()
            self.selected_song = None
            self.selected_song_frame = None
            self.current_index = -1
            self.current_path = None
            self.update_selected_song_display()
            return

        self.selected_song = songs[selected_index]
        self.current_index = selected_index
        self.selected_song_frame = self.song_frames.get(selected_index)
        self.set_song_frame_state(self.selected_song_frame, active=True)
        self.update_selected_song_display(self.selected_song)
    
    ##================================ SELECCIONAR CANCION ==================================
    
    def select_song(self, frame, song):
        if self.selected_song_frame is not None:
            self.set_song_frame_state(self.selected_song_frame, active=False)
            
        self.selected_song = song
        songs = self.get_current_song()
        try:
            self.current_index = songs.index(song)
        except ValueError:
            self.current_index = -1
        
        self.set_song_frame_state(frame, active=True)
        self.selected_song_frame = frame

        path = song.get("path", "")
        self.current_path = path
        self.update_selected_song_display(song)

        self.play_song(path)
        
        return self.selected_song

    def create_song_slide_bar(self, frame):
        
        self.frame_home = tk.Frame(frame, bg = "gray20", width=500)
        
        self.frame_home.pack(side= tk.RIGHT , fill = tk.Y , pady = 10, padx=10)
        
        
        self.canvas_selected_song = tk.Canvas(self.frame_home, bg="gray15", width=600, height=600, highlightthickness=0, bd=0)
        self.canvas_selected_song.pack( padx=20, pady=20)
        
        self.info = tk.Frame (self.frame_home, bg = "gray15", width=600, height=600)
        self.info.pack(side =tk. TOP, fill= tk.BOTH, padx= 20, pady=20)
        self.info.pack_propagate(False)
        
        self.selected_song_label = tk.Label(
            self.info,
            text="No song selected",
            font=("Arial", 14),
            bg="gray15",
            fg="white"
        )

        self.controls_frame2 = tk.Frame(self.info, bg="gray15")

        self.shuffle_btn2 = self.create_mode_button(self.controls_frame2, self.shuffle_off , self.toggle_shuffle)
        self.shuffle_btn2.pack(side=tk.LEFT, padx=6)

        self.previous_btn2 = tk.Button(
            self.controls_frame2,
            image=self.previous_icon,
            command=self.previous_song,
            bg="gray15",
            activebackground="gray15",
            bd=0
        )
        self.previous_btn2.pack(side=tk.LEFT, padx=6)

        self.play_btn2 = tk.Button(
            self.controls_frame2,
            image=self.play_icon,
            command=self.music_activity,
            bg="gray15",
            activebackground="gray15",
            bd=0
        )
        self.play_btn2.pack(side=tk.LEFT, padx=6)
        
        self.next_btn2 = tk.Button(
            self.controls_frame2,
            image=self.next_icon,
            command=self.next_song,
            bg="gray15",
            activebackground="gray15",
            bd=0
        )
        self.next_btn2.pack(side=tk.LEFT, padx=6)
        
        self.stop_btn2 = self.create_mode_button(self.controls_frame2, self.stop_icon, self.stop_song)
        
        self.stop_btn2.pack(side=tk.LEFT, padx=6)

        self.loop_btn2 = self.create_mode_button(self.controls_frame2, self.loop , self.toggle_loop)
        self.loop_btn2.pack(side=tk.LEFT, padx=6)
        
        self.progress = ttk.Progressbar(self.info,
                                   orient="horizontal",
                                   length=500,
                                   mode="determinate",
                                   variable=self.progress_value,
                                   maximum=100)
        self.progress.bind("<Button-1>", self.seek_song)

        self.volume_frame2 = tk.Frame(self.info, bg="gray15")
        self.volume_label2 = tk.Label(
            self.volume_frame2,
            text="Volume 70%",
            bg="gray15",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.volume_label2.pack(anchor="center")

        self.volume_slider2 = ttk.Scale(
            self.volume_frame2,
            from_=0,
            to=100,
            orient="horizontal",
            length=220,
            variable=self.volume_value,
            command=self.change_volume
        )
        self.volume_slider2.pack(anchor="center", pady=(6, 0))
        
        self.progress.place(relx=0.5, rely=0.78, anchor="center")
        self.selected_song_label.place(relx=0.5, rely=0.18, anchor="center")
        self.controls_frame2.place(relx=0.5, rely=0.45, anchor="center")
        self.volume_frame2.place(relx=0.5, rely=0.60, anchor="center")

        self.sync_control_states()
