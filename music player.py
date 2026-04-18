import shutil
from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import tkinterdnd2 as tkdnd
import json, os
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3
from io import BytesIO
import pygame
## 1
## add from file screen : + input artist, title, album, load cover manually
##                        + tinytag/mutagen for metadata (artist, title, album) and cover
## 2 interfaz
## add loaded songs at home screen
## 3 barra de progreso, play, pause, stop, next, previous

##Tkinterdnd - filedialog.askopenfilename()
class MusicPlayer:
    def __init__(self,root):
        
        #=================================CONFIGURACION INICIAL=========================================
        
        self.root_bg = "black"
        self.menu_bg = "PaleVioletRed3"
        self.tree_bg = "black"
        
        self.root = root
        self.root.title("Music Player")

        self.root.state("zoomed")
        self.root.configure(bg=self.root_bg)

        self.root.minsize(800, 600)
        
        pygame.mixer.init()
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Visible.Vertical.TScrollbar",
            gripcount=0,
            background="gray55",
            darkcolor="gray35",
            lightcolor="gray55",
            troughcolor="gray10",
            bordercolor="gray10",
            arrowcolor="white"
        )
        
        
        self.current_page = None
        self.json = "titulos.json"
        
        
        self.selected_song = None
        self.selected_song_frame = None
        self.selected_song_label = None
        self.selected_song_cover = None
        
        self.is_paused = False
        self.is_playing = False
        self.current_path = None
        self.current_index = -1
        
        self.active_playlist = None
        
        self.song_frames = {}
        
        self.load_json()
        self.load_icons()
        
        self.create_sidebar()
        
        self.page_frame = tk.Frame(self.root, bg = self.root_bg)
        self.page_frame.pack(fill = tk.BOTH, expand = True)
        
        
        
        self.screens = {
            "home": self.create_home_screen(),
            "playlist": self.create_playlist_screen(),
            "load": self.create_load_screen()
        }
        
        
        self.create_song_bar()
        
        self.switch_pages("home", self.home_indicator)
        #lambda event pasa el evento como argumento aunque no se use o indique automaticamente
        
    #======================================= MENU BAR ==========================================     

    def create_sidebar(self):
        self.menu_frame_bar = tk.Frame(self.root, bg = self.menu_bg, width=100)
        self.menu_frame_bar.pack(side = tk.LEFT, fill = tk.Y , pady= 10, padx= 10)
        self.menu_frame_bar.pack_propagate(0)
        
        self.home_indicator = self.create_indicators(200)
        self.playlist_indicator = self.create_indicators(350)
        self.add_indicator = self.create_indicators(500)
        
        self.menubtn = tk.Button(self.menu_frame_bar,
                                image= self.menu_icon,
                                command= self.toggle_menu,
                                bg = self.menu_bg,
                                activebackground = self.menu_bg,
                                bd =0)
        
        self.menubtn.status = "closed"
        self.menubtn.place(x = 15 , y = 15 )
        self.toggle_home = self.create_buttons(img = self.home_icon,
                                               cmd = lambda: self.switch_pages("home", self.home_indicator),
                                               y= 200)
        self.toggle_playlist = self.create_buttons(img = self.playlist_icon,
                                                   cmd = lambda: self.switch_pages("playlist", self.playlist_indicator),
                                                   y= 350)
        self.toggle_add = self.create_buttons(img = self.add_icon,
                                              cmd = lambda: self.switch_pages("load", self.add_indicator),
                                              y= 500)
        
        self.home_lb = self.create_label("Home", 100, self.home_indicator, "home")
        self.playlist_lb = self.create_label("Create playlist", 350, self.playlist_indicator, "playlist")
        self.add_lb = self.create_label("Add from file", 500, self.add_indicator, "load")
    
    #============================================ ICONOS-LABELS-BOTONES ==========================================================
    def load_icons(self):
        def load(path,size):
            img = Image.open(path).resize((size, size))
            return ImageTk.PhotoImage(img)

        self.menu_icon = load("menuicons/menu_icon.png",60)
        self.close_icon = load("menuicons/close_icon.png",60)
        self.home_icon = load("menuicons/home_icon.png",60)
        self.playlist_icon = load("menuicons/create_playlist_icon.png",60)
        self.add_icon = load("menuicons/addfromfile_icon.png",60)
        
        self.play_icon = load("songicons/play.png",40)
        self.pause_icon= load("songicons/pausa.png",40)
        self.next_icon = load("songicons/angulo-derecho.png",40)
        self.previous_icon = load("songicons/angulo-izquierdo.png",40)
        
        
    def create_label(self, text,y, indicator, page):
        lb = tk.Label(self.menu_frame_bar,
                      font = ("Arial", 20, "bold"),
                      text= text,
                      bg = self.menu_bg,
                      fg = "black")
        
        lb.bind("<Button-1>", lambda event: self.switch_pages(page, indicator))
        
        return lb
    
    def create_buttons(self, img,cmd,y):
        btn = tk.Button(self.menu_frame_bar,
                        image= img,
                        command= cmd,
                        bg = self.menu_bg,
                        activebackground = self.menu_bg,
                        bd =0)
        
        btn.place(x= 15, y= y)
        return btn
    #=============================== INDICADORES DE SELECCION EN EL MENU ==================================
    
    def create_indicators(self, y):
        ind = tk.Label(self.menu_frame_bar, bg = self.menu_bg)
        ind.place(x=5, y=y, width=7, height=70)
        
        return ind
        
    def switch_indicator(self,indicator, page):
        
        self.home_indicator.configure(bg = self.menu_bg)
        self.playlist_indicator.configure(bg = self.menu_bg)
        self.add_indicator.configure(bg = self.menu_bg)
        
        indicator.configure(bg = "black")
        
        if self.menu_frame_bar.winfo_width() > 100:
            self.toggle_menu_close()
            
        for frame in self.page_frame.winfo_children():
            frame.destroy()
        
        page()
        
    def reset_indicators(self):
        for indicator in [self.home_indicator, self.playlist_indicator, self.add_indicator]:
            indicator.configure(bg = self.menu_bg)
    
    ##================================ SIDE BAR ANIMACIÓN Y FUNCIONAMIENTO ==================================
    def toggle_menu(self):
        self.animation_menu(opening = True)
        self.show_labels()
        self.menubtn.configure(image = self.close_icon, command = self.toggle_menu_close)
    
    def toggle_menu_close(self):
        
        self.animation_menu(opening = False)
        self.hide_labels()
        self.menubtn.configure(image = self.menu_icon, command = self.toggle_menu)
    
    def animation_menu(self, opening = False):
        
        current_width = self.menu_frame_bar.winfo_width()
        
        if opening:
            if not current_width > 400:
                current_width += 10
                self.menu_frame_bar.configure(width = current_width)
                self.root.after(5, func = lambda:self.animation_menu(opening= True))
        else:
            if current_width > 100:
                current_width -= 10
                self.menu_frame_bar.configure(width = current_width)
                self.root.after(5, func= lambda: self.animation_menu(opening=False))
    
    #=============================== MOSTRAR Y OCULTAR LABELS DEL MENU ==================================            
    def show_labels(self):
        self.home_lb.place(x=90, y=220)
        self.playlist_lb.place(x=90, y=370)
        self.add_lb.place(x=90, y=520)
        
    def hide_labels(self):
        self.home_lb.place_forget()
        self.playlist_lb.place_forget()
        self.add_lb.place_forget()

    
    ##================================ SWITCH PAGES Y MOSTRAR PAGINA SELECCIONADA ================================
    
    def switch_pages(self, page, indicator):
        self.reset_indicators()
        indicator.configure(bg = "black")
        
        if self.menu_frame_bar.winfo_width() > 100:
            self.toggle_menu_close()

        self.show_page(page)
    
    def show_page(self, page):
        for w in self.page_frame.winfo_children():
            w.pack_forget()

        self.screens[page].pack(fill=tk.BOTH, expand=True)
        self.current_page = page
        
        if page in ("playlist", "load"):
            self.show_song_bar()
        else:
            self.hide_song_bar()
    
    ##================================ CREAR BARRA DE CANCIONES ==================================
    
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
        

    
    ## ================================= CREAR HOME SCREEN ==================================
    
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
            
            title =tk.Label(song_frame, text=title, fg="white", bg="#121212").pack(anchor="w")
            artist =tk.Label(song_frame, text=artist, fg="gray", bg="#121212").pack(anchor="w")
            album =tk.Label(song_frame, text=album, fg="gray", bg="#121212").pack(anchor="w")

            song_frame.pack(fill="x", padx=5, pady=5)
            
            song_frame.bind("<Button-1>", lambda e, f=song_frame, s=song: self.select_song(f, s))
            
            
            for widget in song_frame.winfo_children():
                widget.bind("<Button-1>", lambda e, f=song_frame, s=song: self.select_song(f, s))
            
            song_frame.bind("<MouseWheel>", self._on_mousewheel)
            song_frame.bind("<Button-4>", self._on_mousewheel)
            song_frame.bind("<Button-5>", self._on_mousewheel)
        
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

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
    
    def get_current_song(self):
        
        if self.active_playlist == None:
            songs = self.load_songs()["songs"]
            return songs
        else:
            with open(self.active_playlist, "r") as f:
                data = json.load(f)
                return data["songs"]
    
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
                
    ##================================ CARGAR A SCROLLABLE FRAME ==================================
    def load_info_tree(self):
        try:
            with open("titulos.json", "r") as file:
                self.datos = json.load(file)
        except FileNotFoundError:
            self.datos = {"songs": []}
    
    ##================================ CREAR LOAD_SCREEN ==================================
    
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
    ##================================ DRAG AND DROP ==================================
    
    def handle_drop(self, event):
        # event.data = la ruta del archivo arrastrado 
        # splitlist() convierte el formato para q sea legible 
        files = self.root.tk.splitlist(event.data)

        for file_path in files:
            # normaliza la ruta 
            normalized_path = os.path.normpath(file_path)

            if normalized_path.lower().endswith((".mp3", ".wav")):
                self.add_song(normalized_path)
            else:
                print(f"Formato no soportado: {normalized_path}")
    
            
    ##================================ CREAR PLAYLIST ==================================

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

    ##================================ CARGAR Y GUARDAR CANCIONES ==================================
    
    def load_file(self):
        file_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.mp3 *.wav")]
        )

        if file_path:
            self.add_song(file_path)
            
    def add_song(self,file_path):
        
        music_folder = "music"
        os.makedirs(music_folder, exist_ok=True)

        filename = os.path.basename(file_path)
        destination = os.path.join(music_folder, filename)

        # copia el archivo a la carpeta solo si no existe
        if not os.path.exists(destination):
            shutil.copy(file_path, destination)

        
        title, artist, album = self.get_song_info(destination)

        data = self.load_songs()
        song = {
            "path": destination,
            "name": filename,
            "title" : title,
            "artist": artist,
            "album" : album
        }

        if song not in data["songs"]:
            data["songs"].append(song)
            self.save_songs(data)
        
    def load_json(self):
        if not os.path.exists(self.json):
            with open(self.json, "w") as f:
                json.dump({"songs": []}, f)
            
    def load_songs(self):
        
        with open(self.json, "r") as f:
            return json.load(f)
    
    def save_songs(self, data):
        with open(self.json, "w") as f:
            json.dump(data, f, indent=4)
    
    
    ##================================ METADATA ==================================
    
    def get_song_info(self,destination):

        audio = EasyID3(destination)

        title = (audio.get("title",['Unknown'])[0])
        artist = audio.get("artist", ['Unknown'])[0]
        album = audio.get("album", ['Unknown'])[0]
       
        return title,artist,album
    
    ##================================ COVER ==================================
       
    def get_cover(self, path):
        cover_data = None
        try:
            audio_id3 = ID3(path)
            for tag in audio_id3.values():
                if tag.FrameID == "APIC":
                    cover_data = tag.data
                    break
        except Exception as e:
            print("No cover:", e)
        return cover_data
    
    def load_cover(self, path, size=50):
        cover_data = self.get_cover(path)

        try:
            if cover_data:
                img = Image.open(BytesIO(cover_data)).convert("RGB")
            else:
                raise Exception("No cover")

        except Exception:
            
            img = Image.open("cover/no_cover.png")
            

        img = img.resize((size, size), Image.LANCZOS)
        
        return ImageTk.PhotoImage(img)

root = tkdnd.Tk()
MusicPlayer(root)
root.mainloop()
