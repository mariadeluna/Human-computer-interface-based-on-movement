#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pprint
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

import webbrowser
import pyautogui
from time import sleep
import tkinter as tk
from PIL import Image, ImageTk
from threading import Thread
import time
import os

# credenciales de Spotify, para poder interactuar con el API de spotify
# tener cuenta en Spotify developer
client_id = "c4db955a993341419e6aa39fcfe707e2"
client_secret = "1e46c178c2214a23beee507041c8a528"
redirect_uri = "http://localhost:8080/callback" 

# permisos necesarios para interactuar con spotify en el programa
scope = "user-library-read user-read-playback-state user-modify-playback-state user-read-playback-state"

# autorizar spotify con las credenciales de arriba
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_path="C:/Users/maria/.spotify_cache" # aquí se guarda la info del token
)

# Autenticación, primero busca si está almacenada ya en el caché
token_info = sp_oauth.get_cached_token()
if not token_info:
    # si el token todavía no se ha encontrado, mandar al usuario a que 
    # de el codigo de autorización con su cuenta de spotify
    auth_url = sp_oauth.get_authorize_url()
    print(f"Visita esta URL para autorizar: {auth_url}")
    auth_code = input("Introduce el código de autorización: ")
    token_info = sp_oauth.get_access_token(auth_code)

# pasar a cadena 
if isinstance(token_info, dict):
    access_token = token_info["access_token"]
else:
    access_token = token_info

# correcto inicio de spotify
sp = spotipy.Spotify(auth=access_token)

print("Autenticación completada correctamente.")


# authors + song list that are going to be displayed in the principal menu
songs_authors = [
    ("The Beatles", "Hey Jude"),
    ("Michael Jackson", "Billie Jean"),
    ("Bee Gees", "Stayin' Alive"),
    ("Earth, Wind & Fire", "September"),
    ("Don McLean", "American Pie"),
    ("Queen", "Bohemian Rhapsody")
]

# Obtain the URIs of the songs, unique strings (primary keys) of the songs
# that identifies the track
uris = []
for author, song in songs_authors:
    result = sp.search(f"{author} {song}", limit=1) # search in spotify fot the specified song (only 1)
    uri = result["tracks"]["items"][0]["uri"]
    uris.append(uri)

# principal menu where all the artist + song are shown
def music_aac():
    window = tk.Tk()
    window.title("Music Player")
    window.attributes('-fullscreen', True)  # full screen
    window.attributes('-topmost', True) # on top of other windows preventing to be hidden

    h_index = [0] # currently highlighted option
    buttons = [] # song options 
    
#update the highlight (yellow background) of the currently selected button
    def update_h():
        for i, btn in enumerate(buttons):
            if i == h_index[0]:
                btn.config(bg="yellow") #highlighted
            else:
                btn.config(bg="SystemButtonFace") #non selected 

