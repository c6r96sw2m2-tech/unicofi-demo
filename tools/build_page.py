#!/usr/bin/env python3
"""Generate index.html for the UniCoFi listening demo.

Run from the repository root:  python3 tools/build_page.py
"""

import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# condition -> page metadata
CONDITIONS = {
    "noisy": dict(
        title="Noisy speech",
        blurb="LRAC Track-2 noisy test set. The baseline is "
              "DPCRN cascaded with the same frozen CleanCodec.",
        protocol="The noisy input is the same file for every system, so the rows "
                 "are directly comparable.",
        baseline="dpcrn",
        baseline_label="DPCRN + CleanCodec",
        input_label="Noisy input",
        extra_rows=[],
        metrics=dict(
            header=["System", "PESQ↑", "UTMOS↑"],
            rows=[["DPCRN + CleanCodec", "2.27", "3.21"],
                  ["UniCoRe", "2.44", "3.61"]],
        ),
    ),
    "reverb": dict(
        title="Reverberant speech",
        blurb="LRAC Track-2 reverberant test set. Baseline: DPCRN cascaded with "
              "the same frozen CleanCodec.",
        protocol="The reverberant input is the same file for every system, so the "
                 "rows are directly comparable.",
        baseline="dpcrn",
        baseline_label="DPCRN + CleanCodec",
        input_label="Reverberant input",
        extra_rows=[],
        metrics=dict(
            header=["System", "PESQ↑", "UTMOS↑"],
            rows=[["DPCRN + CleanCodec", "1.42", "1.86"],
                  ["UniCoRe", "1.93", "3.29"]],
        ),
    ),
    "bwe": dict(
        title="Band-limited speech (8 → 24 kHz)",
        blurb="Bandwidth extension from an 8-kHz band-limited input. Baseline: "
              "AP-BWE cascaded with the same frozen CleanCodec.",
        protocol="The 8-kHz input is the same file for every system, so the rows "
                 "are directly comparable.",
        baseline="apbwe",
        baseline_label="AP-BWE + CleanCodec",
        input_label="8-kHz input",
        extra_rows=[],
        metrics=dict(
            header=["System", "ViSQOL↑", "LSD↓"],
            rows=[["AP-BWE + CleanCodec", "3.77", "0.93"],
                  ["UniCoRe", "3.89", "0.84"]],
        ),
    ),
    "aec": dict(
        title="Acoustic echo (double-talk)",
        blurb="Self-consistent closed-loop double-talk set. Baseline: DeepVQE "
              "cascaded with the same frozen CleanCodec.",
        protocol="""<strong>How to read this condition.</strong> For each test
                 utterance the <em>near-end speech</em>, the <em>far-end speech</em>
                 to be transmitted, the <em>room impulse response (RIR)</em> and the
                 <em>signal-to-echo ratio (SER, &minus;20 to 10 dB)</em> are fixed
                 once and shared by every system. The only quantity that differs is
                 the <em>transmitted far-end output</em>: inside the closed loop it
                 is obtained by encoding and decoding the far-end speech through
                 <em>each system's own</em> codec path. That transmitted output is
                 then convolved with the same RIR to form the echo and mixed with
                 the same near-end speech, so every system sees its own microphone
                 mixture (both are shown above). The comparison stays fair and
                 reproducible &mdash; the utterances, echo paths and levels are
                 identical; only the transmit/receive chain differs.""",
        baseline="deepvqe",
        baseline_label="DeepVQE + CleanCodec",
        input_label="Microphone input (UniCoRe loop)",
        extra_rows=[("input_bl", "Microphone input (DeepVQE loop)",
                     "before", 1)],
        metrics=dict(
            header=["System", "ESTOI (%)↑", "PESQ↑", "UTMOS↑",
                    "AECMOS (Echo)↑", "AECMOS (Other)↑", "ERLE (dB)↑"],
            rows=[["DeepVQE + CleanCodec", "68.71", "1.79", "2.63", "4.52",
                   "3.63", "42.44"],
                  ["UniCoRe", "76.30", "2.06", "3.28", "4.60", "3.91",
                   "61.81"]],
        ),
    ),
}


def audio_cell(path):
    return (f'<audio controls preload="none" src="{html.escape(path)}">'
            f'</audio>')


