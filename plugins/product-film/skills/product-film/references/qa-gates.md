# Gates

| Gate | Measures | Tool |
|---|---|---|
| Lint | composition contract, contrast | the renderer's own check (HyperFrames `check`) |
| Claims | every visible string sourced; required items present; exact lists | registry script over the generated HTML |
| R | reading time per text node | `scripts/reading_rule.py` |
| Disclosure | "Sample data" readable in every product frame | `scripts/ocr_gate.py` (macOS Vision via `ocr.swift`) |
| Status truth | a Pending badge reads "Pending" in every frame of its scene | `scripts/ocr_gate.py` |
| Forbidden names | no old or real-business name in any real-footage frame | `scripts/ocr_gate.py --forbid` |
| Network | zero requests reached the network outside the local build | capture harness log |
| M1 | music-only energy lift at the chosen section bars | `scripts/mix.py` |
| M2 | SFX onset at least 6 dB at every slide start | `scripts/mix.py` |
| Loudness | -14 LUFS integrated (plus or minus 1), true peak at or below -1 dBTP | `scripts/mix.py` |
| M3 | a human listens on headphones, laptop and phone | owner |

Always run a negative control for OCR gates (a frame where the text must NOT be
found), so you know the gate can fail.
