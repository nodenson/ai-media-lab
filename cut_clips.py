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

base = Path.home() / "ai_lab"
srt_file = base / "transcripts" / f"{video_file.stem}.srt"

output_dir = base / "outputs" / video_file.stem
output_dir.mkdir(parents=True, exist_ok=True)

lines = clips_file.read_text(encoding="utf-8").splitlines()

count = 0
for line in lines:
    m = re.match(r"(\d+\.\d+)-(\d+\.\d+)\s+\|", line)
    if not m:
        continue

    start, end = m.groups()
    clip_file = output_dir / f"clip_{count+1}_{start.replace('.', '_')}_{end.replace('.', '_')}.mp4"
    captioned_file = output_dir / f"clip_{count+1}_{start.replace('.', '_')}_{end.replace('.', '_')}_captioned.mp4"

    cut_cmd = [
        "ffmpeg", "-y",
        "-i", str(video_file),
        "-ss", start,
        "-to", end,
        "-c:v", "libx264",
        "-c:a", "aac",
        str(clip_file)
    ]

    print("Running:", " ".join(cut_cmd))
    subprocess.run(cut_cmd, check=False)

    if srt_file.exists():
        caption_cmd = [
            "ffmpeg", "-y",
            "-i", str(clip_file),
            "-vf", f"subtitles={srt_file}",
            str(captioned_file)
        ]
        print("Running:", " ".join(caption_cmd))
        subprocess.run(caption_cmd, check=False)

    count += 1

print(f"Done. Created {count} clips in {output_dir}")
