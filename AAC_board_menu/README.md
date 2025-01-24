The **AAC_board_menu** is a python program that simulates a user-friendly interface that contains different pictograms collected or organized by **"environments"** (Casa, Doctor, Social, Ocio...). Each environment contains a grid with **pictograms** (simulating buttons) that are sequentially highlighted. 
Each time a **click** is made in the window, the program interprets it as a **selection** of the button that is highlighted at that exact moment.

An extra functionallity is added to this grid, that is the **aac_music** program. There are two different envioronments that contain a **"Música"** button in the grid these are **"Casa"** and **"Ocio"**, when this option is selected the module connects to **Spotify** via its API. With the same sequential scanning logic, it allows the user to play pre-defined songs. It also opens a **control panel** to manage playback.

This program only was tested on **Windows** os, it contains dependencies like **pyautogui** and uses specific system commands such as **os.system**.

**Requirements**
- As the program is written in Python requires it to be installed
- Internet connection for Spotify use
- All the required libraries (spotipy, tkinter, pillow, pyautogui, winsound...) must be installed using the "pip install " command in the terminal.
  
**Spotify API Credentials**
To use the music app a previous configuration must be done the first time is being used:
**Spotify Premium account is mandatory and the desktop app must be installed**
  1. Sing up in Spotify for Developers (https://developer.spotify.com/)
  2. Create a new app to obtain: Client ID and Client Secret
  3. Choose and add a Redirect URI (URL where Spotify will send the authorization response). For local testing: "http://localhost:8080/callback" (Use a free port)
  4. Update the variables (client_id, client_secret, and redirect_uri) in the AAC_music code
  5. Follow the instructions for Spotify authentication if running for the first time
     

**Run the program**
1. Download the project folder ensuring AAC_board_menu.py and AAC_music.py are in the **same directory**
2. Open the terminal and navigate to the project directory (cd C:/...)
3. Run the main program (python **AAC_board_menu.py**)
4. Once is open, use it as an AAC communication board.
5. To access the **Music App** select the "Música" option in the "Casa" or "Ocio" environment, be sure that the spotify desktop app is installed and running on the system

