# Quick reference — WLED in 60 seconds + the MIDI map at a glance

A one-page primer for anyone new to this convention — including tool builders (e.g. the
[Bome MIDI Translator](https://www.bome.com/products/miditranslator) team) who want to grasp
*what WLED is* and *which MIDI message means what* without reading the full
[SPEC](../SPEC.md) first. Read this, then dive into the SPEC for the normative detail.

---

## What is WLED? (the 60-second version)

[**WLED**](https://kno.wled.ge) is open-source firmware for **addressable LED** strips and
bulbs (running on ESP32/ESP8266 boards). Once flashed, a WLED device joins your Wi-Fi and
exposes a **local HTTP JSON API** — you control it by POSTing a small JSON "state" object to
`http://<device-ip>/json/state`. No cloud, 100 % local.

This convention is just an agreed **MIDI → that JSON** mapping. Every Core mapping resolves to
one documented WLED JSON key — so it works against a **stock WLED device, no extra software**.

### The handful of WLED words you need

| WLED term | JSON key | What it is |
|---|---|---|
| **Device** | *(the IP/host)* | one WLED unit (a strip or bulb) |
| **Segment** | `seg[]` | a slice of a strip you can address independently |
| **On / off** | `on` | power (`true` / `false` / `"t"` toggle) |
| **Brightness** | `bri` | master brightness, **0–255** |
| **Colour** | `seg[].col` | an RGB triplet, e.g. `[255,0,0]` = red |
| **White temp** | `seg[].cct` | warm ↔ cool white, 0–255 |
| **Effect** | `seg[].fx` | which built-in **animation** plays (0 = solid) |
| **Effect speed / intensity** | `seg[].sx` / `seg[].ix` | how the animation moves, 0–255 |
| **Palette** | `seg[].pal` | the colour set an effect draws from |
| **Preset** | `ps` | a **saved state** you recall by number (1–250) |

That's the whole vocabulary. The MIDI map below is nothing more than "which MIDI message
sets which of these keys".

---

## The MIDI → WLED map at a glance

**One rule to orient you:** **MIDI channel 1 = plain MIDI, controls the lights; a note-on
picks a look or fires an action; a CC sets a continuous parameter; a Program Change recalls a
preset.** Actions fire on **note-on only** (note-off is ignored). All numbers are remappable;
the *transforms* (how a value becomes a WLED number) are the stable contract.

### Notes → looks & actions  *(note-on, velocity ignored by default)*

| Note | Name | Does | WLED result |
|---|---|---|---|
| **59** | black | look | colour `[0,0,0]` (+ `fx:0`) |
| **60** | red | look | colour `[255,0,0]` |
| **61** | orange | look | colour `[255,85,0]` |
| **62** | yellow | look | colour `[255,200,0]` |
| **63** | green | look | colour `[0,255,0]` |
| **64** | cyan | look | colour `[0,200,255]` |
| **65** | blue | look | colour `[0,0,255]` |
| **66** | magenta | look | colour `[255,0,170]` |
| **67** | white | look | colour `[255,255,255]` |
| **68** | effect | look | turn on the effect animation (`fx`/`sx`/`ix` from CC 5/6/7) |
| **48** | off | util | `{"on":false}` |
| **50** | on | util | `{"on":true}` |
| **52** | toggle | util | `{"on":"t"}` |
| **53** | blackout | util | `{"bri":0}` |
| **55** | restore | util | brightness back to last value |
| **56** | solid | util | exit the effect, back to solid colour (`fx:0`) |
| **72** | beat | modifier | toggle: pulse the current look on the beat (needs tempo) |
| **73** | flash | modifier | momentary bright flash, then back |

*Looks (59–68) are **mutually exclusive** — one is "what the lamp shows". Modifiers (72–73)
**overlay** the current look (so you get colour + beat, effect + flash, …).*

### Control Change → continuous parameters

| CC | Sets | WLED key | Transform (`v` = 0–127) |
|---|---|---|---|
| **1** | brightness | `bri` | `round(v/127 × 255)` |
| **2** | white temp | `cct` | `round(v/127 × 255)` |
| **3** | hue | `col` (via HSV) | `hue = v/127` |
| **4** | saturation | `col` (via HSV) | `sat = v/127` |
| **5** | effect | `fx` | `round(v/127 × (fxCount−1))` |
| **6** | effect speed | `sx` | `round(v/127 × 255)` |
| **7** | effect intensity | `ix` | `round(v/127 × 255)` |
| **8** | palette | `pal` | `round(v/127 × (palCount−1))` |

### Program Change, tempo & channel

| MIDI | → | WLED |
|---|---|---|
| **Program Change** *n* | | recall preset `ps = n + 1` (MIDI program 0 → preset 1) |
| **MIDI Clock** (`F8`, 24 ticks/beat) or a session clock (e.g. Ableton Link) | | put pulses / effect speed **on the beat** |
| **MIDI channel** | | which target: `1` = the device / all segments; `2–16` = a segment/group (routing is the implementer's config) |

> **Modes.** The table above is the default **`lamp`** mode (note = a look/action). Two other
> modes reuse the *same* spine but reinterpret the channel/note layout: **`strip`** (note pitch
> → a LED position, e.g. a piano-guide) and **`mpe`** (channel = a per-note expressive voice).
> See [SPEC §12–13](../SPEC.md). If all you need is "control the lights", you only need `lamp`
> on channel 1.

---

## Reading this from the Bome side

[Bome MIDI Translator Pro](https://www.bome.com/products/miditranslator) (an independent
product — not affiliated with this project) is a natural fit as a **general-purpose adapter**:
it takes whatever MIDI a controller sends and **re-labels it** into the messages above, then
routes it to the virtual port a wled-midi implementation listens on. The only thing to *emit*
is the raw MIDI on the outgoing side — here it is in hex (channel 1 = all lamps; change the
channel nibble to target a group):

| Action | Outgoing MIDI (hex) |
|---|---|
| **Looks** black → effect (notes 59–68) | `90 3B 7F` … `90 44 7F` |
| **Util** off/on/toggle/blackout/restore/solid | `90 30 7F` · `90 32 7F` · `90 34 7F` · `90 35 7F` · `90 37 7F` · `90 38 7F` |
| **Modifiers** beat / flash (notes 72/73) | `90 48 7F` / `90 49 7F` |
| **CC** bri/cct/hue/sat/fx/sx/ix/pal (CC 1–8) | `B0 01 pp` … `B0 08 pp` (`pp` = value pass-through) |
| **Program Change** → preset | `C0 pp` |

A no-code translator pack (one translator per action, capture-your-controller on the incoming
side) is available at **[openlamp/bome](https://github.com/openlamp/bome)** — paste the
[`wled-midi.generic.txt`](https://github.com/openlamp/bome/blob/main/wled-midi.generic.txt)
blocks into a Bome preset and capture your buttons. The same tool can also carry
**return-feedback** logic (WLED state → light up the controller's own LEDs).

---

## Go deeper

- **[SPEC.md](../SPEC.md)** — the normative spec (all modes, transforms, extensions).
- **[mapping.spec.json](../mapping.spec.json)** — the same map, machine-readable.
- **[resolve.py](../resolve.py)** — paste in a MIDI event, see the exact WLED JSON it means
  (`python3 resolve.py cc 1 100` → `{"bri":201}`).
- **[docs/README.md](README.md)** — the full documentation index (protocol, hardware guides).
