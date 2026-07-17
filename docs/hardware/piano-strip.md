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
