# UniCoFi — listening samples

Audio examples for the paper **“UniCoFi: Unified Codec-Domain Speech Restoration
with Far-End Decoder Feature Reuse”**.

Open [`index.html`](index.html) to listen (locally, or through GitHub Pages).
For every condition the page plays the degraded input, the clean reference, the
task-specific baseline, and UniCoFi.

Without GitHub Pages you can still listen straight from the repository:
[`links.md`](links.md) lists a direct link for every clip (clicking a `.wav`
plays or downloads it), and opening any `.wav` in the file browser gives a player.

## What is compared

Three task-specific baselines, each cascaded with the **same frozen CleanCodec**
backend that UniCoFi uses, so only the front end differs:

| Condition | Test set | Baseline |
|---|---|---|
| Noisy | LRAC Track-2 noisy test set | DPCRN + CleanCodec |
| Reverberant | LRAC Track-2 reverberant test set | DPCRN + CleanCodec |
| Band-limited (8 → 24 kHz) | LRAC Track-2 band-limited test set | AP-BWE + CleanCodec |
| Acoustic echo (double-talk) | self-consistent closed-loop set | DeepVQE + CleanCodec |

The clean test set is not shown, as it carries no degradation.

## How the AEC condition is built

For every test utterance the **near-end speech**, the **far-end speech** to be
transmitted, the **room impulse response (RIR)** and the **signal-to-echo ratio
(SER, −20 to 10 dB)** are fixed once and shared by all systems. What differs is
only the **transmitted far-end output**: inside the self-consistent loop it is
obtained by encoding and decoding the far-end speech through **each system's
own** codec path. That transmitted output is then convolved with the *same* RIR
to form the echo, which is mixed with the *same* near-end speech.

Each system therefore sees its own microphone mixture — both are provided in the
page (UniCoFi loop / DeepVQE loop) — while the comparison remains fair and
reproducible: identical utterances, identical echo paths, identical levels, and
the same frozen receiver codec. For the noisy, reverberant and band-limited
conditions the degraded input is one and the same file for all systems, so those
rows are directly comparable as well.

All clips are taken from the same runs that produced the numbers reported in the
paper.

## Layout

```
index.html                 # listening page (generated)
links.md                   # direct links to every clip (generated)
audio/<condition>/sample<k>/{input,clean,unicore,<baseline>}.wav
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
plain static files; no build step is involved.

## Notes

- Clips are 24-kHz mono 16-bit PCM.
- Test utterances come from the LRAC 2025 open test set and the far-end material
  of the AEC Challenge, as described in the paper.
- The clips are provided for review; please cite the paper if you reuse them.
