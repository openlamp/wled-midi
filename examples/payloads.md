# Reference payloads

What a Core mapping resolves to on the wire — `POST /json/state` to the WLED device.

| MIDI in | WLED JSON out |
|---|---|
| Note 60 (red, look) | `{"seg":[{"col":[[255,0,0]],"fx":0}]}` |
| Note 67 (white, look) | `{"seg":[{"col":[[255,255,255]],"fx":0}]}` |
| Note 68 (effect, look) | `{"seg":[{"fx":1,"sx":128,"ix":128}]}` |
| Note 48 (off, util) | `{"on":false}` |
| Note 52 (toggle, util) | `{"on":"t"}` |
| Note 53 (blackout, util) | `{"bri":0}` |
| Note 72 (beat, modifier) | *behaviour — pulse the look on the beat (over time)* |
| CC 1 value 100 | `{"bri":201}`  (`round(100/127*255)`) |
| CC 3 value 42, CC 4 value 127 | `{"seg":[{"col":[[R,G,B]]}]}` from `HSV(0.33,1.0,1.0)` |
| CC 5 value 64 (fxcount 118) | `{"seg":[{"fx":59}]}`  (`round(64/127*117)`) |
| CC 8 value 30 (palcount 71) | `{"seg":[{"pal":17}]}` |
| Program Change 4 | `{"ps":5}` |

Combined single POST (colour + effect + brightness at once):

```json
{"on":true,"bri":200,"seg":[{"col":[[255,0,0]],"fx":1,"sx":128,"ix":200,"pal":0}]}
```

Targeting a specific segment (channel → segment N): set the segment `id`:

```json
{"seg":[{"id":2,"col":[[0,0,255]]}]}
```
