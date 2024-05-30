import torch
import torchaudio
from torchaudio.pipelines import MMS_FA as bundle
from typing import List
import IPython
import matplotlib.pyplot as plt
import re
import sys

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = bundle.get_model()
model.to(device)

tokenizer = bundle.get_tokenizer()
aligner = bundle.get_aligner()

def normalize_text(text):
    text = text.lower()
    text = text.replace("’", "'")
    text = re.sub(r"[^a-z\s']", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def compute_alignments(waveform: torch.Tensor, transcript: str):
    with torch.inference_mode():
        print("Waveform shape:", waveform.shape)
        emission, _ = model(waveform.to(device))
        print("Emission shape:", emission.shape)
        token_spans = aligner(emission[0], tokenizer(transcript))
    return emission, token_spans

def _score(spans):
    return sum(s.score * len(s) for s in spans) / sum(len(s) for s in spans)

def plot_alignments(waveform, token_spans, emission, transcript, sample_rate=bundle.sample_rate):
    ratio = waveform.size(1) / emission.size(1) / sample_rate

    fig, axes = plt.subplots(2, 1)
    axes[0].imshow(emission[0].detach().cpu().T, aspect="auto")
    axes[0].set_title("Emission")
    axes[0].set_xticks([])

    axes[1].specgram(waveform[0], Fs=sample_rate)
    for t_spans, chars in zip(token_spans, transcript):
        t0, t1 = t_spans[0].start, t_spans[-1].end
        axes[0].axvspan(t0 - 0.5, t1 - 0.5, facecolor="None", hatch="/", edgecolor="white")
        axes[1].axvspan(ratio * t0, ratio * t1, facecolor="None", hatch="/", edgecolor="white")
        axes[1].annotate(f"{_score(t_spans):.2f}", (ratio * t0, sample_rate * 0.51), annotation_clip=False)

        for span, char in zip(t_spans, chars):
            t0 = span.start * ratio
            axes[1].annotate(char, (t0, sample_rate * 0.55), annotation_clip=False)

    axes[1].set_xlabel("time [second]")
    fig.tight_layout()

def preview_word(waveform, spans, num_frames, transcript, sample_rate=bundle.sample_rate):
    ratio = waveform.size(1) / num_frames
    x0 = int(ratio * spans[0].start)
    x1 = int(ratio * spans[-1].end)
    print(f"{transcript} ({_score(spans):.2f}): {x0 / sample_rate:.3f} - {x1 / sample_rate:.3f} sec")
    segment = waveform[:, x0:x1]
    return IPython.display.Audio(segment.numpy(), rate=sample_rate)

def force_align(audio_path: str, transcript: str):
    waveform, sample_rate = torchaudio.load(audio_path)
    assert sample_rate == bundle.sample_rate, f"Sample rate mismatch: expected {bundle.sample_rate}, got {sample_rate}"

    print("Waveform loaded with shape:", waveform.shape)

    transcript = transcript.split()
    tokens = tokenizer(transcript)

    emission, token_spans = compute_alignments(waveform, transcript)

    num_frames = emission.size(1)

    plot_alignments(waveform, token_spans, emission, transcript)

    IPython.display.Audio(waveform, rate=sample_rate)
    
    for i in range(len(token_spans)):
        preview_word(waveform, token_spans[i], num_frames, transcript[i])
    
def main():
    text = ""
    audio_path = sys.argv[1]
    transcript_path = sys.argv[2]
    with open(transcript_path) as f:
        transcript = f.readlines()
    for line in transcript:
        text += normalize_text(line) + " "
    force_align(audio_path, text)

if __name__ == "__main__":
    main()

