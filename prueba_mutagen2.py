from mutagen.id3 import ID3

def get_mp3_cover(file_path):
    try:
        tags = ID3(file_path)
        # APIC is the tag key for album art
        # It can have multiple frames; usually we want the first one
        apic_frames = tags.getall("APIC")
        
        if apic_frames:
            cover = apic_frames[0]
            mime_type = cover.mime  # e.g., 'image/jpeg'
            image_data = cover.data  # Binary image data
            
            print(f"Found cover with MIME type: {mime_type}")
            return image_data, mime_type
        else:
            print("No cover art found.")
            return None, None
            
    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None

# Example usage
data, mime = get_mp3_cover("loaded/Kevin MacLeod - Early Riser.mp3")
if data:
    with open("cover_extracted.jpg", "wb") as f:
        f.write(data)