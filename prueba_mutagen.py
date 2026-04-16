from mutagen.easyid3 import EasyID3

# Load the MP3 file
audio = EasyID3("loaded/Kevin MacLeod - Early Riser.mp3")

# Access common tags (returns a list)
print(f"Title: {audio.get('title', ['Unknown'])[0]}")
print(f"Artist: {audio.get('artist', ['Unknown'])[0]}")
print(f"Album: {audio.get('album', ['Unknown'])[0]}")

# List all available tags in the file
print(audio.keys())