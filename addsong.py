import os
import board
from adafruit_pn532.i2c import PN532_I2C

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

# Fonction pour scanner un tag NFC
def scan_nfc_tag():
    try:
        while True:
            tag_id = pn532.read_passive_target(timeout=0.5)
            if tag_id is not None:
                return bytes(tag_id).hex()  # Convert the bytearray to a hex string
                
    except KeyboardInterrupt:
        pass

# Vérifier si un fichier est un fichier MP3
def is_mp3_file(filename):
    return filename.lower().endswith('.mp3')

# Liste des musiques dans le dossier 'musics'
music_folder = 'musics'
music_files = [file for file in os.listdir(music_folder) if is_mp3_file(file)]

try:
    # Vérifier chaque fichier de musique s'il est déjà dans audio_map.txt
    for music_file in music_files:
        if music_file not in nfc_audio_map.values():
            
            while True:
                print(f"Scannez un tag NFC pour associer le fichier '{music_file}'")
                tag_id = scan_nfc_tag()
                if tag_id:
                    if tag_id in nfc_audio_map:
                        print(f"Ce tag est déjà associé à '{nfc_audio_map[tag_id]}', veuillez en scanner un autre.")
                        input("Press return key to continue...")
                    else:
                        nfc_audio_map[tag_id] = music_file
                        save_audio_map(nfc_audio_map)
                        print(f"Association du tag NFC et du fichier '{music_file}' ajoutée avec succès.")
                        input("Press return key to continue...")
                        break
                else:
                    print("Aucun tag NFC détecté, veuillez scanner un tag.")
    print("Tous les fichiers ont été associés")
    # Créer le fichier audio_map.txt s'il n'existe pas
    if not os.path.exists('audio_map.txt'):
        with open('audio_map.txt', 'w'):
            pass

except KeyboardInterrupt:
    # Enregistrer la liste des musiques associées aux tags NFC dans le fichier audio_map.txt avant de quitter
    save_audio_map(nfc_audio_map)
