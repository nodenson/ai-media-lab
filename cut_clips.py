from pathlib import Path
import subprocess
import re
import sys

if len(sys.argv) < 3:
    print("Usage: python3 cut_clips.py /path/to/video.mp4 /path/to/clips.txt")
    sys.exit(1)

video_file = Path(sys.argv[1]).expanduser()
clips_file = Path(sys.argv[2]).expanduser()

if not video_file.exists():
    print(f"Video not found: {video_file}")
    sys.exit(1)

if not clips_file.exists():
    print(f"Clips file not found: {clips_file}")
    sys.exit(1)

output_dir = Path.home() / "ai_lab" / "outputs" / video_file.stem
output_dir.mkdir(parents=True, exist_ok=True)

lines = clips_file.read_text(encoding="utf-8").splitlines()

count = 0
for line in lines:
    m = re.match(r"(\d+\.\d+)-(\d+\.\d+)\s+\|", line)
    if not m:
        continue

    start, end = m.groups()
    out_file = output_dir / f"clip_{count+1}_{start.replace('.', '_')}_{end.replace('.', '_')}.mp4"

    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_file),
        "-ss", start,
        "-to", end,
        "-c:v", "libx264",
        "-c:a", "aac",
        str(out_file)
    ]

    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=False)
    count += 1

print(f"Done. Created {count} clips in {output_dir}")
