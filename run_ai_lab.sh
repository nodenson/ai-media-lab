#!/bin/bash
cd ~/ai_lab
source venv/bin/activate
mkdir -p ~/ai_lab/logs
python3 watch_inbox.py >> ~/ai_lab/logs/watcher.log 2>&1
