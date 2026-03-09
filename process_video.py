from pathlib import Path
import subprocess
import sys
import os
import shutil

if len(sys.argv) < 2:
    print("Usage: python3 process_video.py /path/to/video")
    sys.exit(1)

video_file = Path(sys.argv[1]).expanduser()

if not video_file.exists():
    print(f"Video not found: {video_file}")
    sys.exit(1)

base = Path.home() / "ai_lab"
transcript_file = base / "transcripts" / f"{video_file.stem}.txt"
clips_file = base / "clips" / f"{video_file.stem}_clips.txt"
archive_dir = base / "archive"
archive_dir.mkdir(parents=True, exist_ok=True)

env = os.environ.copy()
env["LD_LIBRARY_PATH"] = "/usr/local/lib/ollama/cuda_v12:" + env.get("LD_LIBRARY_PATH", "")

commands = [
    ["python3", str(base / "transcribe.py"), str(video_file)],
    ["python3", str(base / "clip_finder.py"), str(transcript_file)],
    ["python3", str(base / "cut_clips.py"), str(video_file), str(clips_file)],
]

for cmd in commands:
    print("\nRunning:", " ".join(cmd))
    result = subprocess.run(cmd, env=env)
    if result.returncode != 0:
        print(f"Step failed: {' '.join(cmd)}")
        sys.exit(result.returncode)

archived_path = archive_dir / video_file.name
shutil.move(str(video_file), str(archived_path))

print(f"\nDone. Full pipeline completed.")
print(f"Archived source file to: {archived_path}")
