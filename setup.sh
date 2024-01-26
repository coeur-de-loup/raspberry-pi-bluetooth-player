#!/bin/bash
sudo apt-get install git -y

# cd ~
# echo "Cloning raspberry-pi-bluetooth-player repo"
# mkdir -p ~/btplayer
# git clone https://github.com/coeur-de-loup/raspberry-pi-bluetooth-player.git ~/btplayer
# chmod +x ~/btplayer/setup.sh
# sudo sh setup.sh


# Install dependencies
echo "Installing dependencies..."
sudo apt-get update
sudo apt upgrade -y

echo "Downloading Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
echo "Installing Docker"
sudo sh get-docker.sh

echo "Add pi user to docker group"
sudo usermod -aG docker pi

echo "Installing pulseaudio..."
sudo apt-get install pulseaudio pulseaudio-utils pulseaudio-module-bluetooth -y

echo "Activate pulseaudio TCP server mode"
echo "load-module module-native-protocol-tcp auth-anonymous=1" | sudo tee -a /etc/pulse/default.pa

echo "Enable pulseaudio service"
systemctl --user enable pulseaudio
systemctl --user start pulseaudio


echo "Building flask container..."
cd ~/btplayer
docker compose build

echo "Copying bt.service to /etc/systemd/system..."
sudo cp ~/btplayer/bt.service /etc/systemd/system

echo "Reloading system daemon for bt.service to take effect..."
sudo systemctl daemon-reload

echo "Enabling bt.service..."
sudo systemctl enable bt.service

sudo reboot

