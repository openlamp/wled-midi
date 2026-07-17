# TASKS — wled-midi

Technical roadmap for the convention and its reference implementations. One item = a piece of
convention or implementation work.

## Shipped

- **Spec + validator** — [`SPEC.md`](SPEC.md), machine-readable [`mapping.spec.json`](mapping.spec.json),
  and [`resolve.py`](resolve.py) (turns any MIDI event into the WLED JSON it means; `--selftest`
  checks every note/CC).
- **`lamp` mode** — looks (59–68), util (48–56), modifiers (72–73), CC 1–8, Program Change → preset.
- **`strip` mode** — note pitch → LED position, polyphonic, velocity → brightness, individual-LED
  payload. Four position functions: `interpolate`, `keymap` (piano-aligned), `direct` (index),
  `zone` (hold notes → light the range between them; split-zone display). Note-off fade;
  channel → hand colour (Synthesia L/R).
- **`mpe` mode** — per-note voice as a positional LED zone (pitch → position + hue, pressure → bri,
  CC74 → sat, pitch-bend → hue), polyphonic.
- **Channel → segment routing** (`lamp`) and the **per-window batching** of the beat pulse (SPEC §7).
- **Reference implementations**:
  - [openlamp/engine](https://github.com/openlamp/engine) — the reference engine (`midi.py`).
  - [openlamp/wled-midi-web](https://github.com/openlamp/wled-midi-web) — single-HTML Web-MIDI impl,
    full 3-mode parity, zero-install via the WLED filesystem.
  - [openlamp/matrix](https://github.com/openlamp/matrix) — multi-device canvas router: `mirror`
    (HTTP broadcast) + `unified` (per-device slice via realtime **DDP / Art-Net / E1.31**), plus a
    2-D **serpentine** canvas (`posfn: "column"`).
  - [openlamp/bome](https://github.com/openlamp/bome) — no-code Bome MIDI Translator adapter pack.
  - **Bidirectional feedback port** in the engine (`OpenLamp Feedback` MIDI OUT) reflecting state.

## Roadmap

- **Hardware verification** — the implementations are self-tested but the individual-LED `seg[].i`
  path (strip / mpe / matrix) and the realtime transports are **unverified on a physical device**.
  Helper ready: [`bin/wled-verify.py`](bin/wled-verify.py) sends the payloads to a WLED IP to eyeball.
- **`keymap` calibration** — standardise the note→LED mapping on dense strips, folding in the
  LEDs-per-key approach of the reference open-source visualiser
  [onlaj/Piano-LED-Visualizer](https://github.com/onlaj/Piano-LED-Visualizer) (prior art), so any
  dense strip becomes MIDI-compatible via the convention.
- **Piano-guide demo** — a `strip`/`keymap` example that lights the key to play.
- **Split-zone via Max for Live** — wire a Zone M4L device to emit zone bounds + colour into the
  `zone` posfn.
- **MIDI 2.0 profile** — ingest high-res CC once a MIDI-2.0 source is available (step-free fades).
- **Bome pack** — verify the paste round-trip on a real Bome install; optional controller presets.
- **Feedback: real state** — optionally reflect a device's actual state (external changes), not just
  the commands processed.
