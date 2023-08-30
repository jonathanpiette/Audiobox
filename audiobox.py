#!/usr/bin/env python3

import os
import board
from adafruit_pn532.i2c import PN532_I2C
import pygame
import threading
import time

# Set the working directory to the script's directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Créer une instance de la classe PN532 en utilisant I2C
i2c = board.I2C()
pn532 = PN532_I2C(i2c)

# Initialiser la communication avec le PN532
pn532.SAM_configuration()

# Charger la liste des musiques associées aux tags NFC à partir du fichier audio_map.txt
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

# Charger la liste des musiques associées aux tags NFC
nfc_audio_map = load_audio_map()

# Enregistrer la liste des musiques associées aux tags NFC dans le fichier audio_map.txt
def save_audio_map(audio_map):
    with open('audio_map.txt', 'w') as file:
        for tag_id, audio_file in audio_map.items():
            file.write(f"{tag_id},{audio_file}\n")

# Fonction pour initialiser Pygame mixer
def initialize_pygame_mixer():
    pygame.mixer.init()

# Fonction pour jouer le fichier audio
def play_audio(file_path):
    music_folder = os.path.join(dname, 'musics')
    audio_file_path = os.path.join(music_folder, file_path)
    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.play()

# Fonction pour arrêter la lecture audio
def stop_audio():
    pygame.mixer.music.stop()

# Fonction pour scanner un tag NFC
def scan_nfc_tag():
    try:
        tag_id = pn532.read_passive_target(timeout=0.5)
        if tag_id is not None:
            return bytes(tag_id).hex()  # Convert the bytearray to a hex string
    except RuntimeError as e:
        print("Erreur lors de la lecture du tag NFC:", e)
        print("Assurez-vous que le module PN532 est correctement connecté et que l'étiquette NFC est à proximité.")
        return None

# Vérifier si un fichier est un fichier MP3
def is_mp3_file(filename):
    return filename.lower().endswith('.mp3')

# Liste des musiques dans le dossier 'musics'
music_folder = os.path.join(dname, 'musics')
music_files = [file for file in os.listdir(music_folder) if is_mp3_file(file)]

# Variable pour suivre le dernier tag scanné et le temps où il a été scanné
last_tag_id = None
last_tag_time = 0

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
