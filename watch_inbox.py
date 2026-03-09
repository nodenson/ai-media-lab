from pathlib import Path
import subprocess
import time
import os

INBOX = Path.home() / "ai_lab" / "inbox"
TRANSCRIPTS = Path.home() / "ai_lab" / "transcripts"
PROCESSED = set()

print(f"Watching {INBOX} for new files...")

env = os.environ.copy()
env["LD_LIBRARY_PATH"] = "/usr/local/lib/ollama/cuda_v12:" + env.get("LD_LIBRARY_PATH", "")

while True:
    for f in INBOX.iterdir():
        if not f.is_file():
            continue

        if f.suffix.lower() not in {".mp4", ".mov", ".m4a", ".wav", ".mp3"}:
            continue

        if f.name in PROCESSED:
            continue

        transcript_file = TRANSCRIPTS / f"{f.stem}.txt"
        if transcript_file.exists():
            PROCESSED.add(f.name)
            continue

        print(f"New file detected: {f}")

        result = subprocess.run(
            ["python3", str(Path.home() / "ai_lab" / "process_video.py"), str(f)],
            env=env
        )

        if result.returncode == 0:
            print(f"Finished full pipeline for: {f.name}")
            PROCESSED.add(f.name)
        else:
            print(f"Pipeline failed for: {f.name}")

    time.sleep(5)
