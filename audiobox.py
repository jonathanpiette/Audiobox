#!/usr/bin/env python3

import os
import board
from adafruit_pn532.i2c import PN532_I2C
import pygame
import threading
import time
import RPi.GPIO as GPIO

# Configuration
CLK_PIN = 18
DT_PIN = 17
SW_PIN = 27

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup([CLK_PIN, DT_PIN, SW_PIN], GPIO.IN, pull_up_down=GPIO.PUD_UP)
print("GPIO pins configured.")

# Set working directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Initialize PN532
i2c = board.I2C()
pn532 = PN532_I2C(i2c)
print("PN532 initialized.")

# Configure PN532
pn532.SAM_configuration()

# Load audio map
def load_audio_map():
    audio_map = {}
    try:
        with open('audio_map.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                tag_id, audio_file = line.strip().split(',')
                audio_map[tag_id] = audio_file
    except FileNotFoundError:
        print("Fichier audio_map.txt introuvable.")
        print("Le fichier sera créé lors de l'association de tags NFC avec des fichiers audio.")
    return audio_map

# Enregistrer la liste des musiques associées aux tags NFC dans le fichier audio_map.txt
def save_audio_map(audio_map):
    with open('audio_map.txt', 'w') as file:
        for tag_id, audio_file in audio_map.items():
            file.write(f"{tag_id},{audio_file}\n")

# Charger la liste des musiques associées aux tags NFC
nfc_audio_map = load_audio_map()
print("Audio map loaded.")

# Initialize Pygame mixer
def initialize_pygame_mixer():
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.5)  # Set default volume
    
last_CLK_state = GPIO.input(CLK_PIN)

# Play audio
def play_audio(file_path):
    music_folder = os.path.join(dname, 'musics')
    audio_file_path = os.path.join(music_folder, file_path)
    print("Playing audio:", audio_file_path)
    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.play()

# Stop audio
def stop_audio():
    pygame.mixer.music.stop()

# Volume control
def volume_control(channel):
    global last_CLK_state
    CLK_state = GPIO.input(CLK_PIN)
    DT_state = GPIO.input(DT_PIN)
    print("Volume control event detected.")
    print("CLK:", CLK_state)
    print("DT:", DT_state)
    if CLK_state != last_CLK_state:
        if DT_state != CLK_state:
            pygame.mixer.music.set_volume(min(pygame.mixer.music.get_volume() + 0.1, 1.0))
            print("Volume increased:", pygame.mixer.music.get_volume())
        else:
            pygame.mixer.music.set_volume(max(pygame.mixer.music.get_volume() - 0.1, 0.0))
            print("Volume decreased:", pygame.mixer.music.get_volume())
    last_CLK_state = CLK_state

# Set up switch pin
GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
print("Switch pin configured.")

# Switch press event
def switch_pressed(channel):
    print("Switch pressed!")

# Remove existing event detection for the switch pin
GPIO.remove_event_detect(SW_PIN)

# Attach switch press event
GPIO.add_event_detect(SW_PIN, GPIO.FALLING, callback=switch_pressed, bouncetime=300)
print("Switch event attached to pin.")

# Attach volume control event
GPIO.add_event_detect(CLK_PIN, GPIO.FALLING, callback=volume_control, bouncetime=50)
print("Volume control attached to pins.")

# NFC tag scanning
def scan_nfc_tag():
    try:
        tag_id = pn532.read_passive_target(timeout=0.5)
        if tag_id is not None:
            # Convert the bytearray to a hex string
            return bytes(tag_id).hex()
    except RuntimeError as e:
        print("Erreur lors de la lecture du tag NFC:", e)
        print("Assurez-vous que le module PN532 est correctement connecté et que l'étiquette NFC est à proximité.")
        return None

# Check if a file is an MP3 file
def is_mp3_file(filename):
    return filename.lower().endswith('.mp3')

# Music files
music_folder = os.path.join(dname, 'musics')
music_files = [file for file in os.listdir(music_folder) if is_mp3_file(file)]

# Variables for tracking the last scanned tag and time
last_tag_id = None
last_tag_time = 0

# NFC thread
def check_nfc_thread():
    global last_tag_id, last_tag_time
    
    # Initialiser Pygame mixer avant de démarrer le thread
    initialize_pygame_mixer()

    while True:
        tag_id = scan_nfc_tag()
        if tag_id:
            current_time = time.time()
            if last_tag_id == tag_id and current_time - last_tag_time < 5:
                # Même tag NFC détecté dans les 5 secondes, ignorer
                continue
            else:
                last_tag_id = tag_id
                last_tag_time = current_time
                if tag_id in nfc_audio_map:
                    audio_file_path = nfc_audio_map[tag_id]
                    stop_audio()
                    play_audio(audio_file_path)
                else:
                    print("Aucun fichier audio associé à ce tag NFC.")
        else:
            # Aucun tag NFC détecté, réinitialiser les variables
            last_tag_id = None
            last_tag_time = 0

# Lancer le thread pour vérifier les tags NFC
nfc_thread = threading.Thread(target=check_nfc_thread, daemon=True)
nfc_thread.start()

try:
    # Boucle principale pour que le script continue de s'exécuter
    while True:
        pass

except KeyboardInterrupt:
    # Arrêter le thread NFC en cas d'interruption (Ctrl+C)
    nfc_thread.join()
    # Enregistrer la liste des musiques associées aux tags NFC dans le fichier audio_map.txt avant de quitter
    save_audio_map(nfc_audio_map)
    GPIO.cleanup()
