# Changelog

All notable changes to the WLED-MIDI convention. This spec is versioned
independently; implementers pin a version.

## 0.6.2 — 2026-07-16

- **`strip` gains a fourth position function `zone`** — hold notes to light the LED **range**
  between the lowest and highest held note, in the channel's colour; releasing shrinks/clears it.
  Each channel owns one zone, so a keyboard's **split zones** show as coloured bands (left hand
  ch1, right hand ch2 → two colours) — a live **split-zone display**. Shipped in
  [wled-midi-web](https://github.com/openlamp/wled-midi-web) and [engine](https://github.com/openlamp/engine).

## 0.6.1 — 2026-07-16

- **`strip` gains a third position function `direct`** (index) — note number → a specific LED
  index, no pitch-to-position interpolation; for **sequencer / pixel-painting** use. Added from
  the first external-implementer feedback: [theTiPE](https://wled.discourse.group/t/control-wled-led-strip-via-midi-keyboard/15448)
  ([tim-peters/WLED-Midi-Keyboard](https://github.com/tim-peters/WLED-Midi-Keyboard)) pairs an
  `interpolate` keyboard with a direct-addressing touch area, independently confirming the
  "offer both, don't force a choice" (modes-as-configs) philosophy.

## 0.6.0 — 2026-07-15

**Reframed from "3 modes" to ONE unified MPE-aware syntax** — you reach *any* mode through a
single spec, configured by the MIDI channel/zone layout (no separate dialects):

- **Channel 1 = plain MIDI, always** — the universal control floor any simple tool can emit.
- **Channels 2–16 = declared per use** via **MPE zones**: an MPE voice-zone (for `strip` /
  `mpe`) *coexists* in one port with non-zone channels used as **dedicated lamp targets**
  (verified against the MPE Configuration Message; the ROLI Seaboard does exactly this).
- **Expression = MPE-native messages** (pressure → bri, pitch-bend 14-bit → hue, CC 74 → sat,
  *per note*), not 7-bit CC — 7-bit CC stays for global control on ch1.
- New **`lamp` big-rig variant**: 1 note = 1 lamp (128 addressable) for rigs > 16 lamps.
- Added a **per-actor fit table** justifying the single syntax serves every forum actor ideally
  (one honest caveat: cross-device matrix needs a router / Extensions §8).

## 0.5.2 — 2026-07-15

- **Scope now covers cross-device matrix / canvas** (Extensions §8, advisory). Specifies a
  named **canvas** (ordered `(device, segment, offset)` tiles), MIDI control over the whole
  canvas, and two effect strategies — *mirrored* (same fx on all members) or *unified* (router
  streams each device its slice over WLED's realtime input: **DDP / Art-Net / E1.31**). Runs on
  any LAN coordinator (a Raspberry Pi). Covers the forum's club/large-rig ask instead of
  declaring it out of scope.

## 0.5.1 — 2026-07-15

- **Targeted use cases** section added (illustrative, no wire change): enumerates the concrete
  applications per mode, incl. **split-zone display** — colour LED ranges to show a keyboard's
  split zones, pairing with the Ableton **Zone** M4L device ([Beennnn/zone-m4l](https://github.com/Beennnn/zone-m4l)).
  Records which frontends implement which modes today.

## 0.5.0 — 2026-07-15

**Modes framework** — the note/channel interpretation now forks into three mutually-exclusive
modes over a shared universal base (channel/CC/PC/tempo/rules). Verified to cover every
MIDI-related need on the WLED forum.

- **`lamp`** (default, = the old Core note model; the reference impl's `group` mode) — note =
  a look/action. Covers control-surface asks (FX/colour/speed, presets, venue).
- **`strip`** (new, §13) — note pitch → a **LED position**, with two position functions:
  `interpolate` (proportional, stage strip behind the keys) and `keymap` (calibrated 1:1 to
  physical keys — a **piano-guide**). Velocity → brightness, note-off → fade, polyphonic,
  channel → colour/hand option. Basic guide in-scope; falling-notes/preview out (needs score
  look-ahead). Prior art: MusicalBasics "How To Make Your Own LED Piano", onlaj/Piano-LED-Visualizer,
  tim-peters/WLED-Midi-Keyboard.
- **`mpe`** (§12, unchanged) — reframed explicitly as a mode.
- **Extensions (§8)** gains **multi-device matrix / canvas** (cross-device composition — the
  club/large-rig ask), explicitly *not* a note mode.

## 0.4.1 — 2026-07-15

- **§7 rate-limit corrected** (advisory only, no wire change). The old "~4 cmd/s over HTTP"
  ceiling was too conservative and had a typo. Real-world evidence (tim-peters/WLED-Midi-Keyboard
  runs `/json/state` at ~30 req/s, ≤33 ms) shows the limit is **per device and batching-dependent**:
  coalesce a window's changes into one `POST`. New guidance recommends per-window batching; UDP
  reserved for very high rates / per-pixel.

## 0.4.0 — 2026-07-15

- **LOOKS gains `black` (note 59)** — black + white now **anchor** the colour bank (the
  two achromatic ends) around the seven hues (59–67 colours, 68 effect). `black` sets the
  colour to black — distinct from `blackout` (util 53 = `bri:0`). `mapping.spec.json` +
  `resolve.py` `--selftest` updated.
- **DAW-neutral wording throughout** — the convention is frontend/DAW-agnostic. Tempo
  reframed as *MIDI Clock (Core) + optional session clock* (Ableton Link kept only as one
  example); MPE and MIDI-2.0 DAW references generalised. No behaviour change.

## 0.3.0 — 2026-07-14

Profiles beyond the MIDI-1.0 core.

- **MIDI 2.0 forward-compat profile** (§11) — advisory mapping of high-resolution CC
  (16/32-bit → WLED 8-bit) for step-free fades; per-note controllers; a future
  auto-discoverable Profile. Core stays 1.0 (mainstream DAWs have no MIDI 2.0 yet).
- **MPE profile** (§12) — a separate mode (channel = per-note voice, mutually exclusive
  with channel-as-group): note → base hue, pressure → brightness, CC74 → saturation,
  pitch-bend → hue shift. Reference impl: `engine/midi.py` `"mode": "mpe"`. Works in
  MPE-capable DAWs today (Bitwig, Logic, Ableton Live 11+, …).
- `mapping.spec.json` gains a `profiles` block.

## 0.2.0 — 2026-07-14

Note model redesigned into **zones** (breaking: note semantics changed).

- **LOOKS** (notes 60–68, mutually exclusive) — what the lamp shows: 8 colours (now
  each also sets `fx:0` so a colour exits any effect) + a new **effect** look (68).
- **UTIL** (48–56) — off/on/toggle/blackout/restore/solid (unchanged numbers).
- **MODIFIERS** (72–75) — overlay the current look: **beat** toggle (72, pulse on the
  beat via a tempo source) and **flash** (73); 74/75 reserved. Beat is a *modifier*,
  not a peer look — you get *colour + beat*, *effect + beat*.
- **Velocity → brightness** — optional, off by default (§4.4).
- `mapping.spec.json` notes now carry a `zone` + payload; `channels` doc unchanged.

## 0.1.0 — 2026-07-14

Initial draft.

- Core: channel→target, notes 60–67 → colours, power/state notes, CC 1–8
  (bri/cct/hue/sat/fx/sx/ix/pal) with normative transforms, Program Change → preset,
  MIDI Clock (or session clock) → tempo.
- Extensions layer (groups, snapshots, non-WLED, command tokens) sketched as
  advisory.
- `mapping.spec.json` machine-readable default; `examples/payloads.md`.
