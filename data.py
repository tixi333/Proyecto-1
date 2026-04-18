from tkinter import filedialog
import json, os
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3
from io import BytesIO
import shutil
from PIL import Image, ImageTk

class Data:
    def get_current_song(self):
        if self.active_playlist is None:
            songs = self.load_songs()["songs"]
            return songs
        else:
            with open(self.active_playlist, "r") as f:
                data = json.load(f)
                return data["songs"]

    def load_file(self):
        file_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.mp3 *.wav")]
        )

        if file_path:
            self.add_song(file_path)
    
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
    
    def load_info_tree(self):
        try:
            with open("titulos.json", "r") as file:
                self.datos = json.load(file)
        except FileNotFoundError:
            self.datos = {"songs": []}
            
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
