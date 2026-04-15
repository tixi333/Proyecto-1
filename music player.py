from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk

##Tkinterdnd - filedialog.askopenfilename()
class MusicPlayer:
    def __init__(self,root):
        ##pallet colors
        self.root_bg = "gray20"
        self.menu_bg = "PaleVioletRed3"
        ## Root configuration // title, size, not resizable, initial background color
        
        self.root = root
        self.root.title("Music Player")
        
        #screen_width = self.root.winfo_screenwidth()
        #screen_height = self.root.winfo_screenheight()
        
        #self.root.geometry(f"{screen_width}x{screen_height}")
        #self.root.configure(bg = self.root_bg)
        #self.root.resizable(False, False)

        self.root.state("zoomed")  # mejor que geometry full screen
        self.root.configure(bg=self.root_bg)

        self.root.minsize(800, 600)
        
        ##Load icons toggle
        menu_icon = Image.open("menuicons/menu_icon.png")
        menu_icon = menu_icon.resize((60,60))
        self.menu_icon = ImageTk.PhotoImage(menu_icon)
        
        close_icon = Image.open("menuicons/close_icon.png")
        close_icon = close_icon.resize((60,60))
        self.close_icon = ImageTk.PhotoImage(close_icon)
        
        home_icon = Image.open("menuicons/home_icon.png")
        home_icon = home_icon.resize((60,60))
        self.home_icon = ImageTk.PhotoImage(home_icon)
        
        playlist_icon = Image.open("menuicons/create_playlist_icon.png")
        playlist_icon = playlist_icon.resize((60,60))
        self.playlist_icon = ImageTk.PhotoImage(playlist_icon)
        
        add_icon = Image.open("menuicons/addfromfile_icon.png")
        add_icon = add_icon.resize((60,60))
        self.add_icon = ImageTk.PhotoImage(add_icon)
        
        ##Create sidebar frame
        
        self.menu_frame_bar = tk.Frame(self.root, bg = self.menu_bg)
        
        self.menu_frame_bar.pack(side = tk.LEFT, fill = tk.Y , pady= 10, padx= 10)
        
        self.menu_frame_bar.pack_propagate(0)
        
        self.menu_frame_bar.configure(width = 100)
        
        ## Indicators Labels
        
        self.home_indicator = tk.Label(self.menu_frame_bar, bg = self.menu_bg)
        self.home_indicator.place(x=5, y=345, width=7, height=70)
        
        self.playlist_indicator = tk.Label(self.menu_frame_bar, bg = self.menu_bg)
        self.playlist_indicator.place(x=5, y=495, width=7, height=70)
        
        self.add_indicator = tk.Label(self.menu_frame_bar, bg = self.menu_bg)
        self.add_indicator.place(x=5, y=645, width=7, height=70)
        ## Frames
        
        self.home_frame = tk.Frame(self.root, bg = self.root_bg)
        #self.home_frame.pack(fill = tk.BOTH, expand = True)
        
        self.playlist_frame = tk.Frame(self.root, bg = self.root_bg)
        #self.playlist_frame.pack(fill = tk.BOTH, expand = True)
        
        self.add_frame = tk.Frame(self.root, bg = self.root_bg)
        #self.add_frame.pack(fill = tk.BOTH, expand = True)
        
        ##Buttons
        
        self.menubtn = tk.Button(self.menu_frame_bar,
                                image= self.menu_icon,
                                command= self.toggle_menu,
                                bg = self.menu_bg,
                                activebackground = self.menu_bg,
                                bd =0)
        
        self.menubtn.status = "closed"
        
        self.menubtn.place(x=15, y=15)
        
        self.toggle_home = tk.Button(self.menu_frame_bar,
                                image= self.home_icon,
                                command= lambda: [self.switch_indicator(indicator= self.home_indicator, page= self.home_screen)],
                                bg = self.menu_bg,
                                activebackground = self.menu_bg,
                                bd =0)
        
        self.toggle_home.place(x=15, y=350)
        
        self.toggle_playlist = tk.Button(self.menu_frame_bar,
                                image= self.playlist_icon,
                                command= lambda: [self.switch_indicator(indicator= self.playlist_indicator, page= self.create_playlist_screen)],
                                bg = self.menu_bg,
                                activebackground = self.menu_bg,
                                bd =0)
        
        self.toggle_playlist.place(x=15, y=500)
        
        self.toggle_add = tk.Button(self.menu_frame_bar,
                                image= self.add_icon,
                                command= lambda: [self.switch_indicator(indicator= self.add_indicator, page= self.load_screen)],
                                bg = self.menu_bg,
                                activebackground = self.menu_bg,
                                bd =0)
        
        self.toggle_add.place(x=15, y=650)
    
    ## Labels

        self.home_lb = tk.Label(self.menu_frame_bar,font = ("Arial", 20, "bold"), text= "Home", bg = self.menu_bg, fg = "black")
        
        self.home_lb.bind("<Button-1>", lambda event: self.switch_indicator(indicator= self.home_indicator,
                                                                            page= self.home_screen))
        
        self.playlist_lb = tk.Label(self.menu_frame_bar, font = ("Arial", 20, "bold"), text= "Create playlist", bg = self.menu_bg, fg = "black")
        self.playlist_lb.bind("<Button-1>", lambda event: self.switch_indicator(indicator= self.playlist_indicator,
                                                                                page= self.create_playlist_screen))
        
        self.add_lb = tk.Label(self.menu_frame_bar, font = ("Arial", 20, "bold"), text= "Add from file", bg = self.menu_bg, fg = "black")
        self.add_lb.bind("<Button-1>", lambda event: self.switch_indicator(indicator= self.add_indicator, 
                                                                           page= self.load_screen))
        
        #lambda event pasa el evento como argumento aunque no se use o indique automaticamente
        ### Page frame
    
        self.page_frame = tk.Frame(self.root, bg = self.root_bg)
        self.page_frame.pack(fill = tk.BOTH, expand = True)
        
        self.home_screen()
    
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
        self.home_lb.place(x=90, y=370)
        self.playlist_lb.place(x=90, y=515)
        self.add_lb.place(x=90, y=665)
        
    def hide_labels(self):
        self.home_lb.place_forget()
        self.playlist_lb.place_forget()
        self.add_lb.place_forget()

    def manage_pages(self, page):
        pass
    
    def home_screen(self):
        
        
        screen_page = tk.Frame(self.page_frame, bg =self.root_bg)
        
        lb_provisorio = tk.Label(screen_page, text = "Home Screen", font = ("Arial", 30, "bold"), bg = self.root_bg, fg = "white")
        lb_provisorio.pack(pady= 20)
        
        screen_page.pack(fill = tk.BOTH, expand = True)
    
    def create_playlist_screen(self):
        
        playlist_page = tk.Frame(self.page_frame, bg = self.root_bg)
        
        lb_provisorio = tk.Label(playlist_page, text = "Create playlist Screen", font = ("Arial", 30, "bold"), bg = self.root_bg, fg = "white")
        lb_provisorio.pack(pady= 20)
        
        playlist_page.pack(fill = tk.BOTH, expand = True)
    
    def load_screen(self):
        
        load_page = tk.Frame(self.page_frame, bg = self.root_bg)
        
        lb_provisorio = tk.Label(load_page, text = "Add from file Screen", font = ("Arial", 30, "bold"), bg = self.root_bg, fg = "white")
        lb_provisorio.pack(pady= 20)
        
        load_page.pack(fill = tk.BOTH, expand = True)
        
root = tk.Tk()
MusicPlayer(root)
root.mainloop()



