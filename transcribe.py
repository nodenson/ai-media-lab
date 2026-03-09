from faster_whisper import WhisperModel
from pathlib import Path
import sys

if len(sys.argv) < 2:
    print("Usage: python3 transcribe.py /path/to/file")
    sys.exit(1)

input_file = Path(sys.argv[1]).expanduser()

if not input_file.exists():
    print(f"File not found: {input_file}")
    sys.exit(1)

output_dir = Path.home() / "ai_lab" / "transcripts"
output_dir.mkdir(parents=True, exist_ok=True)

txt_file = output_dir / f"{input_file.stem}.txt"
srt_file = output_dir / f"{input_file.stem}.srt"

print("loading")
model = WhisperModel("tiny", device="cuda", compute_type="float16")

print("transcribing")
segments, info = model.transcribe(str(input_file), beam_size=5)

segments = list(segments)

def to_srt_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

with open(txt_file, "w", encoding="utf-8") as txt, open(srt_file, "w", encoding="utf-8") as srt:
    for i, s in enumerate(segments, start=1):
        line = f"[{s.start:.2f}-{s.end:.2f}] {s.text}"
        print(line)
        txt.write(line + "\n")

        srt.write(f"{i}\n")
        srt.write(f"{to_srt_time(s.start)} --> {to_srt_time(s.end)}\n")
        srt.write(f"{s.text.strip()}\n\n")

print(f"done\nsaved to {txt_file}\nsaved to {srt_file}")
