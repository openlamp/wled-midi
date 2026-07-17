# WLED-MIDI — a convention for controlling WLED over MIDI

**Version 0.6.3** · status: draft · license: MIT · patent policy: royalty-free, non-assertion (§14)

A small, open convention that maps standard MIDI messages to
[WLED](https://kno.wled.ge) actions, so any DAW, sequencer or hardware MIDI
controller can drive WLED lights **in time with music**. It targets WLED's
[JSON state API](https://kno.wled.ge/interfaces/json-api/) (`POST /json/state`)
and, where higher rates are needed, WLED's realtime UDP.

The spec has two layers:

- **Core** — pure WLED. Every mapping resolves to a documented WLED JSON-state key.
  Any implementer can adopt it against a stock WLED device, no extra software.
- **Extensions** — optional, for stacks that add grouping across multiple devices,
  snapshots, or non-WLED lamps (e.g. the [OpenLamp](https://github.com/openlamp)
  engine). Clearly separated so the Core stays universal.

Everything is normative in the Core; Extensions are advisory.

### One unified syntax — every mode is a *configuration* of it

There aren't three dialects — there is **one syntax**, and each "mode" is a **configuration**
of it, reached through the MIDI **channel / zone** layout. The spine never changes (notes §4,
CC §5, Program Change §6, tempo §7); the only thing that varies is what a *channel* means —
and MIDI already has a standard way to declare that (**MPE zones**).

**Channel 1 is plain MIDI, always — the universal floor.** It carries the control layer:
notes → looks/actions (§4), CC → params (§5), PC → presets (§6), clock → tempo (§7). Any tool
that speaks basic MIDI (a Stream Deck plugin, a Bome preset, a DAW clip) drives WLED through
channel 1 with **zero ceremony**. Mandatory; everything else is opt-in on top.

**Channels 2–16 are declared per use — same syntax, different configs:**

| Config | Ch 2–16 = | Note = | For |
|---|---|---|---|
| **`lamp`** (default) | a **lamp / group** (one per channel) | a look/action | stage & control surfaces (frankofino, faltim, miledy, Mauri, zumdar) |
| **`lamp` · big-rig** | *(a control channel)* | **a lamp** (1 note = 1 lamp) | rigs with **> 16 lamps** (128 addressable on one channel) |
| **`strip`** | an **MPE voice-zone** | a **position** (2–3 LEDs, animated per voice) | strip-as-instrument · **piano-guide** (theTiPE, onlaj) |
| **`mpe`** | an **MPE voice-zone** | an **expressive voice** | expressive multi-lamp play (Seaboard · Push 3 · TEControl breath) |

**The two coexist in one port (verified against the MPE spec).** MPE's *Configuration Message*
(RPN) declares a **zone** = master channel 1 + a configurable number of member channels.
Channels **outside** the zone stay ordinary single-channel MIDI — free to be **dedicated lamp
targets**. So one port can run e.g. `zone = ch1 + ch2–8` (7 strip voices) **and** `ch9–16` as
8 lamps, in the *same* syntax. (The ROLI Seaboard exposes exactly this: single-channel MIDI ↔
MPE, with a settable zone size.)

**Expression uses MPE-native messages, not 7-bit CC.** Per voice: brightness = channel
pressure, hue = pitch-bend (14-bit), saturation = CC 74 — each *per note, simultaneously*.
7-bit CC stays for **global** control on channel 1. (That per-note independence is exactly what
a plain 7-bit CC on one channel cannot give — it's the whole point of MPE.)

**Cross-device composition** — one matrix spanning several WLED instances (a club rig) — is the
only thing outside this single syntax: it needs a router, covered by the Extensions layer (§8).

So you reach **any mode through one unified spec**: a simple lamp and an expressive strip are
the *same* language, configured differently. §4 (`lamp` notes), §12 (`mpe`), §13 (`strip`) each
describe one configuration of this syntax.

### Targeted use cases

The concrete applications the modes are meant to serve — this is what "covers the need"
means:

- **`lamp`** — stage-lighting control; live FX / colour / speed from a controller; preset
  stepping; Stream-Deck & pad control surfaces.
- **`strip`**
  - *strip-as-instrument* — play an addressable strip melodically (theTiPE's tool).
  - *piano-guide* — a strip on the keys lights the note to play (`keymap`); learning / Synthesia.
  - *split-zone display* — colour LED **ranges** to show a keyboard's **split zones** (which key
    range drives which instrument), pairing with a split/zone tool such as the Ableton **Zone**
    M4L device ([Beennnn/zone-m4l](https://github.com/Beennnn/zone-m4l)): a zone = a contiguous
    position range painted with the zone's colour.
  - *stage backdrop* — a strip behind the keys as a show element (`interpolate`).
  - *sequencer / pixel-painting* — address individual LEDs directly (`direct`), à la theTiPE's touch area.
- **`mpe`** — expressive, per-note play across a pool of lamps (Seaboard / Push 3).
- **Extensions** — a cross-device matrix / canvas for club & large rigs (§8).

*Implementations today*: `engine/midi.py` = `lamp` + `mpe`; [wled-midi-web](https://github.com/openlamp/wled-midi-web)
= `lamp` in the browser (Web MIDI); the Ableton clip pack emits `lamp`. `strip`
(piano-guide + split-zone) is spec'd here and on the implementation roadmap.

### Does one syntax serve everyone? — per-actor fit

Every actor reaches what they need **through the same unified syntax**. This table justifies
that the design fits each ideally (or names the one honest caveat):

| Actor / need | Reached through | Ideal fit? | Justification |
|---|---|---|---|
| **Simple emitter** (Stream Deck, Bome, DAW clip) | channel 1, plain MIDI | ✅ | No MPE to emit — basic notes/CC on ch1. The 90% case stays trivial. |
| **frankofino** — full control of a live matrix | `lamp` on ch1 (CC / PC) | ✅ | Pure control, no voices needed. CC → FX/bri/hue, PC → presets = exactly ch1. |
| **faltim** — club, change FX/colour/speed live | `lamp` control + Extensions matrix | ✅ | Control is ch1; the multi-instance canvas is the router (§8) — honestly separate. |
| **miledy** — Push 2 pads → segments | `lamp` (pads = notes → looks, ch = segment) | ✅ | 64 pads map to looks/segments; no expression needed. |
| **Mauri** — step presets from a pad | `lamp` PC on ch1 | ✅ | Program Change → preset. One message. |
| **theTiPE** — play a strip like an instrument | `strip` MPE-zone (or plain ch1 for the simple case) | ✅ | Note → position + per-voice animation via MPE; can also stay plain on ch1 if no expression is wanted. |
| **Piano-guide user** — light the key to play | `strip` / `keymap`, firmware interpolation | ✅ | Drive with a note; firmware maps note → LED via calibration (dense-strip reality — onlaj). |
| **MPE player** (Seaboard, Push 3, **TEControl breath**) | `mpe` zone | ✅ | Per-note pressure/bend/CC 74 → per-voice bri/hue/sat, polyphonic — the reason MPE exists. |
| **Big-rig owner** — > 16 lamps | `lamp` · **1 note = 1 lamp** | ✅ | 16 channels cap device-per-channel at 16; notes give 128 addressable lamps on one channel. |
| **Multi-instance matrix** (club canvas) | **Extensions §8** (router + WLED realtime) | ⚠️ *served, not stock* | Genuinely needs a coordinator; honestly outside the per-device syntax, by design. |

**Verdict:** the unified syntax fits every actor ideally, with a single honest caveat — a
cross-device *matrix* needs a router (Extensions), because no single-device MIDI syntax can
compose across independent WLED instances. Everything else is one language: one channel-1
floor, opt-in MPE on top.

---

## 1. Transport

The implementer opens a **MIDI input** (a virtual port is recommended; this spec
does not mandate a port name) and translates incoming messages into WLED JSON-state
POSTs to one or more devices. For beat-rate control (pulsing on every beat), prefer
WLED **realtime UDP** or rate-limit HTTP (see §7).

Byte notation: `sn dd dd` where `s` = message type nibble, `n` = channel nibble.

## 2. Channel → target  *(Core)*

`channel = (status & 0x0F) + 1`  → 1–16.

Each MIDI channel addresses **one target**: a WLED device (by IP/host) or a segment
index on a device. The channel→target table is the implementer's routing config.

- A channel **not in the table is ignored** (unrelated MIDI never touches the lights).
- Default suggestion: channel 1 = the (only) device, all segments.
- *(Extension)* a channel MAY map to a **named group** spanning several devices — see §8.

## 3. Message dispatch

| Status | Type | Meaning |
|---|---|---|
| `9n` | Note On (velocity > 0) | discrete action (§4) |
| `9n` vel 0 / `8n` | Note Off | **ignored** — actions fire on note-on only |
| `Bn` | Control Change | continuous parameter (§5) |
| `Cn` | Program Change | preset recall (§6) |
| `F8` | MIDI Clock | tempo (§7) |

## 4. Notes → zones  *(Core — `lamp` mode)*

This is the note model of the **default `lamp` mode**: a note is a *control* (pick a look
or fire an action), not a position or a voice. Notes are organised in three zones.
**Note-on only** (velocity > 0). All numbers are remappable; the zone semantics are the
contract.

### 4.1 LOOKS — what the lamp shows (notes 59–68, mutually exclusive)

Selecting a look is a solid state. A colour also sets `fx:0`, so choosing a colour
**exits any running effect** — looks stay mutually exclusive. **Black** and **white**
anchor the bank (the two achromatic ends) around the seven hues.

| Note | Look | WLED JSON |
|---|---|---|
| 59 | black | `{"seg":[{"col":[[0,0,0]],"fx":0}]}` |
| 60 | red | `{"seg":[{"col":[[255,0,0]],"fx":0}]}` |
| 61 | orange | `…[[255,85,0]]…` |
| 62 | yellow | `…[[255,200,0]]…` |
| 63 | green | `…[[0,255,0]]…` |
| 64 | cyan | `…[[0,200,255]]…` |
| 65 | blue | `…[[0,0,255]]…` |
| 66 | magenta | `…[[255,0,170]]…` |
| 67 | white | `…[[255,255,255]]…` |
| 68 | **effect** | enable the WLED effect look: `{"seg":[{"fx":F,"sx":S,"ix":I}]}` from the current CC 5/6/7 (default `fx:1`) |

The 9 colours (black + 7 hues + white) are an **instant-look bank** — one pad = one
look, ideal live. Note: `black` sets the *colour* to black (leaving brightness), which
differs from `blackout` (util 53 = `bri:0`).

### 4.2 POWER / UTIL — notes 48–56

| Note | Action | WLED JSON |
|---|---|---|
| 48 | off | `{"on":false}` |
| 50 | on | `{"on":true}` |
| 52 | toggle | `{"on":"t"}` |
| 53 | blackout | `{"bri":0}` |
| 55 | restore | `{"bri":<last>}` — implementer keeps last bri per target |
| 56 | solid | `{"seg":[{"fx":0}]}` — exit the effect look, back to solid colour |

### 4.3 MODIFIERS — overlay the current look (notes 72–75)

Modifiers are **not** looks: they layer a behaviour on top of whatever look is active
(so you get *colour + beat*, *effect + beat*, etc.).

| Note | Modifier | Behaviour |
|---|---|---|
| 72 | **beat** | toggle on/off — pulse the current look on the beat (brightness accent per beat, trough between). Needs a tempo source (§7). A session clock that exposes bar phase (e.g. Ableton Link) additionally enables a phase-accurate downbeat accent. |
| 73 | **flash** | momentary bright flash, then return to the look |
| 74 | reserved | (e.g. strobe) |
| 75 | reserved | (e.g. freeze) |

### 4.4 Velocity  *(optional)*

By default velocity is ignored (a look fires at its set brightness). Implementers MAY
enable **velocity → brightness**: a look note-on also sets `bri = round(vel/127*255)`.
Off by default (predictable), config-gated.

## 5. Control Change → continuous  *(Core)*

`v` = data byte (0–127). Transforms are normative.

| CC | Param | WLED JSON | Transform |
|---|---|---|---|
| 1 | brightness | `{"bri":B}` | `B = round(v/127*255)` |
| 2 | white temp | `{"seg":[{"cct":C}]}` | `C = round(v/127*255)` (relative 0–255) |
| 3 | hue | `{"seg":[{"col":[[R,G,B]]}]}` | see §5.1 |
| 4 | saturation | `{"seg":[{"col":[[R,G,B]]}]}` | see §5.1 |
| 5 | effect | `{"seg":[{"fx":F}]}` | `F = round(v/127*(fxcount-1))` |
| 6 | effect speed | `{"seg":[{"sx":S}]}` | `S = round(v/127*255)` |
| 7 | effect intensity | `{"seg":[{"ix":I}]}` | `I = round(v/127*255)` |
| 8 | palette | `{"seg":[{"pal":P}]}` | `P = round(v/127*(palcount-1))` |

`fxcount` / `palcount` come from the device's `GET /json/info`. If unknown, an
implementer MAY fall back to a fixed range (e.g. 0–100) and MUST document it.

### 5.1 Continuous colour (hue + saturation)

Hue (CC 3) and saturation (CC 4) are held **per channel** and combined:

```
hue = v/127            # on CC 3   (0 = red … 1.0 wraps to red)
sat = v/127            # on CC 4   (default 1.0 until set)
R,G,B = HSV_to_RGB(hue, sat, value=1.0) * 255
→ {"seg":[{"col":[[R,G,B]]}]}
```

Brightness stays independent (CC 1) — `value` in HSV is fixed at 1.0 so colour and
brightness don't fight.

## 6. Program Change → preset  *(Core)*

`Cn pp` → recall WLED preset:  `{"ps": pp + 1}`  (WLED presets are 1-based, 1–250;
MIDI program 0 → preset 1). Out-of-range presets are a WLED no-op.

## 7. Tempo — MIDI Clock (+ optional session clock)  *(Core)*

Two kinds of source, same intent — put the lights **on the beat**:

- **MIDI Clock** (`F8`): 24 ticks = 1 beat → `BPM = 60 / Δt(24 ticks)`. Works with any
  MIDI clock master; this is the Core source.
- **Session clock** (optional; e.g. Ableton Link): read the shared timeline; `phase`/
  `quantum` give the exact bar position → a **phase-accurate downbeat accent**
  (brighter/other colour on beat 1).

Use the beat to pulse brightness (`bri` up on the beat, down between) and/or to set
effect speed. **Rate limit — batch, don't spray.** Don't fire one HTTP request per
parameter. WLED's `/json/state` sustains a **higher rate than often assumed** when you
**coalesce** all changes within a short window (≈33 ms) into a **single** `POST` — a single
device holds **~30 req/s at ≤33 ms latency** in practice. The ceiling is **per device** and
falls as you fan out to many devices per beat; for very high rates or per-pixel work, use
WLED **realtime UDP** (DDP/WARLS). Implementers MUST bound their command rate, SHOULD
**batch per window**, and SHOULD document both.

## 8. Extensions  *(non-Core, advisory)*

For stacks richer than a single WLED device. These do **not** resolve to a single
WLED key and require an engine/router (e.g. [OpenLamp](https://github.com/openlamp)).

- **Groups** — a channel maps to a named group spanning several WLED devices (and
  non-WLED lamps). The router fans one command out to each member; WLED-only keys are
  skipped on non-WLED members.
- **Multi-device matrix / canvas** — several WLED instances composed into one logical LED
  space, driven as a whole from MIDI. This is how a **club / large rig** is covered:
  - **Canvas** = a named target = an ordered set of member `(device, segment, offset)` tiles
    forming one matrix or long strip. The router owns the layout.
  - **Control** — a channel addresses the canvas; `lamp` CC/notes (FX / colour / speed /
    presets) and `strip` positions apply to the **whole canvas**, the router mapping them to
    members. "Change FX / colour / speed live" is just CC on the canvas channel.
  - **Cross-device effects — two strategies**: *mirrored* — set the same `fx/pal/sx/ix` on
    every member (each runs the effect locally; simplest); or *unified* — the router computes
    **one** animation across the whole matrix and streams each device its slice over WLED's
    **realtime input** (**DDP / Art-Net / E1.31**, supported natively by WLED). Unified gives a
    single animation genuinely spanning instances.
  - **Where it runs** — any coordinator on the LAN (a Raspberry Pi is plenty).
  - **Why not just a VJ suite?** — the usual WLED route for a multi-instance canvas is
    Art-Net / E1.31 / **[DDP](http://www.3waylabs.com/ddp/)** (the lightweight, performant
    transport) from a VJ tool — [xLights](https://manual.xlights.org/), [Resolume](https://resolume.com),
    [MadMapper](https://madmapper.com). They work, but are either **not built for live
    control** (xLights) or **expensive** (Resolume). wled-midi's router fills that gap:
    **affordable, MIDI-driven, live**, on a Raspberry Pi. *(Confirmed by the club-use-case
    discussion on the WLED forum.)*
- **Snapshots** — capture/recall the whole rig's state as one look.
- **Named scenes / non-WLED devices** — e.g. Tuya lamps, DMX, via the engine's own
  command vocabulary.
- **Higher-level command tokens** — an engine MAY accept string commands
  (`flash:white@300`, `cycle:…`) triggered by notes; these are engine concepts, not
  Core WLED.

## 9. Conventions & rules

- Act on **note-on only** (velocity > 0); note-off and velocity-0 are ignored.
- Continuous state (hue/sat/effect) is tracked **per channel/target**.
- Unmapped channels and unmapped note/CC numbers are ignored (no surprises).
- All default numbers are remappable; the transforms in §5 are the stable contract.

## 10. Machine-readable default

The default number→action map lives in [`mapping.spec.json`](mapping.spec.json) so
tools can generate clips/tests from one source. See also
[`examples/`](examples/) for reference payloads.

## 11. MIDI 2.0 — forward-compat profile  *(advisory)*

The Core is **MIDI-1.0-native** (7-bit) — it works with every controller and DAW today.
WLED, though, is 8-bit (`bri` 0–255, colour 8-bit/channel), so 7-bit CC can't address its
full range: slow fades step visibly. A **MIDI 2.0 profile** removes that ceiling.
Implementers MAY accept MIDI 2.0 high-resolution messages and map them:

- **High-res Control Change** (16/32-bit, `0..65535`) → WLED value:
  `bri8 = round(v16 / 65535 * 255)` (likewise cct/hue/sat) → smooth, step-free fades.
- **16-bit note velocity** → look brightness at full resolution.
- **Per-Note (Registered) Controllers** → per-voice parameters — a natural home for the
  MPE-style expression in §12, *without* stealing channels.
- **Profiles / Property Exchange** → a future auto-discoverable "WLED lighting" profile
  (aspirational; an MMA-level effort, not defined here).

A 2.0 stream degrades cleanly to the 1.0 Core. As of 2026 mainstream DAW support is
uneven (Logic, Cubase 12+, Bitwig lead; several popular DAWs not yet), so this is
forward-looking — the Core stays 1.0.

*Prior art:* MIDI Show Control (MSC) already carries lighting cues over MIDI, but it's
cue-list/theatrical, not real-time colour — a different niche.

## 12. `mpe` mode — play the lamps expressively  *(mode, mutually exclusive with `lamp`/`strip`)*

MPE (MIDI Polyphonic Expression) reinterprets **channels as per-note voices**, so it
**collides with the Core's channel-as-group** and runs as a **separate mode** (a port is
either group-mode or MPE-mode). It turns the lamps into an expressive instrument — one
lamp per finger.

- **Zone**: a master channel + member channels (e.g. master 1, members 2–16).
- **Note-on** (member channel) → light a **voice** on a lamp from the pool. Pitch class →
  base hue (playing up the keyboard sweeps colour); velocity → initial brightness.
- **Channel Pressure** (Z) → that voice's **brightness**.
- **CC 74** slide / timbre (Y) → that voice's **saturation** (white ↔ pure).
- **Pitch Bend** (X) → that voice's **hue shift**.
- **Note-off** → release the voice.

Three MPE axes → three light parameters, all distinct. Works in any DAW that supports
MPE **today** (Bitwig, Logic, Ableton Live 11+, …) with a Seaboard / LinnStrument /
Push 3. The reference implementation is `engine/midi.py` with `"mode": "mpe"`.

## 13. `strip` mode — play a strip by position  *(mode, mutually exclusive with `lamp`/`mpe`)*

Here a **note pitch → a LED position** along an addressable strip (channel still selects
the strip/segment target, as in `lamp`). It turns a strip into an instrument, and —
calibrated to a keyboard — into a **piano-guide** that lights the key to play.

**Position function** (config):

- **`interpolate`** (default) — map the active note range `[lo, hi]` linearly onto the LED
  range `[LED_start, LED_end]`:
  `led = LED_start + round((note − lo) / (hi − lo) × (LED_end − LED_start))`.
  Options: octave offset (± semitones), *white-keys-only* (distribute only white keys, more
  musical). Aesthetic — for a strip mounted **behind** the keys / on stage.
- **`keymap`** (calibrated) — note → the physical LED(s) **above that key**. The calibration
  (LEDs-per-key or per-octave, which note is LED 0, an optional per-key table) is implementer
  config, **not wire**. For a strip stuck **on** the keys — a piano-guide.
- **`direct`** (index) — note number → a **specific LED index** directly, with no
  pitch-to-position interpolation (a pad-grid cell → its pixel). For **sequencer / pixel-painting**
  use — pick and light individual LEDs rather than play melodically. *(Added from implementer
  feedback: [tim-peters/WLED-Midi-Keyboard](https://github.com/tim-peters/WLED-Midi-Keyboard)
  pairs an `interpolate` keyboard with a direct-addressing touch area — "both modes have their
  place, I didn't want to force a choice", which is exactly the modes-as-configs spirit.)*
- **`zone`** (range) — **hold notes to light the LED range between the lowest and highest held
  note**, in the channel's colour. Releasing a boundary note shrinks the range; releasing all
  clears it. Each channel owns one zone, so a keyboard's **split zones** show as coloured bands
  (left hand ch1, right hand ch2 → two colours). A live **split-zone display**: press the edges
  of your split, see it on the strip. Note→position uses the `interpolate` `[lo, hi]` mapping.

**Per-note behaviour:**

- **Velocity → pixel brightness** (or a fixed guide brightness).
- **Note-off → fade** the pixel (fade time via a CC; default ~300 ms). Polyphonic — each
  note keeps independent `{position, fade}` state.
- **Colour** — the base hue/sat (CC 3/4) colour the played pixels. Option: **channel →
  colour/role** (left / right hand on two channels → two colours, Synthesia-style).
- **Payload** — WLED's individual-LED array `{"seg":[{"id":s,"i":[idx,[r,g,b], …]}]}`, with
  per-window **batching** (§7).

**Scope:** lighting the position on note-on — mirroring your play, or a **basic guide**
driven by an incoming song/tutorial — is in-mode. **Falling-notes / preview** (showing a
note *before* it is played) needs score look-ahead with timing → **impl-level, out of the
convention** (the wire only sees note-on).

**One strip, two roles:** the same firmware + a cheap addressable strip is a **piano-guide**
(`keymap`, on the keys) *and* a **stage backdrop** (`interpolate`, behind) — only the
calibration changes.

*Prior art:* [MusicalBasics — How To Make Your Own LED Piano](https://www.youtube.com/watch?v=B-lzFz1RM4E)
(drives the LEDs from Ableton), [onlaj/Piano-LED-Visualizer](https://github.com/onlaj/Piano-LED-Visualizer)
(reference Raspberry-Pi + WS2812 visualizer), [tim-peters/WLED-Midi-Keyboard](https://github.com/tim-peters/WLED-Midi-Keyboard),
Synthesia LED guides.

---

## 14. Patent & openness policy

This convention is meant to stay **free for everyone to implement** — in open-source and commercial
products alike. Two commitments make that durable:

**Defensive publication.** This specification is published openly and in dated form (this
repository's public history, from July 2026) as **prior art**. Once published, the mappings and
mechanisms it describes cannot be newly patented by anyone — *including the authors*. The convention
stays in the commons by design.

**Royalty-free, non-assertion.** The authors make **no patent claim** over this convention and
commit, on a **royalty-free, irrevocable, non-assertion** basis, **not to assert** any patent they
may hold against anyone who implements it. No permission, no licence fee, and no registration is
required to build on it. (This mirrors the royalty-free patent policy that keeps open web standards
adoptable by all.)

**Scope.** This covers *this convention* — the MIDI↔WLED mappings and the modes defined here. It does
**not** grant rights over third parties' patents (see the prior-art note in
[docs/hardware/piano-strip.md](docs/hardware/piano-strip.md)), and it is **not legal advice**: anyone
shipping a commercial product should still obtain their own freedom-to-operate opinion.

Code is licensed [MIT](LICENSE); this policy governs the *specification and its ideas*. Together they
keep the project's guiding line real — **advanced, integrated solutions usable by everyone**.

> **Code licence is an open question.** Whether the code stays MIT or moves to Apache-2.0 (for an
> explicit contributor patent grant) is **deliberately unsettled, pending WLED-community feedback** —
> see [docs/licensing.md](docs/licensing.md). This §14 convention policy holds either way.
