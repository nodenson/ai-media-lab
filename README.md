# AI Media Lab

Personal media automation pipeline for turning raw footage into searchable, editable content.

---

# Goal

Build a workflow that:

- ingests footage from Meta glasses, iPhone, and other sources
- organizes media for processing
- transcribes speech with Faster-Whisper
- finds strong clip moments automatically
- cuts candidate clips with FFmpeg
- prepares content for editing in CapCut
- supports edit once, publish everywhere

---

# Current Status

The system currently supports:

- Ubuntu server running
- SSH access configured
- Faster-Whisper transcription working
- Automated clip detection
- FFmpeg clip cutting
- Automatic vertical clip generation
- Caption support
- Watcher automation running
- GitHub repo active

---

# Pipeline Overview

```
capture
↓
inbox
↓
transcription
↓
clip detection
↓
clip generation
↓
vertical export
↓
edit in CapCut
↓
publish
```

---

# Folder Structure

```
ai_lab/
│
├── inbox/            # new media dropped here
├── processing/       # temporary processing
├── outputs/          # generated clips
├── archive/          # processed source files
│
├── transcripts/      # speech transcripts
├── clips/            # clip suggestions
│
├── logs/             # pipeline logs
├── models/           # AI models
│
├── clip_finder.py
├── cut_clips.py
├── process_video.py
├── transcribe.py
├── watch_inbox.py
└── run_ai_lab.sh
```

---

# Scripts

### transcribe.py
Uses Faster-Whisper to generate transcript and subtitle files.

Outputs:

```
transcripts/video_name.txt
transcripts/video_name.srt
```

---

### clip_finder.py

Analyzes transcript lines and identifies strong moments.

Uses scoring based on:

- sentence completeness
- motivational / dramatic language
- clip length
- speech structure

Outputs:

```
clips/video_name_clips.txt
```

---

### cut_clips.py

Uses FFmpeg to generate video clips from suggested timestamps.

Creates:

```
clip_1.mp4
clip_1_vertical.mp4
clip_1_captioned.mp4
```

---

### process_video.py

Runs the full pipeline for a single video.

```
python3 process_video.py /path/to/video.mp4
```

---

### watch_inbox.py

Watches the inbox folder and triggers processing automatically.

Run:

```
python3 watch_inbox.py
```

---

### run_ai_lab.sh

Launches the full watcher pipeline.

```
./run_ai_lab.sh
```

---

# Typical Workflow

1. Capture footage (iPhone / Meta glasses / camera)
2. Move footage to the AI server inbox
3. System processes automatically
4. Review clips in the outputs folder
5. Import best clips into CapCut
6. Add hook text, music, branding
7. Export and publish

---

# Git Rules

The following folders are ignored:

```
archive/
outputs/
inbox/
transcripts/
clips/
logs/
venv/
```

Media files are not tracked by git.

---

# Roadmap

Planned upgrades:

- searchable transcript database
- smarter clip detection
- auto social media packaging
- batch video ingestion
- AI caption styling

---

# Purpose

The goal of AI Media Lab is to transform raw footage into structured, searchable media assets that can be rapidly turned into publishable content.
