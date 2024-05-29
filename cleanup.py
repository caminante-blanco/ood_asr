import re
import sys

file_name = sys.argv[1]

with open(file_name, 'r') as f:
    text = f.read()

    text = re.sub(r"\*\*.*?\*\*", "", text)
    text = re.sub(r"\*.*?\*", "", text)
    text = re.sub(r"[0-9]+", "", text)
    text = re.sub(r"‑", "-", text)    
    text = re.sub(r"ꞌ", "'", text)
    text = re.sub(r"([.!?])\s+", r"\1\n", text)
    text = re.sub(r"[^\w\s]+", "", text)
    text = re.sub(r" +", " ", text)
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"\n ", "\n", text)
    with open(f"{file_name}_clean", 'w') as f:
        f.write(text)


