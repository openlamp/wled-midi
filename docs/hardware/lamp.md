# WLED lamp(s) — hardware guide

The simplest rig: one or more WLED lamps as stage/room lighting, driven over MIDI through the
default [`lamp` mode](../../SPEC.md) (channel = lamp, note = look/action, CC = params).

## Options

- **Pre-flashed WLED bulb (easiest)** — an [Athom 7–12 W RGBCW E27, pre-flashed with WLED](https://kno.wled.ge)
  (ESP32-C3, ~€13). RGB + a dedicated white channel + tunable warm↔cool. Screw it in, join Wi-Fi,
  done. This is the reference lamp (measured ~45 ms/command end-to-end).
- **DIY** — an [ESP32](https://www.az-delivery.de/) + any WS2812B / SK6812 strip or a bulb board,
  flashed with [WLED](https://kno.wled.ge).

## Setup

1. Flash / power the lamp with WLED; join it to your Wi-Fi.
2. Reserve its IP on the router (so it's stable).
3. In your `lamp`-mode implementation, map a MIDI **channel → this lamp's IP**. Adding a second
   lamp = a second channel (or, past 16 lamps, the *1 note = 1 lamp* variant — see the SPEC).
4. Drive it: notes → colour looks / power, CC → brightness / hue / effect (see [`lamp` mode](../../SPEC.md)).

## Notes

- WLED speaks a plain local **HTTP JSON API** — no cloud, no pairing.
- For per-beat pulsing at speed, batch changes per window or use WLED realtime UDP (see the SPEC, §7).
