#!/usr/bin/env python
# coding: utf-8

# In[13]:


import tkinter as tk
from threading import Thread, Event
import time
from PIL import Image, ImageTk
import winsound  # "beep" sound everytime a selection is made in the subgrids
import subprocess  # execcutes the music app in a different script


# Grids (subgrids) for different environments
grids = {
    "Casa": [
        {"name": "Comer", "image": "eat.png"},
        {"name": "Beber", "image": "drink.png"},
        {"name": "Baño", "image": "bathroom.png"},
        {"name": "Dormir", "image": "sleep.png"},
        {"name": "Jugar", "image": "play.png"},
        {"name": "Ayuda", "image": "help.png"}
    ],
    "Doctor": [
        {"name": "Dolor", "image": "pain.png"},
        {"name": "Medicina", "image": "medicine.png"},
        {"name": "Bien", "image": "good.png"},
        {"name": "Mal", "image": "bad.png"},
        {"name": "Casa", "image": "home.png"},
        {"name": "Ayuda", "image": "help.png"}
    ],
    "Social": [
        {"name": "Hola", "image": "hello.png"},
        {"name": "Adiós", "image": "goodbye.png"},
        {"name": "Gracias", "image": "thankyou.png"},
        {"name": "Sí", "image": "yes.png"},
        {"name": "No", "image": "no.png"},
        {"name": "Lo siento", "image": "sorry.png"}
    ],
    "Comida": [
        {"name": "Comer", "image": "eat.png"},
        {"name": "Beber", "image": "drink.png"},
        {"name": "Terminar", "image": "done.png"},
        {"name": "Gustar", "image": "like.png"},
        {"name": "No gustar", "image": "dislike.png"},
        {"name": "Ayuda", "image": "help.png"}
    ],
    "Ocio": [
        {"name": "Música", "image": "music.png"},
        {"name": "TV", "image": "tv.png"},
        {"name": "Juego", "image": "play.png"},
        {"name": "Libro", "image": "book.png"},
        {"name": "Dibujar", "image": "draw.png"},
        {"name": "Puzzle", "image": "puzzle.png"}
    ]
}

# List storing images for each subgrid
global_images = {}

# automatic and sequential scanning (main thread)
# delay of 3000 milliseconds
def autoHighlight(buttons, h_index, update_h, delay=3000):
    def h_next():
        h_index[0] = (h_index[0] + 1) % len(buttons) # move to next button
        update_h() #update appearance (yellow/normal)
        
        # next highlight 
        buttons[0].after(delay, h_next)

    h_next() # start the highlight process
    
# create a new window for the selected enviroment (subgrid)

def subGrid(enviro, stop_event_main):    
    subgrid_window = tk.Toplevel() # the window must be in front of the other one
    subgrid_window.title(f"AAC - {enviro}")
    subgrid_window.attributes('-topmost', True)
    subgrid_window.attributes('-fullscreen', True)
    #subgrid_window.geometry("500x500")

    grid_pictograms = grids[enviro] # pictograms of the selected subgrid
    buttons = [] #number of options (buttons)
    h_index = [0] # currently highlighted
    
    #automatic highlighting
    stopEventSubgrid = Event() 

    # load images into the global if they were not there
    if enviro not in global_images:
        global_images[enviro] = []
        for symbol in grid_pictograms:
            try:
                img = Image.open(symbol["image"]).resize((120, 120), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                global_images[enviro].append(photo)
            except Exception as e:
                print(f"Error cargando {symbol['name']}: {e}")
                global_images[enviro].append(None)

    # everytime a button is selected the text appears 
    # create an hsistory record of the selected buttons
    selection_display = tk.Text(subgrid_window, height=5, width=40)
    selection_display.grid(row=len(grid_pictograms) // 3 + 1, column=0, columnspan=3, padx=10, pady=10)

    # yellow scanning
    def update_h():
        for i, btn in enumerate(buttons):
            if i == h_index[0]:
                btn.config(bg="yellow")
            else:
                btn.config(bg="SystemButtonFace")

    # move to next button in the grid
    def nextSelection():
        h_index[0] = (h_index[0] + 1) % (len(grid_pictograms) + 1)
        update_h()

    # everytime a clic is made in any part of the screen an option is selected
    # the option appears on the display and a sound is emitted to confirm the selection
    def on_select(event=None):
        if h_index[0] < len(grid_pictograms):
            selected_symbol = grid_pictograms[h_index[0]]["name"]
            selection_display.insert(tk.END, f"{selected_symbol}\n")
            selection_display.see(tk.END)
            winsound.Beep(1000, 300)
            
            # If music options is selected, start the music_aac app 
            if selected_symbol == "Música":
                music_app()
                
        #exiting the subgrid when the exit button is selected
        else:
            stopEventSubgrid.set()
            subgrid_window.destroy()

    # create buttons appearance for the pictograms in the subgrids
    for i, symbol in enumerate(grid_pictograms):
        btn = tk.Button(subgrid_window, text=symbol["name"], image=global_images[enviro][i], compound="top", width=150, height=150,anchor="center", font=("Comic Sans MS", 12))
        btn.grid(row=i // 3, column=i % 3, padx=10, pady=10)
        buttons.append(btn)

    # exit button
    exit_button = tk.Button(subgrid_window, text="Exit", font=("Comic Sans MS", 12),bg="white", fg="black", width=15, height=2, command=lambda: subgrid_window.destroy())
    exit_button.grid(row=len(grid_pictograms) // 3 + 2, column=0, columnspan=3, pady=10)
    buttons.append(exit_button)

    # using the functions to automate the subgrid scanning
    autoHighlight(buttons, h_index, update_h)
    subgrid_window.bind("<Button-1>", on_select) # Bind click event to selection
    update_h()

# Call the music app as a separate process
def music_app():
    subprocess.Popen(["python", "AAC_music.py"])    

    
# main menu with all the environment options    
def mainMenu():
    principal = tk.Tk()
    principal.title("AAC Pictogramas")
    #principal.geometry("500x400")
    principal.attributes('-fullscreen', True)
    principal.attributes('-topmost', True)

    buttons = []
    h_index = [0]
    stop_event_main = Event()

    # Function to update button highlights (main menu)
    def update_h():
        for i, btn in enumerate(buttons):
            if i == h_index[0]:
                btn.config(bg="yellow")
            else:
                btn.config(bg="SystemButtonFace")

    # move to the next button (main menu)
    def nextSelection():
        h_index[0] = (h_index[0] + 1) % len(grids)
        update_h()

    #  button selection (main menu)
    def on_select(event=None):
        if h_index[0] < len(grids):
            selected_grid = list(grids.keys())[h_index[0]]
            print(f"Seleccionado: {selected_grid}")
            subGrid(selected_grid, principal)
        elif h_index[0] == len(grids):  # Close the program if "Cerrar" is highlighted
            principal.destroy()

    # create buttons for the main menu options
    for i, enviro in enumerate(grids.keys()):
        btn = tk.Button(principal, text=enviro, width=20, height=3, font=("Comic Sans MS", 16))
        buttons.append(btn)
        
    # close button to exit the program
    close_button = tk.Button(principal, text="Cerrar", bg="red", fg="black", font=("Comic Sans MS", 16), width=20, height=3)
    #close_button.config(command=principal.destroy)
    buttons.append(close_button)

    # Center the buttons in the grid
    rows, cols = 3, 2  # Define rows and columns for the layout
    total_buttons = len(buttons)
    for i, btn in enumerate(buttons):
        row = i // cols
        col = i % cols
        btn.grid(row=row, column=col, padx=20, pady=20)

    # Adjust the grid size to center the buttons
    for col in range(cols):
        principal.grid_columnconfigure(col, weight=1)
    for row in range((total_buttons + cols - 1) // cols):
        principal.grid_rowconfigure(row, weight=1)

   # def closeProgram(event=None):
   #     principal.destroy()
    
    
   # principal.bind("<Button-1>", closeProgram)  # Bind click to exit

        
    # automatic scanning in the main menu
    autoHighlight(buttons, h_index, update_h)

    principal.bind("<Button-1>", on_select)
    update_h()
    principal.mainloop()


if __name__ == "__main__":
    mainMenu()


   


# In[ ]:




