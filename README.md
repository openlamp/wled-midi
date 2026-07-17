# wled-midi

> **An open convention for controlling [WLED](https://kno.wled.ge) lights over MIDI.**
> Drive WLED from any DAW, sequencer or hardware MIDI controller — in time with your
> music. Notes → colours, CC → brightness/effects, Program Change → presets, MIDI
> Clock (or a session clock) → on-the-beat. 100 % local.

This repo is **just the specification** — no runtime, no dependencies. It exists so
that multiple tools can speak the same MIDI↔WLED language instead of each inventing
its own.

> 🚧 **Status — a project just getting started, built in the open.** wled-midi is young and
> **structuring itself progressively**: the convention is still a **draft** (see [SPEC.md](SPEC.md))
> and squarely in a **build phase**. It's meant to be **co-constructed** — shaped together with
> anyone who wants to take part (WLED users, tool makers, controller and firmware authors).
> **As a result, its structure is likely to change — and, early on, to change quickly** before it
> settles. Expect it to move and sharpen over time; ideas, corrections and contributions are
> welcome via an [issue](https://github.com/openlamp/wled-midi/issues) or a PR.

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
| [openlamp/matrix](https://github.com/openlamp/matrix) | **multi-device canvas router** — compose N WLED into one surface from MIDI: `mirror` (HTTP broadcast) + `unified` (per-device slice via realtime **DDP / Art-Net / E1.31**, incl. a 2-D serpentine canvas) |
| [openlamp/live](https://github.com/openlamp/live) | Ableton Live frontend — *emits* this convention from a Live set |
| [Beennnn/zone-m4l](https://github.com/Beennnn/zone-m4l) | **Max for Live** keyboard-split device — *emits* the `strip` / `zone` mode: each instrument's key range lit as a coloured band on the strip, moving live with the split |
| [openlamp/prism](https://github.com/openlamp/prism) | **Max for Live** colour-zones device — *emits* the `lamp` mode: split the keyboard into colour zones, play a note → the lamp takes that zone's colour, velocity → brightness |

Building your own? Open a PR to add it here.

## Scripting LED sequences

You don't need a bespoke LED scripting language — any tool that can send MIDI can
script the lights through this convention. A great fit is the Elgato Stream Deck
**MIDI plugin `se.trevligaspel.midi`**, whose scripting DSL can emit notes/CC on cue:
write a sequence once, fire it from a key. We deliberately **don't reinvent** a
scripting layer for LEDs — we lean on that one.


## Documentation

New here? The **[Quick reference](docs/quick-reference.md)** explains WLED in 60 seconds and
puts the whole MIDI map on one page — a fast on-ramp for tool builders (e.g. Bome).

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

**Projects & tutorials** (prior art for the `strip` space):

- [tim-peters/WLED-Midi-Keyboard](https://github.com/tim-peters/WLED-Midi-Keyboard) — a single-HTML-on-device MIDI keyboard: play a strip like an instrument. Its zero-install deployment is the ideal we aim a `strip` implementation at.

### Piano-learning tools — and why we build an open protocol alongside them

A whole family of projects and products *light the keys to teach you to play*. Some are polished
learning tools with a real business model behind them — and staying viable can reasonably mean
relying on a **proprietary or closed protocol**. That work is genuine and **we respect it**: several
deliver beautifully **key-aligned strips on standard keyboards** (real engineering — see the
[88-key spacing guide](docs/hardware/piano-strip.md)), and making something people love and can
sustain is hard, so a closed interface is a legitimate way to protect it.

- [onlaj/Piano-LED-Visualizer](https://github.com/onlaj/Piano-LED-Visualizer) — the reference open-source RPi + WS2812 piano visualiser (learning / Synthesia).
- [serifpersia/pianolux-esp32](https://github.com/serifpersia/pianolux-esp32) & [pianolux-arduino](https://github.com/serifpersia/pianolux-arduino) — piano-LED from USB / BLE / WiFi MIDI on cheap ESP hardware.
- [MusicalBasics — How To Make Your Own LED Piano](https://www.youtube.com/watch?v=B-lzFz1RM4E) — a full build that drives the LEDs from Ableton.
- [Piano Led](https://www.facebook.com/pianoled/reels/) (Lille, FR) — a piano-LED visualiser shown in short video reels: the strip lights the notes as you play.
- Synthesia LED guides and the various *Instructables* piano-LED tutorials.

wled-midi runs **in parallel**, with a complementary aim: an **open, standardised, collaborative**
convention, so that any tool — a learning app, a DIY strip, a stage rig, a hardware controller —
can speak the same MIDI↔WLED language and interoperate. We're not here to displace anyone, and
we'll do our best that **each finds its place**: where a product's model needs a closed protocol,
that stays theirs; where a use is more community-minded — education, DIY, sharing, freely mixing
tools — **open interoperability has a great deal to offer**, because it's what lets solutions become
usable by *everyone*, not only inside one vendor's walls.

That is the project's guiding line: **advanced, integrated solutions that anyone can use, across
varied contexts** — from a beginner's first lit key to a full live show — kept open so the whole
community can build on them, together.

**Software that already drives WLED** (the neighbourhood wled-midi joins — these mostly stream
*pixels* over WLED's realtime UDP: DDP / Art-Net / E1.31. wled-midi is the **MIDI-native, per-message**
member of the family: one MIDI event → one WLED action, live, rather than a pre-rendered pixel feed):

- [**xLights**](https://xlights.org) (Win/Mac/Linux) — the big open-source **LED sequencer** + show scheduler; drives WLED over DDP/Art-Net/E1.31. Timeline-authored shows, not live MIDI.
- [**LedFx**](https://github.com/LedFx/LedFx) (Win/Mac/Linux) — **audio-reactive** LED visualiser → WLED via DDP/E1.31; its DDP sender is the reference the [matrix](https://github.com/openlamp/matrix) router's transport models.
- [**QLC+**](https://www.qlcplus.org) (Win/Mac/Linux/RPi) — free **DMX / lighting control** that takes **MIDI in** and outputs Art-Net/E1.31 → WLED. The closest "MIDI → lights" cousin, but DMX-channel-oriented rather than a note/CC convention.
- [**Chataigne**](https://github.com/benkuper/Chataigne) (Win/Mac/Linux) — Ben Kuper's modular **glue** (MIDI/OSC/DMX/Art-Net/sACN); a natural host to *implement* wled-midi as a bridge.
- [**Hyperion.ng**](https://github.com/hyperion-project/hyperion.ng) (Win/Mac/Linux) — ambient/bias lighting → WLED. And WLED's own canonical list: [compatible software](https://kno.wled.ge/basics/compatible-software/).

**Apps & products built on WLED** (finished tools you can just use):

- [**LumiDeck**](https://github.com/openlamp/lumideck-support) — a **Stream Deck** app that drives your WLED lamps & strips locally from physical keys: colour, brightness, effects/palettes by name, scenes, and beat-sync (~45 ms/press). From the OpenLamp author, built on the [engine](https://github.com/openlamp/engine); WLED-first.
- [**OpenLamp Beat**](https://github.com/openlamp/ha-addon-beat) — a **Home Assistant** add-on that flashes your WLED lamps **on the beat** of an Ableton Link / MIDI-clock session (runs the [engine](https://github.com/openlamp/engine) + beatsync, exposes `switch.beat_sync` via MQTT discovery). Install-from-URL, no Docker knowledge needed.

**Kindred products** (the same instinct, done as closed hardware): DAW-driven recording lamps like the [Punchlight Recording Lamp USB RGB](https://www.thomannmusic.com/punchlight_recording_lamp_usb_rgb.htm) — which turns a light red / green straight from your DAW's record state — show the appetite for *DAW → light*. wled-midi is the open, WLED version of exactly that: a record-arm note/CC → a lamp goes red.

**Expressive controllers & MPE sources** (what the `strip` / `mpe` modes are made for): [ROLI Seaboard](https://roli.com) (the flagship MPE controller — also switches single-channel MIDI ↔ MPE, which inspired the unified channel/zone design), [Expressive E Touché](https://www.expressivee.com), the [TEControl USB-MIDI Breath Controller (BBC2)](https://www.tecontrol.se) (breath + bite expression), [Beatbars](https://www.beatbars.com) (MIDI expression pedals/bars for organists), and MPE-capable instruments like [Spectrasonics Omnisphere](https://www.spectrasonics.net/products/omnisphere/).

**Tools that pair well** (ways to *emit* the convention):

- [**Trevliga Spel — Stream Deck MIDI plugin**](https://trevligaspel.se/streamdeck/midi/index.php) ([Elgato Marketplace](https://marketplace.elgato.com/product/midi-b068a591-1a69-48fe-9206-b2d24762228b)) — a rock-solid Stream Deck MIDI plugin (Windows/macOS, MIDI 1.0) with a genuinely great **scripting DSL**. A daily-driver for controlling MIDI gear, and one of the easiest ways to fire wled-midi notes/CC from hardware **on cue, with no code** (see [Scripting LED sequences](#scripting-led-sequences)).

- [**Bome MIDI Translator Pro**](https://www.bome.com/products/miditranslator) — a general-purpose MIDI mapper / router / scripter, and the **universal adapter**: translate *any* input (a controller sending the "wrong" notes/CC, keystrokes, timers, DAW MIDI) into wled-midi, **and integrate the MIDI flows between devices** — merge, split and route between hardware, virtual ports and DAWs. Also a natural home for value-level **return-feedback** logic. No-code **[starter pack → openlamp/bome](https://github.com/openlamp/bome)** (paste-in translators + a WLED primer from Bome's point of view).

**Tooling to build & test an implementation:**

- *Cross-platform* — [**ShowMIDI**](https://github.com/gbevin/ShowMIDI) (Geert Bevin): a free, open-source MIDI **visualizer** — the fastest way to *see* exactly which notes/CC are flowing. Also [**Protokol**](https://hexler.net/protokol) (Hexler): a free MIDI/OSC/gamepad **monitor** (Win/Mac/Linux/iOS).
- *macOS* — virtual MIDI ports via the built-in **IAC Driver** (Audio MIDI Setup, no install); [**MIDI Friend**](https://apps.apple.com/us/app/midi-friend/id497641137?mt=12) (Douglas Heriot): **generate** test notes/CC with no hardware controller.
- *Windows* — [**loopMIDI**](https://www.tobias-erichsen.de/software/loopmidi.html) (Tobias Erichsen): create the virtual MIDI ports the convention routes through (monitor with ShowMIDI, generate/route with Bome). For MIDI over the network, [**rtpMIDI**](https://www.tobias-erichsen.de/software/rtpmidi.html) (same author — RTP-MIDI / AppleMIDI). The classic [**MIDI-OX**](http://www.midiox.com) monitors + routes MIDI.
- *Linux* — virtual ports via the ALSA **`snd-virmidi`** kernel module (or JACK / PipeWire); **`aseqdump -l`** lists ports and **`aseqdump -p <port>`** monitors them; **[a2jmidid](https://github.com/jackaudio/a2jmidid)** bridges ALSA ↔ JACK for routing into DAWs (Bitwig, Reaper).

**The two open standards this bridges** — wled-midi stands equally on both pillars, and owes each its thanks:

- **MIDI** — the universal music-control standard stewarded by the [MIDI Association](https://midi.org). The Core is plain **MIDI 1.0**; the `mpe` and `strip` modes build directly on **MPE** (MIDI Polyphonic Expression — per-note pitch / pressure / slide), and the forward-compat profile follows **[MIDI 2.0](https://midi.org/midi-2-0)** (high-resolution control). Everything wled-midi *reads* is ordinary MIDI — nothing proprietary on the input side.
- **WLED** — [WLED](https://kno.wled.ge) (Aircoookie and the WLED community), whose public local **JSON-state + realtime-UDP** API every mapping *resolves to* — nothing proprietary on the output side either.

wled-midi is just the agreed **dictionary between these two open standards**: MIDI in, WLED out.

## License

[MIT](LICENSE) — implement it freely, no copyleft. A convention is only useful if
anyone can adopt it.
