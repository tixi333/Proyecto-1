import tkinter as tk
from tkinter import ttk
import tkinterdnd2 as tkdnd

class Screens:
    def create_home_screen(self):
    
        frame = tk.Frame(self.page_frame, bg=self.root_bg)

        tk.Label(
            frame,
            text="Inicio",
            font=("Arial", 30, "bold"),
            bg=self.root_bg,
            fg="white"
        ).pack(pady=20)
        
        self.selected_song_label = tk.Label(
            frame,
            text="No song selected",
            font=("Arial", 14),
            bg=self.root_bg,
            fg="white"
        )
        self.selected_song_label.pack(pady=20)

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
        
        self.canvas_selected_song = tk.Canvas(frame, bg=self.tree_bg, width=600, height=600, highlightthickness=0, bd=0)
        self.canvas_selected_song.pack( padx=20, pady=20)
        
        
        self.show_songs()
        return frame
    
    def create_playlist_screen(self):
        frame = tk.Frame(self.page_frame, bg=self.root_bg)
        tk.Label(
            frame,
            text="Crear playlist",
            font=("Arial", 30, "bold"),
            bg=self.root_bg,
            fg="white"
            ).pack(pady=20)
        return frame
    def create_load_screen(self):
    
        frame = tk.Frame(self.page_frame, bg=self.root_bg)

        tk.Label(
            frame,
            text="Anadir desde archivos",
            font=("Arial", 30, "bold"),
            bg=self.root_bg,
            fg="white"
        ).pack(pady=20)

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

        bg_color = "gray30" if active else self.tree_bg
        frame.configure(bg=bg_color)

        for widget in frame.winfo_children():
            widget.configure(bg=bg_color)
    
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
        
        if self.selected_song_label is not None:
            title = song.get("title", "Unknown")
            artist = song.get("artist", "Unknown")
            self.selected_song_label.configure(text=f"Selected: {title} - {artist}")
        
        if self.canvas_selected_song is not None:
            path = song.get("path", "")
            self.current_path = path
            
            self.selected_song_cover = self.load_cover(path, size=420)
            self.canvas_selected_song.delete("all")
            self.canvas_selected_song.create_image(300, 300, image=self.selected_song_cover)
            
        self.play_song(path)
        
        return self.selected_song