#emulate the sequential scanning                 
    def select_next():
        # loop back to the first button
        h_index[0] = (h_index[0] + 1) % len(buttons)
        update_h()

        # when a click event occurs a song is selected and played
    def on_click(event=None):
        if h_index[0] < len(songs_authors):
            # selected and played a song in the given position
            selected_song = songs_authors[h_index[0]]
            selected_uri = uris[h_index[0]]
            print(f"Playing: {selected_song[1]} - {selected_song[0]}")
            
            webbrowser.open(selected_uri)  # abrir Spotify en el navegador

            # start to play the song, requires spotify to be open on the device
            os.system("start spotify://")
           # sleep(2)
            #pyautogui.press('enter')

            window.destroy()  # close principal menu 
            openControlGrid(selected_song[1])  # open the control window
        else:
            # closing the aac_music program and spotify app
            print("Cerrando aplicación y Spotify...")
            os.system("taskkill /F /IM spotify.exe")  # Cierra Spotify
            window.destroy()  

    # each song + author are represented as "buttons"
    rows = 3  
    cols = (len(songs_authors) + rows - 1) // rows  # necessary columns
    for i, (author, song) in enumerate(songs_authors):
        btn = tk.Button(window, text=f"{song} - {author}", width=30, height=3, font=("Arial", 20))
        btn.grid(row=i % rows, column=i // rows, padx=10, pady=10)
        
        buttons.append(btn)

    # close button
    close_button = tk.Button(window, text="Cerrar", width=30, height=3, bg="red", fg="black", font=("Arial", 20))
    close_button.grid(row=rows, column=0, columnspan=cols, pady=20)
    buttons.append(close_button)
    
#automatically scan, highlight option every 2 secs
    def auto_highlight():
        while True:
            time.sleep(2)
            select_next()
            
# start the sequential scanning as a separate thread
    Thread(target=auto_highlight, daemon=True).start()
    # daemon: The thread will run as a background process
    # Stops abruptly if the main program exits
    
    # attach an event handler to a specific event for the click event (left: button-1)
       # everytime the user clicks anywhere INSIDE the window th on_click function is triggered

    window.bind("<Button-1>", on_click)
    update_h()
    window.mainloop()

#control options, managing playback and displaying the current song
def openControlGrid(current_song):
    control_window = tk.Tk()
    control_window.title("Control Panel") # set the title on the control window
    control_window.attributes('-fullscreen', True)  
    control_window.attributes('-topmost', True)  
    #control_window.lift()

    # Load images for control options
    try:
        images = {
            "prev": ImageTk.PhotoImage(Image.open("./prev.png").resize((100, 100), Image.Resampling.LANCZOS)),
            "play_pause": ImageTk.PhotoImage(Image.open("./play_pause.png").resize((100, 100), Image.Resampling.LANCZOS)),
            "next": ImageTk.PhotoImage(Image.open("./next.png").resize((100, 100), Image.Resampling.LANCZOS)),
            "exit": ImageTk.PhotoImage(Image.open("./exit.png").resize((100, 100), Image.Resampling.LANCZOS)),
        }
    except Exception as e:
        print(f"Error loading images: {e}")
        return

    h_index2 = [0] # currently highlighted control button
    control_buttons = []

    # Display for the currently playing song
    song_display = tk.Label(
        control_window, text=f"Reproduciendo: {current_song}", font=("Arial", 24), anchor="center"
    )
    song_display.grid(row=0, column=0, columnspan=4, pady=20)

#  update the display with the current song that is being played on spotify
    def songDisplayUpdate():
        try:
            playback_state = sp.current_playback()
            if playback_state and playback_state["is_playing"]:
                current_song = playback_state["item"]["name"]
                # song + artist
                current_artist = ", ".join(artist["name"] for artist in playback_state["item"]["artists"])
                song_display.config(text=f"Reproduciendo: {current_song} -  {current_artist}")
            else:
                song_display.config(text="No hay canciones reproduciéndose")
        except Exception as e:
            print(f"Error updating song display: {e}")
            song_display.config(text="Error al sincronizar con Spotify")

    def updateControl_h():
        for i, btn in enumerate(control_buttons):
            if i == h_index2[0]:
                btn.config(bg="yellow")
            else:
                btn.config(bg="SystemButtonFace")

    def selectNextControl():
        h_index2[0] = (h_index2[0] + 1) % len(control_buttons)
        updateControl_h()

# handle left click + highlighted button selection        
    def clickControlOptions(event=None):
        option = h_index2[0]
        if option == 0:  # Previous song
            #print("Playing previous song...")
            sp.previous_track()
            songDisplayUpdate()
            
        elif option == 1:  # Play/Pause
           # print(" play/pause...")
            playback_state = sp.current_playback()
            if playback_state and playback_state["is_playing"]:
                sp.pause_playback()
            else:
                sp.start_playback()
            songDisplayUpdate()
        elif option == 2:  # Next song
           # print("Playing next song...")
            sp.next_track()
            songDisplayUpdate()
        elif option == 3:  # Exit
            print("Exiting control panel...")
            control_window.destroy()
            music_aac()  # Return to the main menu

    # Options for the control buttons
    options = [
        ("Anterior", images["prev"]),
        ("Play/Pause", images["play_pause"]),
        ("Siguiente", images["next"]),
        ("Atrás", images["exit"]),
    ]

    # Create buttons for the controls
    for i, (text, img) in enumerate(options):
        btn = tk.Button(control_window, text=text, image=img, compound="top", width=150, height=150, font=("Arial", 16))
        btn.grid(row=1, column=i, padx=20, pady=20)  # position on the screen
        control_buttons.append(btn)

        
#sequential scanning fot the control buttons
    def autoSelectControl():
        while True: #every 2 secs highlight
            time.sleep(2)
            selectNextControl()

    # Start automatic highlighting in a separate thread
    Thread(target=autoSelectControl, daemon=True).start()

    # every x time update the display in case a next/previous song is played
    def periodicDisplay():
        while True:
            time.sleep(3)  # update every 3 seconds
            songDisplayUpdate()

    Thread(target=periodicDisplay, daemon=True).start()

    # Bind click events to the control buttons
    control_window.bind("<Button-1>", clickControlOptions)
    songDisplayUpdate()  # Initial display update
    control_window.mainloop()



music_aac()


# In[ ]:





# In[ ]:




