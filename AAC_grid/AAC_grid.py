#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from threading import Thread
import time
from PIL import Image, ImageTk 
import winsound  # beep

# Tkinter is used to build basic GUI applications
def start_tkinter():
    # main and unique window
    root = tk.Tk()
    root.title("AAC Grid")

    # window dimension
    root.geometry("700x500")  
    # can be modified
    root.resizable(True, True) 

    # symbols + images
    symbols = [
        {"name": "Jugar", "image": "play.png"},
        {"name": "Comer", "image": "eat.png"},
        {"name": "Beber", "image": "drink.png"},
        {"name": "Dormir", "image": "sleep.png"},
        {"name": "Música", "image": "music.png"},
        {"name": "Baño", "image": "bathroom.png"},
        {"name": "Ayuda", "image": "help.png"},
        {"name": "Dibujar", "image": "draw.png"}
    ]
    buttons = []
    images = []  
    highlighted_index = [0]  # list with a single element, tracks which button is highlighted
    
    # show the selection in a text area
    text_area = tk.Text(root, height=10, width=70)
    text_area.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

    # indicate that a button is highlighted (yellow background)
    def update_highlight():
        for i, btn in enumerate(buttons):
            if i == highlighted_index[0]:
                btn.config(bg="yellow")  # highlight
            else:
                btn.config(bg="SystemButtonFace")  # default system color to the rest of the buttons

    # emulate the sequential scanning, move to the next button
    def select_next():
        # increment the index, % len(symbols) ensures circular scanning when reaching the last button
        highlighted_index[0] = (highlighted_index[0] + 1) % len(symbols)
        update_highlight()

    def send_tap():     
        # name of the selected symbol
        selected_symbol = symbols[highlighted_index[0]]["name"]
        
        # display the selection in the text area
        text_area.insert(tk.END, f"{selected_symbol}\n")  # "history"
        text_area.see(tk.END)  

        # Emit a beep sound when a symbol is selected
        winsound.Beep(1000, 300)  # Beep once per selection

    # Create the images in the buttons
    for i, symbol in enumerate(symbols):
        try:
            img = Image.open(symbol["image"])  # Load image
            img = img.resize((50, 50), Image.Resampling.LANCZOS)  # size of the image
            photo = ImageTk.PhotoImage(img)
            images.append(photo)  # image reference
        except Exception as e:
            print(f"Error loading image for {symbol['name']}: {e}")
            photo = None  # don't show any picture

        # buttons + distribution (4 columns and 2 rows)
        btn = tk.Button(root, text=symbol["name"], image=photo, compound="top", width=100, height=100)
        btn.grid(row=i // 4, column=i % 4, padx=10, pady=10)
        buttons.append(btn)

    # first highlight
    update_highlight()

    # sequential scanning automated every x seconds
    def auto_select():
        while True:
            time.sleep(3)  # can be modified depending on the user capabilities
            select_next()

    # detection of a click in any part of the window
    def on_screen_click(event):
        send_tap()
    root.bind("<Button-1>", on_screen_click)

    # automatically sequential scanning (background execution)
    auto_thread = Thread(target=auto_select, daemon=True)
    auto_thread.start()

    # window is open
    root.mainloop()

# run independently of other logic or code outside the Tkinter application
tk_thread = Thread(target=start_tkinter)
tk_thread.daemon = True
tk_thread.start()

print("Grid execution started")


# In[ ]:




