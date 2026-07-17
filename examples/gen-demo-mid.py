#!/usr/bin/env python3
"""Generate a wled-midi demo MIDI clip (`wled-midi-demo.mid`).

A Standard MIDI File that *emits the wled-midi convention* — drop it on a MIDI track in any DAW
(Ableton Live, Logic, Reaper, Bitwig…) and route that track's MIDI OUT to your wled-midi port
(the engine's `OpenLamp` virtual port). It plays a short showcase: colour looks, a brightness
fade (CC 1), a hue sweep (CC 3), a flash, and a blackout/restore.

Why a `.mid` and not a `.als`: a MIDI file is a stable, DAW-agnostic format that works everywhere,
whereas an Ableton `.als` is a version-specific gzipped-XML session that breaks easily. Drag this
`.mid` into a Live MIDI track and you have the "Ableton demo" — in any DAW.

Run:  python3 examples/gen-demo-mid.py    (writes examples/wled-midi-demo.mid)
Pure stdlib.
"""
import os, struct

PPQ = 480          # ticks per quarter note
BEAT = PPQ


def vlq(n):
    """MIDI variable-length quantity."""
    out = bytearray([n & 0x7F])
    n >>= 7
    while n:
        out.insert(0, (n & 0x7F) | 0x80)
        n >>= 7
    return bytes(out)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    events = []          # (abs_tick, midi_bytes)

    def note(t, n, dur, vel=100, ch=0):
        events.append((t, bytes([0x90 | ch, n, vel])))
        events.append((t + dur, bytes([0x80 | ch, n, 0])))

    def cc(t, num, val, ch=0):
        events.append((t, bytes([0xB0 | ch, num, val])))

    # --- the showcase ---
    LOOKS = [(60, "red"), (63, "green"), (65, "blue"), (67, "white")]
    t = 0
    for n, _ in LOOKS:                         # 4 colour looks, one per beat
        note(t, n, BEAT // 2)
        t += BEAT

    # brightness fade up then down (CC 1) over 4 beats — smooth on a high-res-CC setup
    for i in range(33):
        cc(t + i * (4 * BEAT) // 32, 1, round(i / 32 * 127))
    t += 4 * BEAT
    for i in range(33):
        cc(t + i * (2 * BEAT) // 32, 1, round((1 - i / 32) * 127))
    t += 2 * BEAT

    # hue sweep (CC 3) across the spectrum, 4 beats
    note(t, 67, 8 * BEAT)                       # hold a white look so the hue CC colours it
    for i in range(65):
        cc(t + i * (4 * BEAT) // 64, 3, round(i / 64 * 127))
    t += 4 * BEAT

    note(t, 73, BEAT // 4)                      # flash (note 73)
    t += 2 * BEAT
    note(t, 53, BEAT // 4)                      # blackout (util 53)
    t += BEAT
    note(t, 55, BEAT // 4)                      # restore (util 55)
    t += 2 * BEAT

    # --- serialise to a format-0 track ---
    events.sort(key=lambda e: e[0])
    track = bytearray()
    track += b"\x00" + b"\xFF\x03\x0Ewled-midi demo"          # track name
    track += b"\x00" + b"\xFF\x51\x03" + struct.pack(">I", 500000)[1:]  # tempo 120 BPM
    last = 0
    for abs_t, data in events:
        track += vlq(abs_t - last) + data
        last = abs_t
    track += vlq(BEAT) + b"\xFF\x2F\x00"                       # end of track

    header = b"MThd" + struct.pack(">IHHH", 6, 0, 1, PPQ)
    chunk = b"MTrk" + struct.pack(">I", len(track)) + bytes(track)
    out = os.path.join(here, "wled-midi-demo.mid")
    with open(out, "wb") as f:
        f.write(header + chunk)
    print("wrote", out, "(%d bytes, %d events)" % (len(header + chunk), len(events)))


if __name__ == "__main__":
    main()
