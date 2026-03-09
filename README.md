# AI Media Lab

Personal media automation pipeline for turning raw footage into searchable, editable content.

## Goal

Build a workflow that:

- ingests footage from Meta glasses, iPhone, and other sources
- organizes media for processing
- transcribes speech with Faster-Whisper
- finds strong clip moments automatically
- cuts candidate clips with FFmpeg
- prepares content for editing in CapCut
- supports edit once, publish everywhere

## Current Status

- Ubuntu server is running
- SSH is working
- Faster-Whisper is installed and working
- Transcription pipeline is working
- Clip suggestion pipeline is working
- FFmpeg clip cutting is working
- Full pipeline script is working
- Watcher automation is running
- GitHub repo is live

## Current Workflow

Capture -> Inbox -> Transcribe -> Find Clips -> Cut Clips -> Edit in CapCut -> Post -> Archive

## Scripts

- `transcribe.py` — transcribes audio/video into text
- `clip_finder.py` — scores transcript lines and suggests clip moments
- `cut_clips.py` — cuts real video clips from suggested timestamps
- `process_video.py` — runs the full pipeline on one file
- `watch_inbox.py` — watches the inbox and triggers processing automatically

## Usage

Run the full pipeline on one file:

```bash
python3 process_video.py /path/to/video.mp4

Run transcription only:

'''bash
python3 transcribe.py /path/to/video.mp4

Run the watcher:

'''bash
python3 watch_inbox.py

Notes

This repo is for code and lightweight text outputs. Raw media and generated clip files should stay out of version control.


