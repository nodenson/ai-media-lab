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

dramatic_words = {
    "power", "dark", "fear", "pain", "fight", "war", "fire", "death",
    "destroyer", "arrival", "shadow", "blood", "storm", "king", "god",
    "rage", "iron", "throne", "force"
}

motivational_words = {
    "remember", "forgot", "alone", "hard", "afraid", "push", "strong",
    "never", "more", "keep", "going", "become", "rise", "fall", "stand",
    "health", "discipline", "suffer", "work", "training", "effort"
}

hook_starts = (
    "you", "i", "this", "that", "we", "they", "let", "listen",
    "watch", "remember", "imagine", "if", "when", "never", "your"
)

filler_phrases = (
    "um", "uh", "like", "you know", "sort of", "kind of", "basically"
)

segments = []
lines = transcript_file.read_text(encoding="utf-8").splitlines()

for line in lines:
    m = re.match(r"\[(\d+\.\d+)-(\d+\.\d+)\]\s+(.*)", line)
    if not m:
        continue

    start, end, text = m.groups()
    text = text.strip()
    if not text:
        continue

    segments.append({
        "start": float(start),
        "end": float(end),
        "text": text
    })

if not segments:
    print("No valid transcript segments found.")
    sys.exit(0)

candidates = []

def score_text(text: str, duration: float) -> int:
    lower = text.lower()
    score = 1

    word_count = len(text.split())

    if word_count >= 8:
        score += 2
    elif word_count >= 5:
        score += 1

    if word_count >= 15:
        score += 2

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

    if duration >= 8:
        score += 1
    if duration >= 12:
        score += 1
    if duration > 45:
        score -= 2

    return score

# Build clip candidates from windows of 1 to 3 adjacent transcript lines
max_window = 3

for i in range(len(segments)):
    for window_size in range(1, max_window + 1):
        j = i + window_size - 1
        if j >= len(segments):
            continue

        block = segments[i:j + 1]
        start_f = block[0]["start"]
        end_f = block[-1]["end"]
        duration = end_f - start_f

        if duration < 4.0:
            continue
        if duration > 60.0:
            continue

        text = " ".join(seg["text"] for seg in block).strip()
        if len(text) < 20:
            continue

        padded_start = max(0.0, start_f - 2.0)
        padded_end = end_f + 2.5

        score = score_text(text, duration)

        candidates.append((score, padded_start, padded_end, text))

# Sort by highest score first, then earlier clips first
candidates.sort(key=lambda x: (-x[0], x[1]))

selected = []
for candidate in candidates:
    score, start, end, text = candidate
    overlaps = False

    for existing in selected:
        _, ex_start, ex_end, _ = existing
        if not (end < ex_start or start > ex_end):
            overlaps = True
            break

    if not overlaps:
        selected.append(candidate)

    if len(selected) >= 10:
        break

with open(output_file, "w", encoding="utf-8") as f:
    for score, start, end, text in selected:
        line = f"{start:.2f}-{end:.2f} | score={score} | {text}"
        print(line)
        f.write(line + "\n")

print(f"\nSaved clip suggestions to: {output_file}")
