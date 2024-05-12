#!/bin/bash

# Update package lists
sudo apt update
apt update

# Install Python 3 and pip
sudo apt install -y python3 python3-pip
apt install -y python3 python3-pip

# Install requests library
sudo pip3 install requests
pip3 install requests

# Install Java Runtime Environment (JRE)
sudo apt install -y default-jre
apt install -y default-jre

# Install git
sudo apt install -y git
apt install -y git

sudo rm CloudShellLinker -r
rm CloudShellLinker -r

# Clone the repository
sudo git clone https://github.com/SpigotRCE/CloudShellLinker
git clone https://github.com/SpigotRCE/CloudShellLinker