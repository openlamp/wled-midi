# wled-midi — documentation

Topic map for the [wled-midi convention](../README.md). The **normative spec is a single,
atomic file** ([SPEC.md](../SPEC.md)) — one source of truth, no cross-file drift; this index
segments the docs **by topic** and points into it. Hardware and tooling live on their own pages.

## Protocol — in [SPEC.md](../SPEC.md)

- [One unified syntax](../SPEC.md) — channel 1 = plain-MIDI floor (universal); channels 2–16 declared per use via **MPE zones**; every "mode" is a configuration of one syntax.
- [`lamp` mode](../SPEC.md) — notes → looks / power / modifiers, channel = a lamp/group (+ the *1 note = 1 lamp* big-rig variant).
- [`strip` mode](../SPEC.md) — note → a LED **position** (`interpolate` | `keymap` piano-guide), animated per voice.
- [`mpe` mode](../SPEC.md) — per-note expressive voices (pressure → bri, bend → hue, CC 74 → sat).
- [CC & tempo](../SPEC.md) — CC 1–8 params; MIDI clock / session clock → on-the-beat.
- [Extensions — multi-device matrix](../SPEC.md) — a club canvas across several WLED instances via a router (DDP / Art-Net / E1.31).
- [Per-actor fit table](../SPEC.md) — justification that one syntax serves every forum actor.
- Machine-readable map: [mapping.spec.json](../mapping.spec.json) · executable resolver: [resolve.py](../resolve.py) · examples: [examples/payloads.md](../examples/payloads.md).

## Hardware

- [Piano-aligned LED strip](hardware/piano-strip.md) — dense strip + note→LED mapping, the density insight, BOM, calibration, references.
- [WLED lamp(s)](hardware/lamp.md) — the simplest rig (a pre-flashed WLED bulb).

## Tooling & credits — in the [README](../README.md)

- [Tooling to build & test](../README.md#credits--prior-art) — ShowMIDI (visualizer), MIDI Friend (generator), loopMIDI / rtpMIDI (Windows ports/network), Bome (adapter/router), IAC (macOS ports).
- [Expressive controllers & MPE sources](../README.md#credits--prior-art) — ROLI Seaboard, Expressive E Touché, TEControl BBC2, Beatbars, Omnisphere.
- [Credits & prior art](../README.md#credits--prior-art) — forum threads, projects, kindred products (Punchlight), tools.
