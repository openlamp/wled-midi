#!/usr/bin/env python3
"""wled-midi reference resolver — turn a MIDI event into the WLED JSON it means.

The *executable* form of SPEC.md's transforms: a golden reference for implementers
and tests. Spec-only helper (stdlib) — NOT a runtime (no MIDI I/O, no HTTP). Reads
the default map from mapping.spec.json.

Usage:
  python3 resolve.py note 60                 # look: red
  python3 resolve.py note 68                 # look: effect
  python3 resolve.py note 48                 # util: off
  python3 resolve.py cc 1 100                # brightness
  python3 resolve.py cc 5 64 --fxcount 118   # effect id
  python3 resolve.py pc 4                     # preset ps=5
  python3 resolve.py --selftest              # validate the map + example assertions
"""
import json, os, sys, colorsys, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "mapping.spec.json")
FALLBACK_FXCOUNT, FALLBACK_PALCOUNT = 118, 71


def load():
    return json.load(open(SPEC))


def _col(r, g, b):
    return {"seg": [{"col": [[r, g, b]]}]}


def resolve_note(spec, note, vel=127):
    """Return the WLED JSON for a note-on, or a {'_behaviour': ...} marker for
    modifiers/stateful actions that aren't a single static payload."""
    n = spec["notes"].get(str(note))
    if not n:
        return None
    zone = n.get("zone")
    if zone == "look":
        if n.get("effect"):
            return {"seg": [{"fx": 1, "sx": 128, "ix": 128}]}   # default effect look
        r, g, b = n["col"]
        out = {"seg": [{"col": [[r, g, b]], "fx": 0}]}
        if spec.get("velocity", {}).get("to_bri"):
            out["bri"] = round(vel / 127 * 255)
        return out
    if zone == "util":
        if "on" in n:
            return {"on": n["on"]}
        if "bri" in n:
            return {"bri": n["bri"]}
        if "fx" in n:
            return {"seg": [{"fx": n["fx"]}]}
        if "restore" in n:
            return {"_behaviour": "restore-" + n["restore"]}     # stateful (last bri)
    if zone == "modifier":
        return {"_behaviour": n.get("name")}                     # beat / flash: over-time
    return None


def resolve_cc(spec, num, val, fxcount=FALLBACK_FXCOUNT, palcount=FALLBACK_PALCOUNT,
               hue=None, sat=1.0):
    """Resolve a Control Change. hue/sat are stateful (combined per channel); for a
    single-shot reference, hue defaults to the CC value on CC3, sat to 1.0."""
    kind = spec["cc"].get(str(num))
    if kind == "bri":
        return {"bri": round(val / 127 * 255)}
    if kind == "cct":
        return {"seg": [{"cct": round(val / 127 * 255)}]}
    if kind == "hue":
        r, g, b = colorsys.hsv_to_rgb(val / 127.0, sat, 1.0)
        return _col(round(r * 255), round(g * 255), round(b * 255))
    if kind == "sat":
        h = hue if hue is not None else 0.0
        r, g, b = colorsys.hsv_to_rgb(h, val / 127.0, 1.0)
        return _col(round(r * 255), round(g * 255), round(b * 255))
    if kind == "fx":
        return {"seg": [{"fx": round(val / 127 * (fxcount - 1))}]}
    if kind == "sx":
        return {"seg": [{"sx": round(val / 127 * 255)}]}
    if kind == "ix":
        return {"seg": [{"ix": round(val / 127 * 255)}]}
    if kind == "pal":
        return {"seg": [{"pal": round(val / 127 * (palcount - 1))}]}
    return None


def resolve_pc(spec, prog):
    pc = spec.get("program_change", {"target": "ps", "offset": 1})
    return {pc.get("target", "ps"): prog + pc.get("offset", 1)}


def selftest(spec):
    fails = []
    # 1) every mapped note resolves to something
    for note in spec["notes"]:
        if resolve_note(spec, int(note)) is None:
            fails.append(f"note {note} did not resolve")
    # 2) every CC kind resolves
    for num in spec["cc"]:
        if resolve_cc(spec, int(num), 64) is None:
            fails.append(f"cc {num} did not resolve")
    # 3) example assertions (must match examples/payloads.md)
    cases = [
        (resolve_note(spec, 60), {"seg": [{"col": [[255, 0, 0]], "fx": 0}]}, "note 60 = red"),
        (resolve_note(spec, 48), {"on": False}, "note 48 = off"),
        (resolve_cc(spec, 1, 100), {"bri": 201}, "cc1 100 = bri 201"),
        (resolve_cc(spec, 5, 64, fxcount=118), {"seg": [{"fx": 59}]}, "cc5 64 = fx 59"),
        (resolve_cc(spec, 8, 30, palcount=71), {"seg": [{"pal": 17}]}, "cc8 30 = pal 17"),
        (resolve_pc(spec, 4), {"ps": 5}, "pc 4 = ps 5"),
    ]
    for got, want, label in cases:
        if got != want:
            fails.append(f"{label}: got {got}, want {want}")
    if fails:
        print("SELFTEST FAILED:")
        for f in fails:
            print("  -", f)
        return 1
    print(f"selftest OK — {len(spec['notes'])} notes, {len(spec['cc'])} CCs, "
          f"{len(cases)} assertions")
    return 0


def main():
    spec = load()
    ap = argparse.ArgumentParser(description="wled-midi reference resolver")
    ap.add_argument("kind", nargs="?", choices=["note", "cc", "pc"])
    ap.add_argument("args", nargs="*", type=int)
    ap.add_argument("--fxcount", type=int, default=FALLBACK_FXCOUNT)
    ap.add_argument("--palcount", type=int, default=FALLBACK_PALCOUNT)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest(spec))
    if a.kind == "note":
        out = resolve_note(spec, a.args[0], a.args[1] if len(a.args) > 1 else 127)
    elif a.kind == "cc":
        out = resolve_cc(spec, a.args[0], a.args[1], a.fxcount, a.palcount)
    elif a.kind == "pc":
        out = resolve_pc(spec, a.args[0])
    else:
        ap.print_help(); return
    print(json.dumps(out))


if __name__ == "__main__":
    main()
