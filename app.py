import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageDraw, ImageTk
import pygame

from ui_navigation import Navigation
from ui_playerbar import PlayerBar
from ui_screens import Screens
from data import Data


class MusicPlayer(Navigation, PlayerBar, Screens, Data):
    def __init__(self,root):
        
        # color
        self.root_bg = "black"
        self.menu_bg = "PaleVioletRed3"
        self.tree_bg = "black"
        
        #root config
        self.root = root
        self.root.title("Music Player")

        self.root.state("zoomed")
        self.root.configure(bg=self.root_bg)

        self.root.minsize(800, 600)

        #
        pygame.mixer.init()

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.current_page = None
        self.json = "titulos.json"

        
        #selected song verificaciones
        self.selected_song = None
        self.selected_song_frame = None
        self.selected_song_label = None
        self.selected_song_cover = None

        self.is_paused = False
        self.is_playing = False
        self.current_path = None
        self.current_index = -1

        #playlist verificacion
        self.active_playlist = None

        self.song_frames = {}
 
        self.song_render_jobs = []
        
        #barra de progreso selected song
        self.progress_value = tk.DoubleVar(value=0)
        self.total_seconds = 0
        self.progress_job = None
        self.playback_offset = 0
        
        self.current_time_var = tk.StringVar(value="0:00")
        self.total_time_var = tk.StringVar(value="0:00")

        #volumen
        self.volume_value = tk.DoubleVar(value=70)

        #modos
        self.shuffle_enabled = False
        self.loop_enabled = False
        self.current_mode = None

        self.playlist_selected_songs = []
        self.home_song_search_var = tk.StringVar()
        self.saved_playlist_search_var = tk.StringVar()
        self.available_song_search_var = tk.StringVar()
        self.selected_playlist_search_var = tk.StringVar()

        self.load_json()
        self.load_icons()

        pygame.mixer.music.set_volume(self.volume_value.get() / 100)

        self.create_sidebar()

        self.page_frame = tk.Frame(self.root, bg=self.root_bg)
        self.page_frame.pack(fill=tk.BOTH, expand=True)

        self.screens = {
            "home": self.create_home_screen(),
            "playlist": self.create_playlist_screen(),
            "load": self.create_load_screen()
        }

        self.create_song_bar()

        self.switch_pages("home", self.home_indicator)
        
        

    def load_icons(self):
        def load(path, size):
            img = Image.open(path).resize((size, size))
            return ImageTk.PhotoImage(img)

        self.menu_icon = load("menuicons/menu_icon.png", 60)
        self.close_icon = load("menuicons/close_icon.png", 60)
        self.home_icon = load("menuicons/home_icon.png", 60)
        self.playlist_icon = load("menuicons/create_playlist_icon.png", 60)
        self.add_icon = load("menuicons/addfromfile_icon.png", 60)

        self.play_icon = load("songicons/play.png", 40)
        self.pause_icon = load("songicons/pausa.png", 40)
        self.next_icon = load("songicons/angulo-derecho.png", 40)
        self.previous_icon = load("songicons/angulo-izquierdo.png", 40)
        
        self.stop_icon = load("songicons/stop.png",40)
        self.shuffle_on = load("songicons/shuffle-on.png",40)
        self.shuffle_off = load("songicons/shuffle-off.png",40)
        self.loop_on = load("songicons/loop-on.png",40)
        self.loop_off = load("songicons/loop-off.png",40)

        
