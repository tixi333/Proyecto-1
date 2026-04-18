import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
import pygame

from ui_navigation import Navigation
from ui_playerbar import PlayerBar
from ui_screens import Screens
from data import Data


class MusicPlayer(Navigation, PlayerBar, Screens, Data):
    def __init__(self,root):
        
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
        self.menu_animation_job = None
        self.menu_labels_visible = False
        self.label_animation_jobs = []
        self.song_render_jobs = []

        self.load_json()
        self.load_icons()

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
