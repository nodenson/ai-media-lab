from pathlib import Path
import re
import sys

if len(sys.argv) < 2:
    print("Usage: python3 clip_finder.py /path/to/transcript.txt")
    sys.exit(1)

transcript_file = Path(sys.argv[1]).expanduser()

if not transcript_file.exists():
    print(f"Transcript not found: {transcript_file}")
    sys.exit(1)

output_dir = Path.home() / "ai_lab" / "clips"
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / f"{transcript_file.stem}_clips.txt"

lines = transcript_file.read_text(encoding="utf-8").splitlines()

keywords = [
    "go", "again", "hard", "fight", "push", "up", "let's",
    "come on", "now", "never", "more", "pain", "power",
    "strong", "remember", "forgot", "afraid", "alone"
]

clips = []

for line in lines:
    lower = line.lower()
    score = 0

    for kw in keywords:
        if kw in lower:
            score += 1

    m = re.match(r"\[(\d+\.\d+)-(\d+\.\d+)\]\s+(.*)", line)
    if m:
        start, end, text = m.groups()

        if len(text.strip()) > 12 and score > 0:
            clips.append((score, float(start), float(end), text.strip()))

clips.sort(key=lambda x: (-x[0], x[1]))

top = clips[:10]

with open(output_file, "w", encoding="utf-8") as f:
    for score, start, end, text in top:
        line = f"{start:.2f}-{end:.2f} | score={score} | {text}"
        print(line)
        f.write(line + "\n")

print(f"\nSaved clip suggestions to: {output_file}")
