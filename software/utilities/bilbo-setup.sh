#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to edit files safely
temp_edit() {
    local file=$1
    local search=$2
    local replace=$3
    
    if [ -n "$search" ]; then
        sudo sed -i "s|$search|$replace|g" "$file"
    fi
    
    if [ -n "$replace" ] && ! grep -q "$replace" "$file"; then
        echo "$replace" | sudo tee -a "$file" > /dev/null
    fi
}

# ==========================
# Step 2.1: Update System
# ==========================
echo -e "
========== Updating System =========="
sudo apt-get update -y

echo -e "
========== System Update Complete =========="

# ==========================
# Step 2.2: Set USB Mode
# ==========================
echo "\n========== Configuring USB Mode =========="
# Edit /boot/config.txt
CONFIG_TXT="/boot/config.txt"
temp_edit $CONFIG_TXT "otg_mode=1" ""
temp_edit $CONFIG_TXT "dtoverlay=dwc2" "dtoverlay=dwc2"

# Edit /boot/cmdline.txt
CMDLINE_TXT="/boot/cmdline.txt"
sudo sed -i 's|\(rootwait\)|\1 modules-load=dwc2,g_ether|' $CMDLINE_TXT

echo "\n========== USB Mode Configuration Complete =========="

# ==========================
# Step 3.1: Install Python Tools
# ==========================
echo "\n========== Installing Python Tools =========="
sudo apt-get install -y python3-distutils python3-pip
sudo apt-get install -y --upgrade python3-setuptools

echo "\n========== Python Tools Installation Complete =========="

# ==========================
# Step 3.2: Install Micropython Libraries
# ==========================
echo "\n========== Installing Micropython Libraries =========="
pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py -O raspi-blinka.py
echo "n" | sudo -E env PATH=$PATH python3 raspi-blinka.py

echo "\n========== Micropython Libraries Installation Complete =========="

# ==========================
# Step 3.3: Install Python Libraries
# ==========================
echo "\n========== Installing Additional Python Libraries =========="
pip3 install orjson evdev cobs pygame dacite adafruit-circuitpython-ssd1306 luma.oled

echo "\n========== Additional Python Libraries Installation Complete =========="

# ==========================
# Step 3.4: Install GIT
# ==========================
echo "\n========== Installing GIT =========="
sudo apt-get install -y git

echo "\n========== GIT Installation Complete =========="

# ==========================
# Step 4: Make Directories
# ==========================
echo "\n========== Creating Directories =========="
# Get the home directory of the invoking user
USER_HOME=$(eval echo ~${SUDO_USER:-$USER})

# Change to the invoking user's home directory
cd "$USER_HOME"

# Create directories in the invoking user's home directory
mkdir -p robot/{settings,software,configs,experiments,venv}
sudo chown -R ${SUDO_USER:-$USER}:${SUDO_USER:-$USER} "$USER_HOME/robot"

echo "\n========== Directory Creation Complete =========="

# ==========================
# Step 5.1: Enable UART
# ==========================
echo "\n========== Enabling UART =========="
# Edit /boot/config.txt
temp_edit $CONFIG_TXT "enable-uart=1" "enable-uart=1"
temp_edit $CONFIG_TXT "dtoverlay=uart5" "dtoverlay=uart5"

echo "\n========== UART Enabled =========="

# ==========================
# Step 6.1: Enable Soundcard Overlay
# ==========================
echo "\n========== Configuring Soundcard Overlay =========="
# Edit /boot/config.txt
temp_edit $CONFIG_TXT "dtoverlay=googlevoicehat-soundcard" "dtoverlay=googlevoicehat-soundcard"
sudo sed -i 's|^dtparam=audio-on|#dtparam=audio-on|' $CONFIG_TXT

# Configure /etc/asound.conf
echo "\n========== Configuring Audio Settings =========="
sudo bash -c 'cat > /etc/asound.conf' << EOF
pcm.!default {
    type asym
    playback.pcm {
        type dmix
        ipc_key 1024
        slave {
            pcm "hw:0,0"
            rate 48000
        }
    }
    capture.pcm {
        type dsnoop
        ipc_key 1025
        slave {
            pcm "hw:0,0"
            rate 48000
        }
    }
}

ctl.!default {
    type hw
    card 0
}
EOF

echo "\n========== Installing SOX and MP3 Support =========="
sudo apt-get install -y sox libsox-fmt-mp3

echo -e "
========== Adding Zero Sound to Startup =========="
USER_CRON=$(logname) # Determine the original user who invoked sudo
TMP_CRON=$(mktemp)
crontab -u "$USER_CRON" -l 2>/dev/null | grep -v "play -n synth 0 sine 0 repeat" > "$TMP_CRON" || true  # Avoid duplicates
echo "@reboot sleep 10 && nohup play -n synth 0 sine 0 repeat > /dev/null 2>&1 &" >> "$TMP_CRON"
echo "@reboot /usr/bin/python3 /home/admin/robot/software/robot/applications/startup.py &" >> "$TMP_CRON"
crontab -u "$USER_CRON" "$TMP_CRON"
rm -f "$TMP_CRON"
echo -e "
========== Zero Sound and Python Startup Added to Crontab =========="

echo "\n========== Soundcard Configuration Complete =========="

# ==========================
# Step 7.1: Install Fish Shell
# ==========================
echo "\n========== Installing Fish Shell =========="
sudo apt install fish -y

echo "
========== Fish Shell Installation Complete =========="

# ==========================
# Step 7.4: Set Fish as Default Shell
# ==========================
echo "
========== Setting Fish as Default Shell =========="
sudo -u "$USER" chsh -s $(which fish)
echo "
========== Fish Set as Default Shell =========="

# ==========================
# Step 7.2: Suppress SSH Greetings
# ==========================
echo "\n========== Suppressing SSH Greetings =========="
sudo rm -r /etc/motd

echo "\n========== SSH Greetings Suppressed =========="

# ==========================
# Step 7.3: Remove Fish Greeting
# ==========================
echo "\n========== Removing Fish Shell Greeting =========="

cd "$USER_HOME"
mkdir -p ./.config/fish
sudo chown -R ${SUDO_USER:-$USER}:${SUDO_USER:-$USER} "$USER_HOME/.config/fish"
echo "set fish_greeting ''" > ./.config/fish/config.fish

echo "\n========== Fish Shell Greeting Removed =========="

# ==========================
# Completion Message and Reboot
# ==========================
echo "\n========== Setup Complete! =========="
echo "\nSetup complete! Please press any key to reboot your Raspberry Pi."
read -n 1 -s
sudo reboot
