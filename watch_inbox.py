from pathlib import Path
import subprocess
import time
import os
import shutil

BASE = Path.home() / "ai_lab"
INBOX = BASE / "inbox"
DONE = BASE / "done"
ARCHIVE = BASE / "archive"
TRANSCRIPTS = BASE / "transcripts"

AUDIO_EXTS = {".wav", ".mp3", ".m4a"}
VIDEO_EXTS = {".mp4", ".mov"}

DONE.mkdir(parents=True, exist_ok=True)
ARCHIVE.mkdir(parents=True, exist_ok=True)
TRANSCRIPTS.mkdir(parents=True, exist_ok=True)

processed = set()

print(f"Watching {INBOX} for new files...")

env = os.environ.copy()
env["LD_LIBRARY_PATH"] = "/usr/local/lib/ollama/cuda_v12:" + env.get("LD_LIBRARY_PATH", "")

while True:
    for f in INBOX.iterdir():
        if not f.is_file():
            continue

        ext = f.suffix.lower()
        if ext not in AUDIO_EXTS and ext not in VIDEO_EXTS:
            continue

        if f.name in processed:
            continue

        print(f"New file detected: {f}")

        try:
            if ext in AUDIO_EXTS:
                result = subprocess.run(
                    ["python3", str(BASE / "transcribe.py"), str(f)],
                    env=env
                )

                if result.returncode == 0:
                    shutil.move(str(f), str(DONE / f.name))
                    print(f"Finished audio transcription for: {f.name}")
                    processed.add(f.name)
                else:
                    print(f"Audio transcription failed for: {f.name}")

            elif ext in VIDEO_EXTS:
                result = subprocess.run(
                    ["python3", str(BASE / "process_video.py"), str(f)],
                    env=env
                )

                if result.returncode == 0:
                    print(f"Finished full video pipeline for: {f.name}")
                    processed.add(f.name)
                else:
                    print(f"Video pipeline failed for: {f.name}")

        except Exception as e:
            print(f"Error processing {f.name}: {e}")

    time.sleep(5)
