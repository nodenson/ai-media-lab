import argparse
import os
import time
import torch

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
args = parser.parse_args()

print(f"Starting job for input: {args.input}")
print(f"PID: {os.getpid()}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"Visible GPU count: {torch.cuda.device_count()}")

if torch.cuda.is_available():
    device = torch.device("cuda:0")
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")

    x = torch.randn(4000, 4000, device=device)
    for i in range(10):
        x = x @ x
        print(f"Step {i+1}/10 complete")
        time.sleep(1)

print("Job finished.")
