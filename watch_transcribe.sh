#!/bin/bash

INBOX="$HOME/ai_lab/inbox"
DONE="$HOME/ai_lab/done"
SCRIPT="$HOME/ai_lab/transcribe.py"

mkdir -p "$DONE"

while true; do
  for file in "$INBOX"/*.wav "$INBOX"/*.mp3 "$INBOX"/*.m4a; do
    [ -e "$file" ] || continue
    echo "Processing $file"
    python3 "$SCRIPT" "$file"
    mv "$file" "$DONE"/
  done
  sleep 10
done
