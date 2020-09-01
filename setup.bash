#!/bin/bash
sudo apt-get update
sudo apt-get install build-essential python-dev python-setuptools python-pip python-smbus python3-pip virtualenv -y
pip install -U pip setuptools wheel
rm -r venv
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
deactivate
sudo cp systemd/nubeio-bbio.service /etc/systemd/system/
sudo cp systemd/nubeio-enable-uart-pins.service /etc/systemd/system/
sudo cp systemd/nubeio-enable-uart-pins.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable nubeio-bbio.service
sudo systemctl enable nubeio-enable-uart-pins.timer
sudo systemctl start bbio.service
