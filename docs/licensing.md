# Licensing — an open question, deliberately not settled yet

> **Status: undecided, on purpose.** The code currently ships under [MIT](../LICENSE), and the
> *specification* is covered by the royalty-free non-assertion policy in [SPEC §14](../SPEC.md).
> Whether the **code** stays MIT or moves to **Apache-2.0** is an **open decision we are holding
> until we have feedback from the WLED community** — the convention's natural home. Nothing is being
> changed for now; this page just records the question so the choice is made in the open.

## Why it's open

wled-midi is young and **co-constructed** (see the status note in the [README](../README.md)). The
licence should reflect what best serves the WLED ecosystem and the people who build on it — so it's
right to ask *them* before settling, rather than lock it in early and churn it later.

Two things are already true regardless of the outcome:

- The **convention stays free for everyone** — [SPEC §14](../SPEC.md) is a dated defensive
  publication + a royalty-free, irrevocable non-assertion pledge. That protection does **not** depend
  on the code licence.
- The code is **permissively licensed today** (MIT) — anyone can already use it, in open-source or
  commercial products.

So this is not "closed vs open" — both candidates are permissive and open. It's a finer choice about
**patent hygiene**.

## The choice: MIT vs Apache-2.0

| | **MIT** (current) | **Apache-2.0** (candidate) |
|---|---|---|
| Permissive, commercial-friendly | ✅ | ✅ |
| Simplicity / ubiquity | ✅ the most widely used, shortest | slightly more ceremony (NOTICE file, header recommendation) |
| **Explicit patent grant from contributors** | ❌ none | ✅ every contributor grants a patent licence to their contribution |
| **Patent-retaliation clause** | ❌ | ✅ a contributor who sues over patents loses their grant |
| Trademark handling | silent | explicit (no trademark rights granted) |

**In plain terms:** MIT is the simplest and most-adopted permissive licence, but it says *nothing*
about patents. Apache-2.0 is just as permissive but adds an **explicit patent grant** from anyone who
contributes code, plus a clause that a contributor who launches a patent attack loses their licence —
better hygiene once a project has **external contributors** and a commercial ecosystem forms.

### What would tip it

- Toward **Apache-2.0**: external contributors start landing code; companies build products on it and
  want a clear contributor-patent grant; we want maximum patent safety as the ecosystem grows.
- Toward **MIT**: simplicity and the widest possible adoption stay the priority, and the SPEC §14
  non-assertion pledge is judged enough for the convention's patent safety.

A common resolution is a **hybrid**: Apache-2.0 on the *code* repos (for the contributor patent
grant) and MIT + §14 on the *spec* repo (mostly docs + `resolve.py`). That's on the table too.

## Practicalities (for when we do decide)

- Relicensing our own code MIT → Apache-2.0 is clean: it's Benoît's code (with Claude as co-author),
  so there are no third-party contributors whose consent would be needed.
- Existing MIT copies already out there stay MIT — relicensing only governs the project going forward.
- The decision is reversible in spirit (you can always dual-license or add grants), so waiting costs
  nothing.

Whatever we pick, the guiding line holds: **advanced, integrated solutions usable by everyone.**
