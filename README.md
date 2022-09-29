# BLE GATT CLIENT CLI

This is a bluetooth GATT Client for reading a GATT Server. It looks for a device named ESP_GATTS_DEMO and connects to it
if found.

# Setup

make sure you've got python 3 installed with pip and venv

### first change to this directory:
```bash
cd path_to_this_directory
```
## create virtual environment: 
```bash
python3 -m venv venv
```

### begin virtual environment:
```bash
source venv/bin/activate
```

### install all dependencies:
```bash
pip install -r requirements.txt
```

### run GATT Client:
```bash
python main.py
```