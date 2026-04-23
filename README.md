# Reproductor de música

Este proyecto es un reproductor de música con interfaz gráfica hecho con tkinter.

## Características

- Cargar canciones con formato mp3 
- Crear playlists personalizadas
- Barra de progreso interactiva
- Modos de reproducción (Shuffle - Loop)
- Reproducción, pausa y cambio de canciones

### Tecnologías utilizadas

- Python
- Tkinter (interfaz gráfica)
- pygame (reproducción de audio)
- mutagen (metadata de canciones)
- pillow (manejo de imágenes)
- tkinterdnd2 (drag & drop)
- fuzzywuzzy (búsqueda de canciones)

### Dependencias

- pygame (reproducción de audio)
- pygame-widgets (componentes interactivos)
- mutagen (metadata de canciones)
- pillow (manejo de imágenes)
- tkinterdnd2 (drag & drop)

### Estructura del proyecto

```plaintext
proyecto-1/
│── app.py
│── main.py
│── requirements.txt
│── README.md
│── data.py
│── titulos.json
│── commits.txt
│
├── cover/            # Imágenes de portada de canciones        
├── menuicons/        # Iconos del menú
├── music/            # Canciones (MP3)
├── playlists/        # Playlists guardadas
├── songicons/        # Iconos del reproductor
│   ├── play.png
│   ├── pause.png
│   ├── stop.png
│   ├── shuffle-on.png
│   ├── shuffle-off.png
│   ├── loop-on.png
│   ├── loop-off.png
│   ├── angulo-derecho.png
│   └── angulo-izquierdo.png
│
├── ui_navigation.py  # Navegación entre pantallas
├── ui_playerbar.py   # Barra de reproducción
└── ui_screens.py     # Pantallas principales
```
