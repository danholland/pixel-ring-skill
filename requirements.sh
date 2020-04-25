#!/bin/bash

sudo apt-get -y install python3-mraa libmraa1
sudo usermod -a -G input respeaker
exit 0