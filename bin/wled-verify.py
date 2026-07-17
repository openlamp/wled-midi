#!/usr/bin/env python3
"""wled-verify — send the wled-midi payloads to a real WLED device and watch it react.

The one thing self-tests can't prove is that a real WLED device forwards the individual-LED
`seg[].i` payload (used by strip / mpe / matrix) and the look colours the way the convention
assumes. This script sends those exact payloads over the local HTTP JSON API so you can confirm
on hardware when the rig is back online. stdlib only.

Usage:  python3 bin/wled-verify.py <wled-ip> [--leds N] [--slow]
        python3 bin/wled-verify.py 192.168.1.50
        python3 bin/wled-verify.py 192.168.1.50 --leds 144 --slow

Watch the lamp/strip: each step prints what it sends and what you should SEE. A step that
doesn't match on the device is a real finding to feed back into the impl (engine / web / matrix).
"""
import sys, json, time, argparse, urllib.request

# wled-midi look notes 60-67 -> colours (SPEC §"looks"); a subset to eyeball.
LOOKS = [
    ("red",     [255, 0, 0]),
    ("green",   [0, 255, 0]),
    ("blue",    [0, 0, 255]),
    ("white",   [255, 255, 255]),
]


def post(ip, body, note):
    data = json.dumps(body).encode()
    req = urllib.request.Request("http://%s/json/state" % ip, data=data,
                                 headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=3).read()
        print("  → %-46s  SEE: %s" % (json.dumps(body), note))
    except Exception as e:
        print("  ! POST failed (%s) — is %s reachable?  %s" % (e, ip, json.dumps(body)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ip")
    ap.add_argument("--leds", type=int, default=30, help="LED count on the strip (for the i-payload test)")
    ap.add_argument("--slow", action="store_true", help="pause 1.5s between steps to eyeball each")
    a = ap.parse_args()
    gap = 1.5 if a.slow else 0.6
    N = a.leds

    print("wled-verify → %s  (%d LEDs)\n" % (a.ip, N))

    print("[1] power + brightness (lamp mode: util 'on', CC1 bri)")
    post(a.ip, {"on": True, "bri": 128}, "lamp ON, mid brightness")
    time.sleep(gap)

    print("\n[2] looks — note 60-67 → whole-segment colours (fx off)")
    for name, col in LOOKS:
        post(a.ip, {"seg": [{"col": [col], "fx": 0}]}, "solid %s" % name)
        time.sleep(gap)

    print("\n[3] individual-LED payload — the strip/mpe/matrix path (THE thing to verify)")
    print("    Expect: only the named pixels light, the rest stay off.")
    post(a.ip, {"on": True, "bri": 255, "seg": [{"i": [0, [255, 0, 0]]}]},
         "LED 0 = red, nothing else")
    time.sleep(gap)
    mid = N // 2
    post(a.ip, {"seg": [{"i": [mid, [0, 255, 0]]}]}, "LED %d = green (LED 0 still red)" % mid)
    time.sleep(gap)
    post(a.ip, {"seg": [{"i": [N - 1, [0, 0, 255]]}]}, "LED %d = blue (0 red, %d green)" % (N - 1, mid))
    time.sleep(gap)

    print("\n[4] polyphony in one payload — several pixels at once")
    post(a.ip, {"seg": [{"i": [0, [0, 0, 0], mid, [0, 0, 0], N - 1, [0, 0, 0]]}]},
         "those 3 pixels go dark together")
    time.sleep(gap)

    print("\n[5] a small moving dot (velocity→brightness feel)")
    for i in range(min(N, 12)):
        post(a.ip, {"seg": [{"i": [max(0, i - 1), [0, 0, 0], i, [0, 200, 255]]}]},
             "dot at LED %d" % i)
        time.sleep(0.15)

    print("\n[6] blackout")
    post(a.ip, {"seg": [{"i": ["0-%d" % (N - 1), [0, 0, 0]]}]}, "all pixels off (range clear)")
    post(a.ip, {"on": False}, "lamp OFF")

    print("\nDone. If [3]/[4]/[5] lit the RIGHT pixels, the individual-LED forwarding works on this")
    print("device → strip / mpe / matrix are hardware-confirmed. If not, capture what happened and")
    print("feed it back into the impl (the payload shape may need a per-firmware tweak).")


if __name__ == "__main__":
    main()
