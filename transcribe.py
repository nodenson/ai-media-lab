from faster_whisper import WhisperModel
from pathlib import Path
import sys
import os

os.environ["LD_LIBRARY_PATH"] = "/usr/local/lib/ollama/cuda_v12:" + os.environ.get("LD_LIBRARY_PATH", "")

if len(sys.argv) < 2:
    print("Usage: python3 transcribe.py /path/to/file")
    sys.exit(1)

input_file = Path(sys.argv[1]).expanduser()

if not input_file.exists():
    print(f"File not found: {input_file}")
    sys.exit(1)

output_dir = Path.home() / "ai_lab" / "transcripts"
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / f"{input_file.stem}.txt"

print("loading")
model = WhisperModel("tiny", device="cuda", compute_type="float16")

print("transcribing")
segments, info = model.transcribe(str(input_file), beam_size=5)

with open(output_file, "w", encoding="utf-8") as f:
    for s in segments:
        line = f"[{s.start:.2f}-{s.end:.2f}] {s.text}"
        print(line)
        f.write(line + "\n")

print(f"done\nsaved to {output_file}")
