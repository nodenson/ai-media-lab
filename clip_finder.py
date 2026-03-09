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

dramatic_words = {
    "power", "dark", "fear", "pain", "fight", "war", "fire", "death",
    "destroyer", "arrival", "shadow", "blood", "storm", "king", "god",
    "rage", "iron", "throne", "force"
}

motivational_words = {
    "remember", "forgot", "alone", "hard", "afraid", "push", "strong",
    "never", "more", "keep", "going", "become", "rise", "fall", "stand"
}

hook_starts = (
    "you", "i", "this", "that", "we", "they", "let", "listen",
    "watch", "remember", "imagine", "if", "when", "never"
)

filler_phrases = (
    "um", "uh", "like", "you know", "sort of", "kind of", "basically"
)

clips = []

for line in lines:
    m = re.match(r"\[(\d+\.\d+)-(\d+\.\d+)\]\s+(.*)", line)
    if not m:
        continue

    start, end, text = m.groups()
    text = text.strip()
    lower = text.lower()

    if len(text) < 12:
        continue

    score = 1

    word_count = len(text.split())
    if word_count >= 5:
        score += 1
    if word_count >= 9:
        score += 1

    if text.endswith((".", "!", "?")):
        score += 2

    if lower.startswith(hook_starts):
        score += 2

    if any(word in lower for word in dramatic_words):
        score += 2

    if any(word in lower for word in motivational_words):
        score += 2

    if "," in text or ";" in text or ":" in text:
        score += 1

    if any(phrase in lower for phrase in filler_phrases):
        score -= 2

    # Expand short timestamps into more usable clips
    start_f = float(start)
    end_f = float(end)
    padded_start = max(0.0, start_f - 1.5)
    padded_end = end_f + 1.5

    clips.append((score, padded_start, padded_end, text))

# Sort by score first, then earlier clips first
clips.sort(key=lambda x: (-x[0], x[1]))

# Deduplicate near-overlapping results
selected = []
for clip in clips:
    score, start, end, text = clip
    overlaps = False
    for existing in selected:
        _, ex_start, ex_end, _ = existing
        if not (end < ex_start or start > ex_end):
            overlaps = True
            break
    if not overlaps:
        selected.append(clip)
    if len(selected) >= 10:
        break

with open(output_file, "w", encoding="utf-8") as f:
    for score, start, end, text in selected:
        line = f"{start:.2f}-{end:.2f} | score={score} | {text}"
        print(line)
        f.write(line + "\n")

print(f"\nSaved clip suggestions to: {output_file}")
