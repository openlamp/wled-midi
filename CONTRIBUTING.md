# Contributing to wled-midi

wled-midi is **young and co-constructed** — a draft convention shaped together with the people who
use WLED and build MIDI tools. Corrections, ideas and implementations are all welcome, and early on
the structure is expected to move and sharpen. The guiding line for every decision: **advanced,
integrated solutions usable by everyone.**

## Ways to help

- **Describe a need or use case** — open an [issue](https://github.com/openlamp/wled-midi/issues).
  The spec is a *write-down of real needs*; the clearest way to improve it is to tell us what you're
  trying to do that it doesn't cover yet.
- **Propose a change to the convention** — a PR touching [SPEC.md](SPEC.md). Keep it consistent with
  the two-layer split (Core = pure WLED JSON; Extensions = advisory) and the one-unified-syntax model.
- **Add an implementation** — built a tool that emits or receives the convention? Open a PR adding a
  row to the *Implementations* table in the [README](README.md).
- **Improve the docs or prior art** — the [docs/](docs/README.md) topic map, hardware guides, or a
  reference/credit we've missed.

## Ground rules that keep it coherent

- **One atomic spec.** The normative source is the single [SPEC.md](SPEC.md) — no parallel dialects.
  If you change a mapping, update the machine-readable [mapping.spec.json](mapping.spec.json) **and**
  keep the resolver green: `python3 resolve.py --selftest` must pass.
- **Core stays pure WLED.** Every Core mapping must resolve to a documented WLED JSON-state key, so a
  stock WLED device can adopt it with no extra software. Vendor- or engine-specific behaviour lives in
  Extensions.
- **Backward-compat matters once it settles.** While `status: draft` the numbers can still move; call
  out any breaking change clearly in [CHANGELOG.md](CHANGELOG.md) with a version bump.
- **Conventional commits** (`feat(scope): …`, `docs: …`) and a short, plain-language rationale.

## Openness & patents

Contributions are made under the project's open terms: the **code** under its
[LICENSE](LICENSE) (currently MIT — see the [licensing chapter](docs/licensing.md), an open question
pending WLED-community feedback), and the **convention** under the royalty-free, non-assertion policy
in [SPEC §14](SPEC.md). In short: by contributing you agree your contribution can be used freely by
everyone, on the same open basis.

## Be kind

This is a friendly, community-minded project that respects the wider ecosystem — including closed and
commercial products (see the [piano-learning tools](README.md#credits--prior-art) note). We assume
good faith, credit ideas generously, and aim for *each finds its place*.
