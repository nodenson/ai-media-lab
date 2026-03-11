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

Working components:

- Ubuntu server running
- SSH access working
- Python virtual environment active
- Faster-Whisper transcription working
- Clip suggestion system working
- FFmpeg clip cutting working
- Full pipeline script working
- Inbox watcher automation running
- GitHub repo initialized

---

# Folder Structure

\`\`\`
ai_lab/
├── inbox/        # drop new videos here
├── archive/      # processed source videos
├── transcripts/  # .txt and .srt transcription outputs
├── clips/        # suggested clip timestamps
├── outputs/      # rendered clips
├── logs/         # watcher logs
├── models/       # downloaded AI models
\`\`\`

---

# Pipeline

\`\`\`
Capture
   ↓
Drop video in inbox
   ↓
Watcher detects file
   ↓
Transcribe speech
   ↓
Find clip moments
   ↓
Cut clips
   ↓
Outputs ready for editing
   ↓
Edit in CapCut
   ↓
Post
   ↓
Archive source
\`\`\`

---

# Scripts

\`transcribe.py\`
- transcribes audio/video into text and subtitles

\`clip_finder.py\`
- scores transcript lines
- identifies promising clip timestamps

\`cut_clips.py\`
- cuts clips using FFmpeg
- optionally burns subtitles

\`process_video.py\`
- runs the full pipeline on a single file

\`watch_inbox.py\`
- monitors the inbox
- automatically processes new files

---

# Basic Usage

Run full pipeline manually:

\`\`\`
python3 process_video.py /path/to/video.mp4
\`\`\`

Run transcription only:

\`\`\`
python3 transcribe.py /path/to/video.mp4
\`\`\`

Run watcher manually:

\`\`\`
python3 watch_inbox.py
\`\`\`

Run watcher daemon:

\`\`\`
tmux new -d -s ailab '~/ai_lab/run_ai_lab.sh'
\`\`\`

View logs:

\`\`\`
tail -f ~/ai_lab/logs/watcher.log
\`\`\`

---

# Drop-Folder Workflow

1. Record footage
2. Upload video to server
3. Drop file into:

\`\`\`
~/ai_lab/inbox/
\`\`\`

The system will automatically:

- transcribe
- find clips
- render outputs

---

# Notes

- Raw media should not be committed to GitHub
- Only scripts and lightweight outputs belong in the repo
- Large media files stay local on the server

---

# Next Improvements

Future upgrades planned:

- smarter clip detection (multi-line scoring)
- vertical crop for Shorts/TikTok
- auto caption styling
- auto publishing pipeline
- searchable transcript index

