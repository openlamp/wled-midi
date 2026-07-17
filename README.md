# wled-midi

> **An open convention for controlling [WLED](https://kno.wled.ge) lights over MIDI.**
> Drive WLED from any DAW, sequencer or hardware MIDI controller — in time with your
> music. Notes → colours, CC → brightness/effects, Program Change → presets, MIDI
> Clock (or a session clock) → on-the-beat. 100 % local.

This repo is **just the specification** — no runtime, no dependencies. It exists so
that multiple tools can speak the same MIDI↔WLED language instead of each inventing
its own.

## Why a convention

WLED already exposes a clean [JSON state API](https://kno.wled.ge/interfaces/json-api/).
What's missing is an agreed **MIDI mapping** on top of it: which note is which
colour, which CC is brightness, how a channel targets a device. Pin that down once
and a Live set, a Stream Deck, a hardware pad controller and a lighting cue system
can all drive the same lamp identically.

## Two layers

- **Core** — pure WLED. Every mapping resolves to a documented WLED JSON key
  (`bri`, `seg[].col`, `fx`, `ps`…). Adoptable against a stock WLED device, no extra
  software.
- **Extensions** — optional (grouping across devices, snapshots, non-WLED lamps) for
  richer stacks like the [OpenLamp](https://github.com/openlamp) engine.

The note/channel interpretation runs in one of **three mutually-exclusive modes** over a
shared base (channel/CC/PC/tempo) — see SPEC *"Modes"*:

- **`lamp`** *(default)* — note = a look/action, channel = a lamp/group. The control mode
  (stage lighting, control surfaces).
- **`strip`** — note pitch → a **LED position**: `interpolate` for a stage strip behind the
  keys, `keymap` for a **piano-guide** stuck on the keys (lights the key to play). Play a
  strip like an instrument.
- **`mpe`** — channel = a per-note voice: play the lamps expressively (pressure → brightness,
  slide → saturation, bend → hue).

Plus a **MIDI 2.0** forward-compat profile (high-res CC → step-free fades); the Core stays
MIDI-1.0-native (mainstream DAWs have no MIDI 2.0 yet).

## The spec

👉 **[SPEC.md](SPEC.md)** — normative. Machine-readable default map:
[`mapping.spec.json`](mapping.spec.json). Executable reference:
[`resolve.py`](resolve.py) turns any MIDI event into the WLED JSON it means
(`python3 resolve.py cc 1 100` → `{"bri":201}`; `--selftest` validates the map).

At a glance:

| MIDI | → | WLED |
|---|---|---|
| Notes 59–68 · **looks** | | black + 7 hues + white + effect (mutually exclusive — what the lamp shows) |
| Notes 48–56 · **util** | | off / on / toggle / blackout / restore / solid |
| Notes 72–75 · **modifiers** | | beat toggle, flash — *overlay* the current look |
| CC 1 | | brightness (`bri`) |
| CC 3 + 4 | | continuous hue + saturation |
| CC 5/6/7/8 | | effect / speed / intensity / palette |
| Velocity *(optional)* | | look brightness |
| Program Change *n* | | preset `ps = n+1` |
| MIDI Clock (or session clock) | | on-the-beat pulse, phase-accurate downbeat |
| MIDI channel | | target device / segment / group (max 16 per port) |

## Implementations

| Project | Role |
|---|---|
| [openlamp/engine](https://github.com/openlamp/engine) | **reference implementation** — receives this convention, drives WLED + Tuya (`midi.py`) |
| [openlamp/wled-midi-web](https://github.com/openlamp/wled-midi-web) | **browser reference impl** — a single HTML file: Web MIDI → WLED JSON (all 3 modes: `lamp` + `strip` + `mpe`), zero install (upload to the WLED filesystem) |
| [openlamp/bome](https://github.com/openlamp/bome) | **Bome MIDI Translator pack** — map *any* hardware controller onto this convention, no code (generic template + capture) |
| [openlamp/matrix](https://github.com/openlamp/matrix) | **multi-device canvas router** — compose N WLED into one surface from MIDI: `mirror` (HTTP broadcast) + `unified` (per-device slice via realtime DDP) |
| [openlamp/live](https://github.com/openlamp/live) | Ableton Live frontend — *emits* this convention from a Live set |

Building your own? Open a PR to add it here.

## Scripting LED sequences

You don't need a bespoke LED scripting language — any tool that can send MIDI can
script the lights through this convention. A great fit is the Elgato Stream Deck
**MIDI plugin `se.trevligaspel.midi`**, whose scripting DSL can emit notes/CC on cue:
write a sequence once, fire it from a key. We deliberately **don't reinvent** a
scripting layer for LEDs — we lean on that one.


## Documentation

Topic-segmented docs live in **[`docs/`](docs/README.md)** — protocol map (into [SPEC.md](SPEC.md)),
plus hardware guides: [piano-aligned LED strip](docs/hardware/piano-strip.md) and
[WLED lamp(s)](docs/hardware/lamp.md).

## Credits & prior art

wled-midi is really a *write-down* of needs and ideas the WLED community has been voicing for
years. It's shaped by — and owes thanks to — the discussions and projects below. None are
affiliated with it and none have endorsed it; they're credited for the **ideas**. Building on
this, or want a credit added/changed/removed? Open a PR or an issue.

**WLED forum threads** (the needs behind the modes):

- [Control WLED LED Strip via MIDI keyboard](https://wled.discourse.group/t/control-wled-led-strip-via-midi-keyboard/15448) — *theTiPE* — playing a strip like an instrument → the `strip` mode.
- [MIDI live performance usermod](https://wled.discourse.group/t/midi-live-performance-usermod/14472) / [mode](https://wled.discourse.group/t/midi-live-performance-mode/14459) — *frankofino* — "a full MIDI mapping on most controls" → the `lamp` mode.
- [External WLED Controller for club use case](https://wled.discourse.group/t/external-wled-controller-for-club-use-case/11887) — *faltim* — the multi-device **matrix / canvas** (Extensions §8).
- [MIDI with WLED (miledy), e.g. Ableton Push2](https://wled.discourse.group/t/midi-with-wled-miledy-eg-abledon-push2/10539) — *MikeFormerShibumi* — pads → looks.
- [Progress preset in playlist with MIDI/pc](https://wled.discourse.group/t/progress-preset-in-playlist-with-midi-or-pc-key/8065) — *Mauri* — Program Change → preset.
- [Simple DMX/MIDI control for venue](https://wled.discourse.group/t/simple-dmx-midi-control-for-venue/12068) — *zumdar* — brightness on a controller.
- [WLED + MIDI Player?](https://wled.discourse.group/t/wled-midi-player/4536) — *wombat* — the earliest "can I?" (2021).

**Projects & tutorials** (prior art for the `strip` / piano-guide space):

- [tim-peters/WLED-Midi-Keyboard](https://github.com/tim-peters/WLED-Midi-Keyboard) — single-HTML-on-device MIDI keyboard; its zero-install deployment is the ideal we're aiming a `strip` implementation at.
- [onlaj/Piano-LED-Visualizer](https://github.com/onlaj/Piano-LED-Visualizer) — the reference Raspberry-Pi + WS2812 piano visualizer (learning / Synthesia).
- [MusicalBasics — How To Make Your Own LED Piano](https://www.youtube.com/watch?v=B-lzFz1RM4E) — a full build that drives the LEDs from Ableton.
- Synthesia LED guides and the various *Instructables* piano-LED tutorials.

**Kindred products** (the same instinct, done as closed hardware): DAW-driven recording lamps like the [Punchlight Recording Lamp USB RGB](https://www.thomannmusic.com/punchlight_recording_lamp_usb_rgb.htm) — which turns a light red / green straight from your DAW's record state — show the appetite for *DAW → light*. wled-midi is the open, WLED version of exactly that: a record-arm note/CC → a lamp goes red.

**Expressive controllers & MPE sources** (what the `strip` / `mpe` modes are made for): [ROLI Seaboard](https://roli.com) (the flagship MPE controller — also switches single-channel MIDI ↔ MPE, which inspired the unified channel/zone design), [Expressive E Touché](https://www.expressivee.com), the [TEControl USB-MIDI Breath Controller (BBC2)](https://www.tecontrol.se) (breath + bite expression), [Beatbars](https://www.beatbars.com) (MIDI expression pedals/bars for organists), and MPE-capable instruments like [Spectrasonics Omnisphere](https://www.spectrasonics.net/products/omnisphere/).

**Tools that pair well** (ways to *emit* the convention):

- [**Trevliga Spel — Stream Deck MIDI plugin**](https://trevligaspel.se/streamdeck/midi/index.php) ([Elgato Marketplace](https://marketplace.elgato.com/product/midi-b068a591-1a69-48fe-9206-b2d24762228b)) — a rock-solid Stream Deck MIDI plugin (Windows/macOS, MIDI 1.0) with a genuinely great **scripting DSL**. A daily-driver for controlling MIDI gear, and one of the easiest ways to fire wled-midi notes/CC from hardware **on cue, with no code** (see [Scripting LED sequences](#scripting-led-sequences)).

- [**Bome MIDI Translator Pro**](https://www.bome.com/products/miditranslator) — a general-purpose MIDI mapper / router / scripter, and the **universal adapter**: translate *any* input (a controller sending the "wrong" notes/CC, keystrokes, timers, DAW MIDI) into wled-midi, **and integrate the MIDI flows between devices** — merge, split and route between hardware, virtual ports and DAWs. Also a natural home for value-level **return-feedback** logic.

**Tooling to build & test an implementation:**

- *Cross-platform* — [**ShowMIDI**](https://github.com/gbevin/ShowMIDI) (Geert Bevin): a free, open-source MIDI **visualizer** — the fastest way to *see* exactly which notes/CC are flowing.
- *macOS* — virtual MIDI ports via the built-in **IAC Driver** (Audio MIDI Setup, no install); [**MIDI Friend**](https://apps.apple.com/us/app/midi-friend/id497641137?mt=12) (Douglas Heriot): **generate** test notes/CC with no hardware controller.
- *Windows* — [**loopMIDI**](https://www.tobias-erichsen.de/software/loopmidi.html) (Tobias Erichsen): create the virtual MIDI ports the convention routes through (monitor with ShowMIDI, generate/route with Bome). For MIDI over the network, [**rtpMIDI**](https://www.tobias-erichsen.de/software/rtpmidi.html) (same author — RTP-MIDI / AppleMIDI).

**Platform**: [WLED](https://kno.wled.ge) itself — Aircoookie and the WLED community — which this convention merely speaks to over its public local API.

## License

[MIT](LICENSE) — implement it freely, no copyleft. A convention is only useful if
anyone can adopt it.