def main():
    samples = ["sample1", "sample2", "sample3"]

    parts = ["""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>UniCoFi - listening samples</title>
<style>
  :root { color-scheme: light dark; }
  body { font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
         max-width: 1080px; margin: 0 auto; padding: 24px 18px 64px;
         line-height: 1.5; }
  h1 { font-size: 1.6rem; margin-bottom: .2em; }
  h2 { font-size: 1.2rem; margin-top: 2.2em; border-bottom: 1px solid #8884;
       padding-bottom: .2em; }
  .lead { color: #666; }
  .blurb { max-width: 70ch; }
  .protocol { max-width: 78ch; background: #8881; border-left: 3px solid #0a7d32;
              padding: 8px 12px; border-radius: 4px; font-size: .92rem; }
  table { border-collapse: collapse; margin: 1em 0 1.4em; font-size: .92rem; }
  th, td { border-bottom: 1px solid #8883; padding: 6px 10px; text-align: left;
           vertical-align: middle; }
  th { font-weight: 600; }
  audio { width: 220px; height: 32px; }
  .sys { font-weight: 600; white-space: nowrap; }
  .sys.best { color: #0a7d32; }
  .metric { font-size: .88rem; }
  .metric td:not(:first-child), .metric th:not(:first-child) { text-align: right; }
  footer { margin-top: 3em; font-size: .9rem; color: #666; }
  code { background: #8881; padding: 0 .25em; border-radius: 3px; }
</style>
</head>
<body>
<h1>UniCoFi &mdash; listening samples</h1>
<p class="lead">Audio examples for <em>UniCoFi: Unified Codec-Domain Speech
Restoration with Far-End Decoder Feature Reuse</em>. All systems share the same
frozen CleanCodec backend; only the front end differs.</p>
<p class="blurb">Each condition shows three held-out utterances (the clean test
set is omitted, as it carries no degradation). Clips are 24-kHz mono 16-bit PCM.
For AEC the microphone input is generated inside the self-consistent closed loop
and already contains the far-end echo that the system has to remove.</p>
"""]

    for cond, meta in CONDITIONS.items():
        systems = [("input", meta["input_label"])]
        for key, label, _pos, _idx in meta.get("extra_rows", []):
            systems.append((key, label))
        systems += [("clean", "Clean / near-end reference"),
                    ("unicore", "UniCoRe (ours)"),
                    (meta["baseline"], meta["baseline_label"])]
        labels = {
            "input": meta["input_label"],
            "clean": "Clean / near-end reference",
            "unicore": "UniCoRe (ours)",
            meta["baseline"]: meta["baseline_label"],
        }
        labels.update({k: v for k, v, _p, _i in meta.get("extra_rows", [])})
        parts.append(f"<h2>{html.escape(meta['title'])}</h2>")
        parts.append(f"<p class=\"blurb\">{meta['blurb']}</p>")
        if meta.get("protocol"):
            parts.append(f"<p class=\"protocol\">{meta['protocol']}</p>")
        parts.append('<table class="metric"><thead><tr>' +
                     "".join(f"<th>{html.escape(h)}</th>"
                             for h in meta["metrics"]["header"]) +
                     "</tr></thead><tbody>")
        for row in meta["metrics"]["rows"]:
            cls = ' class="sys best"' if row[0].startswith("UniCoRe") else ""
            parts.append("<tr>" + f"<td{cls}>{html.escape(row[0])}</td>" +
                         "".join(f"<td>{html.escape(v)}</td>"
                                 for v in row[1:]) + "</tr>")
        parts.append("</tbody></table>")

        parts.append("<table><thead><tr><th>System</th>" +
                     "".join(f"<th>{s}</th>" for s in samples) +
                     "</tr></thead><tbody>")
        for sys_, name in systems:
            name = labels[sys_]
            cls = ' class="sys best"' if sys_ == "unicore" else ' class="sys"'
            cells = []
            for s in samples:
                path = f"audio/{cond}/{s}/{sys_}.wav"
                cells.append("<td>" + (audio_cell(path)
                                       if os.path.exists(os.path.join(ROOT, path))
                                       else "&mdash;") + "</td>")
            parts.append(f"<tr><td{cls}>{html.escape(name)}</td>" +
                         "".join(cells) + "</tr>")
        parts.append("</tbody></table>")

    parts.append("""<footer>Sample clips are provided for review purposes. Test
utterances come from the LRAC 2025 open test set and the AEC Challenge material
referenced in the paper.</footer>
</body>
</html>
""")

    out = os.path.join(ROOT, "index.html")
    with open(out, "w", encoding="utf8") as fh:
        fh.write("\n".join(parts))
    print("wrote", out)


if __name__ == "__main__":
    main()
