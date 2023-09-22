#!/bin/bash

set -e  # Exit on error

# Run system update and upgrade
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip git mpg123 vsftpd

# Install Python packages
pip3 install Adafruit-Blinka adafruit-circuitpython-pn532 pygame

# Clone and install WM8960-Audio-HAT
git clone https://github.com/waveshare/WM8960-Audio-HAT
cd WM8960-Audio-HAT
sudo ./install.sh
cd ..

# Create the service unit file for audiobox
service_unit_content="[Unit]
Description=PyboxAudio
After=network.target

[Service]
Type=simple
User=admin
WorkingDirectory=/home/admin/
ExecStart=/usr/bin/python3 /home/admin/audiobox.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"

service_unit_file_path="/etc/systemd/system/audiobox.service"

echo "$service_unit_content" | sudo tee "$service_unit_file_path" > /dev/null
sudo chmod 644 "$service_unit_file_path"
sudo systemctl enable audiobox.service
sudo systemctl start audiobox.service

# Create the alsactl-restore.service file
alsactl_service_content="[Unit]
Description=Restore ALSA settings

[Service]
ExecStart=/usr/sbin/alsactl restore

[Install]
WantedBy=multi-user.target
"

alsactl_service_file_path="/etc/systemd/system/alsactl-restore.service"

echo "$alsactl_service_content" | sudo tee "$alsactl_service_file_path" > /dev/null
sudo systemctl enable alsactl-restore.service
sudo systemctl start alsactl-restore.service

# Define the MOTD content
MOTD_CONTENT=" ______         __
|   __ \.--.--.|  |--.-----.--.--.
|    __/|  |  ||  _  |  _  |_   _|
|___|   |___  ||_____|_____|__.__|
        |_____|    AudioBox with love
-----------------------------------------------
Pybox is a special project for you Arthur. I made
it with love just for you so you can discover
great music!
-----------------------------------------------"

# Write the MOTD content to the /etc/motd file
echo -e "$MOTD_CONTENT" | sudo tee /etc/motd > /dev/null

# Clean up cloned repository
rm -rf WM8960-Audio-HAT

# Display a message indicating completion
echo "Setup completed successfully."
