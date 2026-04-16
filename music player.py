import shutil
from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import tkinterdnd2 as tkdnd
import json, os
from mutagen.easyid3 import EasyID3

## 1
## add from file screen : + input artist, title, album, load cover manually
##                        + tinytag/mutagen for metadata (artist, title, album) and cover
## 2 interfaz
## add loaded songs at home screen
## 3 barra de progreso, play, pause, stop, next, previous

##Tkinterdnd - filedialog.askopenfilename()
class MusicPlayer:
    def __init__(self,root):
        
        #--------------------------------------------------------CONFIGURACION INICIAL--------------------------------------------------------
        ##pallet colors
        self.root_bg = "gray20"
        self.menu_bg = "PaleVioletRed3"
        self.tree_bg = "grey15"
        ## Root configuration // title, size, not resizable, initial background color
        
        self.root = root
        self.root.title("Music Player")
        
        #screen_width = self.root.winfo_screenwidth()
        #screen_height = self.root.winfo_screenheight()
        
        #self.root.geometry(f"{screen_width}x{screen_height}")
        #self.root.configure(bg = self.root_bg)
        #self.root.resizable(False, False)

        self.root.state("zoomed")
        self.root.configure(bg=self.root_bg)

        self.root.minsize(800, 600)
        
        # --------------------- INTERFACE FUNCTIONS ---------------------
        
        self.current_page = None
        self.json = "titulos.json"
        
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
        
        
        self.switch_pages("home", self.home_indicator)
        #lambda event pasa el evento como argumento aunque no se use o indique automaticamente
        
        
    def load_icons(self):
        def load(path):
            img = Image.open(path).resize((60, 60))
            return ImageTk.PhotoImage(img)

        self.menu_icon = load("menuicons/menu_icon.png")
        self.close_icon = load("menuicons/close_icon.png")
        self.home_icon = load("menuicons/home_icon.png")
        self.playlist_icon = load("menuicons/create_playlist_icon.png")
        self.add_icon = load("menuicons/addfromfile_icon.png")

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
                
    def show_labels(self):
        self.home_lb.place(x=90, y=220)
        self.playlist_lb.place(x=90, y=370)
        self.add_lb.place(x=90, y=520)
        
    def hide_labels(self):
        self.home_lb.place_forget()
        self.playlist_lb.place_forget()
        self.add_lb.place_forget()

    def reset_indicators(self):
        for indicator in [self.home_indicator, self.playlist_indicator, self.add_indicator]:
            indicator.configure(bg = self.menu_bg)
            
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
    
    def create_home_screen(self):
    
        frame = tk.Frame(self.page_frame, bg=self.root_bg)

        tk.Label(
            frame,
            text="Inicio",
            font=("Arial", 30, "bold"),
            bg=self.root_bg,
            fg="white"
        ).pack(pady=20)

        self.load_info_tree()
        self.tree_frame = tk.Frame(frame, bg = self.tree_bg, width= 400, height=400)
        self.tree_frame.pack(side = LEFT, fill = tk.Y, pady= 20, padx= 20)
        self.tree_frame.pack_propagate(False)

        columns = ["Path", "Title", "Artist", "Album"]
        self.tree = ttk.Treeview(self.tree_frame, columns = ("Path", "Title", "Artist", "Album"))
        
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.column('#0', width=0, stretch='no')
        self.tree.pack(side = LEFT,fill= tk.BOTH, ipadx= 10, ipady=10)
        
        return frame

    def load_info_tree(self):
        try:
            with open("titulos.json","r") as file:
                self.datos = json.load(file)

                print(len(self.datos["songs"]))

                for e in range(len(self.datos["songs"])):
                    path = (self.datos["songs"][e]["path"])
                    name = (self.datos["songs"][e]["name"])
                    
        except FileNotFoundError:
            self.datos = {}

    def create_playlist_screen(self):
    
        frame = tk.Frame(self.page_frame, bg=self.root_bg)

        tk.Label(
            frame,
            text="Crear Playlist",
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
    
    
    def load_file(self):
        file_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.mp3 *.wav")]
        )
        print(file_path)

        if file_path:
            self.add_song(file_path)

    def add_song(self,file_path):
        
        music_folder = "music"
        os.makedirs(music_folder, exist_ok=True)

        filename = os.path.basename(file_path)
        destination = os.path.join(music_folder, filename)

        print(destination)


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
            
    def get_song_info(self,destination):

        audio = EasyID3(destination)

        title = (audio.get("title",['Unknown'])[0])
        artist = audio.get("artist", ['Unknown'])[0]
        album = audio.get("album", ['Unknown'])[0]
        
        return title,artist,album

root = tkdnd.Tk()
MusicPlayer(root)
root.mainloop()
