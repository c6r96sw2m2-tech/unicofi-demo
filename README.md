# UniCoFi — listening samples

Audio examples for the paper **“UniCoFi: Unified Codec-Domain Speech Restoration
with Far-End Decoder Feature Reuse”**.

Open [`index.html`](index.html) to listen (locally, or through GitHub Pages).
For every condition the page plays the degraded input, the clean reference, the
task-specific baseline, and UniCoRe.

## What is compared

Three task-specific baselines, each cascaded with the **same frozen CleanCodec**
backend that UniCoRe uses, so only the front end differs:

| Condition | Test set | Baseline |
|---|---|---|
| Noisy | LRAC Track-2 noisy test set | DPCRN + CleanCodec |
| Reverberant | LRAC Track-2 reverberant test set | DPCRN + CleanCodec |
| Band-limited (8 → 24 kHz) | LRAC Track-2 band-limited test set | AP-BWE + CleanCodec |
| Acoustic echo (double-talk) | self-consistent closed-loop set | DeepVQE + CleanCodec |

The clean test set is not shown, as it carries no degradation.

## How the samples were chosen

Three utterances per condition, selected as the ones where UniCoRe leads the
corresponding task-specific baseline by the largest margin (PESQ for
noisy/reverb/BWE, ESTOI for AEC):

| Condition | Selection |
|---|---|
| Noisy | PESQ 3.20 / 3.09 / 2.88 (baseline 2.03 / 1.96 / 1.77) |
| Reverberant | PESQ 2.77 / 2.91 / 2.54 (baseline 1.55 / 1.71 / 1.40) |
| Band-limited | PESQ 2.93 / 3.38 / 3.56 (baseline 1.79 / 2.45 / 2.64) |
| Echo (double-talk) | ESTOI 85.2 / 91.7 / 87.6 % (baseline 22.6 / 36.3 / 32.2 %) |

### How the AEC condition is built

For every test utterance the **near-end speech**, the **far-end speech** that is
played out, the **room impulse response (RIR)** and the **signal-to-echo ratio
(SER, −20 to 10 dB)** are fixed once and shared by all systems. What differs is
only the far-end waveform that actually reaches the loudspeaker: inside the
self-consistent loop it is obtained by decoding the far-end bitstream through
**each system's own** codec path, and that echo is then convolved with the *same*
RIR and mixed with the *same* near-end speech.

Each system therefore sees its own microphone mixture — both are provided in the
page (UniCoRe loop / DeepVQE loop) — while the comparison remains fair and
reproducible: identical utterances, identical echo paths, identical levels, and
the same frozen receiver codec. For the noisy, reverberant and band-limited
conditions the degraded input is one and the same file for all systems, so those
rows are directly comparable as well.

## Layout

```
index.html                 # listening page (generated)
audio/<condition>/sample<k>/{input,clean,unicore,<baseline>}.wav
tools/build_samples.py     # collects + converts the clips (24 kHz mono PCM16)
tools/build_page.py        # regenerates index.html
```

## Publishing on GitHub Pages

```sh
git init
git add .
git commit -m "UniCoFi listening samples"
git remote add origin git@github.com:<user>/<repo>.git
git push -u origin main
```

Then enable **Settings → Pages → Deploy from branch → main / root**. The demo is
plain static files (no build step); the scripts in `tools/` are only needed to
regenerate the clips or the page.

## Notes

- Clips are 24-kHz mono 16-bit PCM.
- Test utterances come from the LRAC 2025 open test set and the far-end material
  of the AEC Challenge, as described in the paper.
- The clips are provided for review; please cite the paper if you reuse them.
