# Piano-aligned LED strip (WLED) — hardware guide

A dense addressable strip stuck along a piano keyboard that **lights the LED(s) in front of
each key** — a piano-guide (learn/Synthesia) and/or a stage backdrop. Driven over MIDI through
the [`strip` mode](../../SPEC.md) (`keymap` position function).

## The key insight — density, not physical 1-LED-per-key

**There is no bare LED strip with a "physical" asymmetric one-diode-per-key layout.** Every
system — including product listings that imply it (e.g. the Etsy *i-Piano*) — actually uses a
**high-density strip (~144 LED/m)** in a black profile, plus a **software/firmware mapping**
that lights the LED zone in front of each key. With an opaque diffuser the illusion is perfect.
This is how ~99% of DIY piano-LED builds work in 2026.

→ The viable, reliable, **WLED-compatible** method is *density + mapping*:

1. **WS2812B 144 LED/m** strip (black PCB for discretion).
2. Aluminium/plastic black profile + **opaque diffuser** (hides individual points → a continuous line).
3. **WLED on an ESP32**.
4. A **note → LED mapping** (either a host like Piano-LED-Visualizer, or the mapping baked into
   the WLED firmware/usermod — see [Calibration](#calibration)).

Closed / pricey aligned systems exist (**Piano LED Plus**, **Symphone**); the open route above
is cheaper and WLED-native.

## LED spacing for a full-size 88-key piano (the market standard)

Weighted-key (hammer-action / *toucher lourd*) digital pianos are, **with rare exceptions, 88 keys** —
full-size keys, A0 → C8 (MIDI 21 → 108). Designing the strip for **88 full-size keys** therefore
covers essentially the whole weighted-piano market; the odd 73/76-key stage piano is the exception,
not the rule.

The physical span to cover:

| Measure | Value |
|---|---|
| Playing width (A0 → C8) | **≈ 1225 mm** (~48.2") |
| White keys | 52 · white-key pitch ≈ **23.5 mm** (an octave of 7 whites ≈ 165 mm) |
| Average note-to-note pitch | ≈ **13.75 mm** (12 semitones per 165 mm octave) |

Keys are **not uniformly spaced** (whites are wide, blacks sit offset between them), so a uniform-pitch
strip can't put exactly one diode on every key centre. The fix is **density**: pick ~2 LEDs per key so
the mapping can always centre on the played key and absorb the white/black offset in software.

| Strip density | LED pitch | LEDs over 1225 mm | LEDs / key | Verdict |
|---|---|---|---|---|
| **144 LED/m** | 6.9 mm | **≈ 176** | **≈ 2.0** | ✅ the de-facto piano choice — fine enough to align cleanly |
| 96 LED/m | 10.4 mm | ≈ 118 | ≈ 1.35 | workable, coarser |
| 72 LED/m | 13.9 mm | ≈ 88 | ≈ 1.0 | tempting (1 LED/note) but **no margin** — alignment drifts across the board, fragile |
| 60 LED/m | 16.7 mm | ≈ 73 | < 1 | too coarse |

→ **144 LED/m, ≈ 176 LEDs, LED 0 centred on A0** — i.e. `lpk ≈ 2.0`, `firstnote = 21` in the
[calibration formula](#the-formula-what-keymap-uses). The **proprietary aligned systems**
(Piano LED Plus, Symphone, i-Piano…) reach their clean, key-perfect look the same way — a dense
strip + an opaque diffuser + a careful per-key mapping. That alignment is **genuinely good
engineering**; the open route here matches it with a WLED-native strip and the mapping in firmware.

## Producing a purpose-built strip (industrial or artisanal)

The 144 LED/m + firmware-mapping route above is what an **artisanal / DIY** build uses — an
off-the-shelf reel, a black diffuser channel, and the `keymap` calibration (measure the span, set
`lpk` + `firstnote`). Cheap, reliable, no tooling. If you want to **manufacture** a dedicated strip,
there are two levels:

**A — uniform dense strip + firmware mapping (low tooling).** Ship a standard high-density reel
(**144 LED/m**, ~176 LEDs for the 88-key span) in a black anodised channel with an opaque diffuser,
and bake the note→LED map into the firmware. Off-the-shelf LEDs, **no custom PCB**; the non-uniform
key layout is absorbed in software. This is how most aligned products actually reach their look, and
it stays flexible (recalibrates to any keyboard size).

**B — custom-pitch PCB (pixel-perfect 1:1, real tooling).** Design a flexible PCB that places the
LEDs **at the measured key-centre positions** rather than at a uniform pitch — the only way to sit
one diode exactly over each key centre with *no* software mapping. The geometry to encode:

- 88 notes over **≈ 1225 mm**, A0 → C8, centres **not evenly spaced**: 52 white centres at ≈ 23.5 mm
  pitch, plus 5 black centres per octave offset into the gaps (C♯/D♯ between C-D-E; F♯/G♯/A♯ between
  F-G-A-B).
- **1 LED per note at its centre** (88 LEDs) for a point-guide, or **2–3 LEDs per key footprint**
  (~176–264 LEDs) for a lit-bar-per-key look — whites getting a wider LED group than blacks.
- Keep the data protocol **WLED-native** (WS2812 / SK6812) so a stock ESP32 + WLED drives it: the
  strip is bespoke, the brain and protocol stay open.

Trade-off: **A** is cheap and universal (any keyboard, calibrate in software); **B** is perfect out
of the box but costs PCB tooling and locks the geometry to one layout. For the standard 88-key
weighted-piano market, **B** is worth it; for reach across keyboard sizes, **A** wins.

### Prior art & patents (informational — not legal advice)

The "light the key to play" idea has **decades of prior art**: illuminated-key guidance patents go
back to the late 1990s — e.g. [US 6,037,534](https://patents.google.com/patent/US6037534),
[US 6,008,783](https://patents.google.com/patent/US6008783) and
[US 6,407,324](https://patents.google.com/patent/US6407324) (the last covers *two colours for
left/right hand*) — most now past their 20-year term, plus a large body of open work
([onlaj/Piano-LED-Visualizer](https://github.com/onlaj/Piano-LED-Visualizer) is MIT) and countless
DIY builds. The general concept isn't something one could newly monopolise. **Live, specific patents
do exist** on *particular* systems, though — e.g. [US 11,087,636](https://patents.google.com/patent/US11087636)
(2021: an enclosure over the keys + per-key lights + laser sensors synced to lessons/games) and
[US 9,652,994](https://patents.google.com/patent/US9652994) (LED bars in 1:1 key correspondence,
MIDI-file-driven) — claiming specific mechanisms, not the generic dense-strip + note→LED mapping.
**Takeaway:** the open density-plus-mapping approach on generic components rests on broad, long-standing
prior art; but patents are jurisdictional and claim-specific, so **anyone selling a product should get
a proper freedom-to-operate opinion from a patent attorney**. This note is informational only.

## Bill of materials (for two strips — one for the audience, one for the player)

| Part | Example | ~Price |
|---|---|---|
| 5V PSU | [BTF-LIGHTING 5V 10A 50W (CE)](https://www.amazon.fr/dp/B01AS0ELDA) | €50.99 |
| Strip connectors + extension | RUNCCI-YUN 3-pin 10 mm connector kit (×10) + 5 m cable | €10.99 |
| ESP32 | [AZDelivery ESP32 D1 Mini NodeMCU USB-C (×3)](https://www.az-delivery.de/) | €28.34 |
| LED strip | [BTF-LIGHTING WS2812B **144 LED/m** 1 m, black PCB IP30](https://www.amazon.fr/BTF-LIGHTING-flexible-individuellement-adressable-non-%C3%A9tanche/dp/B01CDTEJR0/) | €24.99 |

*(Prices indicative. One ESP32 + one strip + wiring per bar; the 3-pack ESP32 and the PSU cover both.)*

## Calibration (note → LED)

The convention sends **a note**; the implementation decides **which LED(s)** to light. Put that
intelligence in the firmware/host so any dense strip becomes MIDI-compatible:

- **LEDs-per-key** derived from *LEDs-per-octave* + an offset (which note is LED 0), **or**
- the user **measures** the keyboard width + white-key count and the firmware computes the map.

### The formula (what `keymap` uses)

Two numbers calibrate a whole strip — no per-key table needed:

```
lpk       = strip_LED_count / number_of_keys_the_strip_covers   (LEDs per key)
firstnote = the MIDI note sitting at LED 0 (e.g. 21 = piano A0, 36 = a 61-key C)
led(note) = round((note − firstnote) × lpk)                     (light led(note) … +ceil(lpk))
```

Examples: a **144 LED/m** strip over an **88-key** piano (~1.23 m ≈ 176 LEDs) → `lpk ≈ 176/88 = 2.0`,
`firstnote = 21`. A **61-key** (C2–C7) controller with a 100-LED strip → `lpk ≈ 100/61 ≈ 1.6`,
`firstnote = 36`. These are exactly the `strip.lpk` / `strip.firstnote` config keys in the
[engine](https://github.com/openlamp/engine) and [wled-midi-web](https://github.com/openlamp/wled-midi-web).

Each key lights ~2–3 LEDs (density > keys). Velocity → brightness, note-off → fade (see
[`strip` mode](../../SPEC.md)).

## References

- [onlaj/Piano-LED-Visualizer](https://github.com/onlaj/Piano-LED-Visualizer) — the reference open-source note→LED mapper (Raspberry Pi + WS2812; learning/Synthesia). The algorithm to fold into `strip`/`keymap`.
- [MusicalBasics — How To Make Your Own LED Piano](https://www.youtube.com/watch?v=B-lzFz1RM4E) — a full build (drives the LEDs from Ableton).
- Reddit — [Is there any RGB-LED bar to connect to MIDI?](https://www.reddit.com/r/piano/comments/q596ln/is_there_any_rgbled_bar_to_connect_to_midi/)
- Reddit — [Ultimate Guide to DIY LED Visualizer for your piano](https://www.reddit.com/r/piano/comments/q7rk9h/ultimate_guide_to_diy_led_visualizer_for_your/)
- YouTube — [DIY piano LED demo](https://youtu.be/31xEZO2boNs)
- Etsy — [i-Piano LED visualizer](https://www.etsy.com/fr/listing/1339576021/visualiseur-led-i-piano-o-autodidacte-o) (an example of "density disguised as 1-LED-per-key")
- Amazon — [BTF-LIGHTING WS2812B strip](https://www.amazon.fr/BTF-LIGHTING-flexible-individuellement-adressable-non-%C3%A9tanche/dp/B01CDTEJR0/)
