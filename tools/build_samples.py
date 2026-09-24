#!/usr/bin/env python3
"""Collect the listening samples for the UniCoFi demo page.

Four test conditions are covered (clean is excluded), three utterances each.
Utterances are picked where UniCoRe leads its task-specific baseline by the
largest margin in the primary metric (PESQ for noisy/reverb/BWE, ESTOI for AEC):

  noisy   LRAC Track-2 noisy test set          baseline: DPCRN + CleanCodec
  reverb  LRAC Track-2 reverberant test set    baseline: DPCRN + CleanCodec
  bwe     8-kHz band-limited test set          baseline: AP-BWE + CleanCodec
  aec     self-consistent double-talk set      baseline: DeepVQE + CleanCodec

Every clip is converted to 24-kHz mono 16-bit PCM so that the page keeps a
uniform, reasonably small footprint.

In the self-consistent AEC loop the far-end signal is decoded by each system's
own codec path, so every system sees its own microphone mixture; the UniCoRe and
DeepVQE microphone inputs are therefore both exported.

Run from the repository root:  python3 tools/build_samples.py
"""

import os
import subprocess

ROOT = "/data/ssd0/yufei.xiang"
LRAC = "/data/ssd0/ronghui.hu/DATA/LRAC-2025-test-data/open-test-set/track_2"
TEST = f"{ROOT}/stage2_student/offline_test_distorted"
UC = f"{ROOT}/stage2_student_v2_1/exp/exp_asa_film_v2"
DP = f"{ROOT}/dpcrn_local_train/eval/results/eval_samples/Track2/high"
DV = (f"{ROOT}/deepvqe/exp/deepvqe_24k_cleancodec_2026-09-05-13h21m/test_results/"
      "self_consistent_cleancodec/eval_samples/Track2/high")
AB = (f"{ROOT}/AP-BWE/checkpoints/"
      "AP-BWE_8kto24k_local_256_disc_half_2026-09-22-22h18m16s/test_results/"
      "apbwe_256_disc_half_cleancodec_g180000/eval_samples/Track2/high/bwe/"
      "g_00180000/wav")

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)

# condition -> (list of source indices, system -> source path template)
PLAN = {
    "noisy": dict(
        indices=[432, 37, 86],
        sources={
            "input":   f"{LRAC}/noisy/T2_noise_speech_file{{idx:03d}}.wav",
            "clean":   f"{LRAC}/reference_noisy/T2_noise_speech_file{{idx:03d}}.wav",
            "unicore": f"{UC}/eval_samples_v2/Track2/high/noisy/best_model_395/utt{{idx:04d}}_enh.wav",
            "dpcrn":   f"{DP}/noisy/dpcrn_codec_e330/wav/utt{{idx:04d}}_enh.wav",
        },
    ),
    "reverb": dict(
        indices=[43, 162, 51],
        sources={
            "input":   f"{LRAC}/reverb/T2_reverb_speech_file{{idx:03d}}.wav",
            "clean":   f"{LRAC}/reference_reverb/T2_reverb_speech_file{{idx:03d}}.wav",
            "unicore": f"{UC}/eval_samples_v2/Track2/high/reverb/best_model_395/utt{{idx:04d}}_enh.wav",
            "dpcrn":   f"{DP}/reverb/dpcrn_codec_e330/wav/utt{{idx:04d}}_enh.wav",
        },
    ),
    "bwe": dict(
        indices=[100, 41, 7],
        sources={
            "input":   f"{TEST}/bwe/{{idx:06d}}.wav",
            "clean":   f"{TEST}/clean/{{idx:06d}}.wav",
            "unicore": f"{UC}/eval_samples_v2/Track2/high/bwe/best_model_395/{{idx:06d}}_enh.wav",
            "apbwe":   f"{AB}/{{idx:06d}}_enh.wav",
        },
    ),
    "aec": dict(
        indices=[185, 104, 35],
        sources={
            "input":   f"{UC}/eval_samples_closed_loop/Track2/high/aec/best_model_395/mic/{{idx:06d}}_mic.wav",
            "input_bl": f"{DV}/aec/best_model_0385/mic/{{idx:06d}}_mic.wav",
            "clean":   f"{UC}/eval_samples_closed_loop/Track2/high/aec/best_model_395/target/{{idx:06d}}_target.wav",
            "unicore": f"{UC}/eval_samples_closed_loop/Track2/high/aec/best_model_395/{{idx:06d}}_enh.wav",
            "deepvqe": f"{DV}/aec/best_model_0385/{{idx:06d}}_enh.wav",
        },
    ),
}


def convert(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", src,
         "-ac", "1", "-ar", "24000", "-c:a", "pcm_s16le", dst],
        check=True,
    )


def main():
    count = 0
    for cond, plan in PLAN.items():
        for k, idx in enumerate(plan["indices"], start=1):
            for system, template in plan["sources"].items():
                src = template.format(idx=idx)
                if not os.path.exists(src):
                    raise FileNotFoundError(src)
                dst = os.path.join(OUT, "audio", cond, f"sample{k}",
                                   f"{system}.wav")
                convert(src, dst)
                count += 1
    print(f"wrote {count} clips -> {OUT}/audio")


if __name__ == "__main__":
    main()
