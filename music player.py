from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk

class MusicPlayer:
    def __init__(self,root):
        ##pallet colors
        self.root_bg = "gray20"
        self.menu_bg = "Indian Red3"
        ## Root configuration // title, size, not resizable, initial background color
        
        self.root = root
        self.root.title("Music Player")
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.configure(bg = self.root_bg)
        self.root.resizable(False, False)

        ##Load icons toggle
        self.menu_icon = ImageTk.PhotoImage(Image.open("menuicons/menu_icon.png"))
       
        #self.home_icon = PhotoImage(file= "menuicons/home_icon.png")
        
        #self.playlist_icon = PhotoImage(file= "menuicons/create_playlist_icon.png")
        
        #self.add_icon = PhotoImage(file= "menuicons/addfromfile_icon.png")
        
        ##Create sidebar frame
        
        self.menu_frame_bar = tk.Frame(self.root, bg = self.menu_bg)
        
        self.menu_frame_bar.pack(side = tk.LEFT, fill = tk.Y , pady= 10, padx= 10)
        
        self.menu_frame_bar.pack_propagate(0)
        
        self.menu_frame_bar.configure(width = 100)
        
        ##Toggle buttons
        
        toggle_menu = tk.Button(self.menu_frame_bar,
                                image= self.menu_icon,
                                command= self.toggle_menu,
                                bg = "Indian Red3",
                                activebackground = "Indian Red4",)
        
        toggle_menu.place(x=10, y=10)
    
    def toggle_menu(self):
        pass

root = tk.Tk()
MusicPlayer(root)
root.mainloop()



