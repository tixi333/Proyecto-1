import tkinter as tk

class Navigation:
    def create_sidebar(self):
        self.menu_frame_bar = tk.Frame(self.root, bg = self.menu_bg, width=100)
        self.menu_frame_bar.pack(side = tk.LEFT, fill = tk.Y , pady= 10, padx= 10)
        self.menu_frame_bar.pack_propagate(0)
        
        self.home_indicator = self.create_indicators(200)
        self.playlist_indicator = self.create_indicators(350)
        self.add_indicator = self.create_indicators(500)
        
        
        self.toggle_home = self.create_buttons(img = self.home_icon,
                                               cmd = lambda: self.switch_pages("home", self.home_indicator),
                                               y= 200)
        self.toggle_playlist = self.create_buttons(img = self.playlist_icon,
                                                   cmd = lambda: self.switch_pages("playlist", self.playlist_indicator),
                                                   y= 350)
        self.toggle_add = self.create_buttons(img = self.add_icon,
                                              cmd = lambda: self.switch_pages("load", self.add_indicator),
                                              y= 500)

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
    
