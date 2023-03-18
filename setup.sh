#!/bin/bash

# installing dependencies
pip install -r requirements.txt

# Allowing users to access serial ports without sudo
sudo usermod -a -G plugdev $USER
sudo usermod -a -G dialout $USER

if [ ! -f config.ini ]
then
    cat config.example.ini > config.ini
fi
