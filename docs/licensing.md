# Licensing — an open question, deliberately not settled yet

> **Preamble — reconcile everyone, nothing fixed in advance.** The aim of this project is to **bring all
> the actors together**, not to pick a camp: the WLED community and its open ethos; the makers and
> companies who need a **closed part to make a living**; the DIY, education and hobby world that thrives
> on **interoperability**; and the tool authors who build the bridges between them. The licence question
> is approached **in that spirit, with no predetermined answer** — nothing on this page is a settled
> position. It's an open reflection, meant to be weighed *together* and adjusted as the project and its
> community grow. The goal, as everywhere in the project, is that **each finds its place**.
>
> **If any actor has an explicit need — a guarantee for a commercial or closed use case, patent
> certainty, a specific licence, or anything else that would let you build on this with confidence —
> please voice it.** Open an [issue](https://github.com/openlamp/wled-midi/issues) or reach the
> maintainer ([@Beennnn](https://github.com/Beennnn)); it will be genuinely weighed in the decision.
> Better to hear the need now, while the choice is still open, than after it's settled.

> **Status: undecided, on purpose.** The code currently ships under [MIT](../LICENSE), and the
> *specification* is covered by the royalty-free non-assertion policy in [SPEC §14](../SPEC.md).
> Whether the **code** stays MIT or moves to another licence is an **open decision we are holding
> until we have feedback from the WLED community** — the convention's natural home. Nothing is being
> changed for now; this page records the question, the surrounding landscape, and the trade-offs so
> the choice is made in the open.

## Why it's open

wled-midi is young and **co-constructed** (see the status note in the [README](../README.md)). The
licence should reflect what best serves the WLED ecosystem and the people who build on it — so it's
right to ask *them* before settling, rather than lock it in early and churn it later. Two things are
already true regardless of the outcome:

- The **convention stays free for everyone** — [SPEC §14](../SPEC.md) is a dated defensive publication
  + a royalty-free, irrevocable non-assertion pledge. That protection does **not** depend on the code
  licence.
- The code is **permissively licensed today** (MIT) — anyone can already use it, open-source or
  commercial.

So this is not "closed vs open" — it's a finer choice about **patent hygiene** and **how much we want
improvements to stay open**.

## Inventory — the OpenLamp repos (ours)

| Repo | Role | License (repo) | Note |
|---|---|---|---|
| [openlamp/wled-midi](https://github.com/openlamp/wled-midi) | the convention (spec + docs) | **MIT** | + [SPEC §14](../SPEC.md) RF non-assertion policy |
| [openlamp/engine](https://github.com/openlamp/engine) | reference implementation | **MIT** | *PyPI `openlamp-lamp` still shows EUPL-1.2 on the old 0.1.x builds — stale; corrects on the next release* |
| [openlamp/wled-midi-web](https://github.com/openlamp/wled-midi-web) | browser impl | **MIT** | |
| [openlamp/matrix](https://github.com/openlamp/matrix) | multi-device router | **MIT** | |
| [openlamp/bome](https://github.com/openlamp/bome) | Bome pack | **MIT** | |
| [openlamp/live](https://github.com/openlamp/live) | Ableton frontend | **MIT** | |
| [openlamp/midi](https://github.com/openlamp/midi) | tempo / Ableton Link | **MIT** | *uses Ableton Link (GPLv2+) — kept clean via a **process boundary** (see below); `openlamp-midi` PyPI also shows stale EUPL* |

Everything of ours is **MIT today**. The one real drift to fix on the next publish: two PyPI packages
still carry an **EUPL-1.2** licence field from before the repos were relicensed to MIT.

## Inventory — the ecosystem (others), verified via the GitHub API

| Project | Role | License |
|---|---|---|
| **[WLED](https://github.com/wled/WLED)** | the platform (firmware) — output pillar | **EUPL-1.2** (weak copyleft + patent grant) |
| **MIDI** ([MIDI Association](https://midi.org)) | the input standard | **open standard, royalty-free to implement** (not a software licence) |
| [xLights](https://github.com/smeighan/xLights) | LED sequencer → WLED | **GPL-3.0** |
| [LedFx](https://github.com/LedFx/LedFx) | audio-reactive → WLED | **GPL-3.0** |
| [QLC+](https://github.com/mcallegari/qlcplus) | DMX / lighting control (MIDI in) | **Apache-2.0** |
| [Chataigne](https://github.com/benkuper/Chataigne) | MIDI/OSC/DMX glue | **GPL-3.0** |
| [Hyperion.ng](https://github.com/hyperion-project/hyperion.ng) | ambient lighting → WLED | **MIT** |
| [onlaj/Piano-LED-Visualizer](https://github.com/onlaj/Piano-LED-Visualizer) | piano visualiser | **MIT** |
| [ShowMIDI](https://github.com/gbevin/ShowMIDI) | MIDI monitor | **GPL-3.0** |
| [Ableton Link](https://github.com/Ableton/link) | tempo-sync SDK | **GPLv2+** *or* a commercial licence (dual) |
| [Bome MIDI Translator](https://www.bome.com/products/miditranslator) | MIDI mapper | **proprietary** (commercial) |
| Trevliga Spel Stream-Deck plugin | Stream Deck MIDI | **proprietary** (freeware) |

**Two things stand out.** (1) The platform we build on — **WLED — is EUPL-1.2**, a *copyleft* licence:
the WLED community chose to keep improvements open, not maximally permissive. (2) The audio/lighting
neighbours (**xLights, LedFx, Chataigne, ShowMIDI**) are mostly **GPL-3.0**; the DMX cousin **QLC+** is
**Apache-2.0**; the WLED-adjacent tools (**Hyperion.ng, onlaj**) are **MIT**. So the space spans the
full range — permissive *and* copyleft coexist healthily.

## Background — copyleft & the EUPL, in plain terms

**Permissive vs copyleft** is the core axis of open-source licences:

- **Permissive** (MIT, Apache-2.0): *"do almost anything, just keep the notice."* You can take the code,
  modify it, and ship it inside a **closed, proprietary product** with no obligation to share your
  changes back. Maximum freedom for whoever uses the code; no guarantee it stays open downstream.
- **Copyleft** (GPL, LGPL, MPL, EUPL): *"same freedoms, but they must travel with the code."* You can
  use and modify it freely, **but if you distribute it (or a derivative) it has to be under the
  same/compatible open licence** — so improvements stay open. It uses copyright *to guarantee* the code
  can't be re-closed. Also called **share-alike**.

Copyleft comes in strengths:

- **Strong copyleft** (GPL-3.0): the obligation covers the **whole program** that includes the code —
  link GPL code into your app and the *whole app* must be GPL. Powerful, but it keeps the code out of
  closed products entirely.
- **Weak / file-level copyleft** (LGPL, MPL, **EUPL**): the obligation covers only the **library or the
  modified files** — you can combine it with proprietary code *around* it, and only your changes *to it*
  must stay open. A middle ground.
- **Network copyleft** (AGPL): even offering it as a *network service* triggers the share-back
  obligation — closes the "SaaS loophole" of modifying GPL code but never distributing a binary.

**The EUPL (European Union Public Licence)** is a **weak / file-level copyleft** licence with a few
unusual traits:

- **Drafted by the European Commission** (v1.1 in 2007, v1.2 in 2017) and published, legally equivalent,
  in **all official EU languages** — a rare, government-vetted open licence written for EU copyright law.
- **A compatibility clause** — its standout feature: it *lists* other copyleft licences it can mix with
  (GPLv2/v3, AGPL, MPL, LGPL, CeCILL, …). Combine EUPL code with, say, GPL code and distribute the
  result, and you may relicense the whole under that compatible licence — dissolving the classic
  "two copyleft licences won't mix" headache.
- **An explicit patent grant**, and it covers *"distribution **or communication to the public**"* — so
  it reaches network / hosted use more than a plain GPL does.

**Why WLED uses it:** EUPL-1.2 keeps **WLED's own firmware improvements open** — you can't take WLED,
close it, and ship it proprietary — while staying interoperable with the GPL world around it. A
"keep the ecosystem open, but play well with others" choice.

**Does it reach us?** No — copyleft travels only through *code*. Our engine speaks to WLED **over the
network** (HTTP/UDP); it doesn't incorporate a line of WLED source, so no EUPL obligation flows into our
repos. We're free to pick our own licence — WLED's choice is a *signal of community values*, not a
constraint on us.

## License families at a glance

| License | Type | Patent clause | Copyleft scope | In one line |
|---|---|---|---|---|
| **MIT** | permissive | none | none | simplest, maximal adoption, silent on patents |
| **Apache-2.0** | permissive | ✅ explicit grant + retaliation | none | permissive **and** patent-safe; a little ceremony |
| **GPL-3.0** | strong copyleft | ✅ explicit grant | the whole derivative work | improvements must stay open; can't be embedded in a *closed* product |
| **EUPL-1.2** | weak / file copyleft | ✅ explicit grant | modified files, with a **compatibility clause** (interoperates with GPL, MPL, …) | EU-drafted; copyleft but deliberately interoperable — **WLED's choice** |
| **Proprietary** | closed | — | — | vendor-controlled (Bome, Trevliga Spel) |

## Pros & cons of switching *a project* to each

What it would mean to put one of our repos under a given licence:

**Stay MIT**
- ➕ Widest possible adoption; anyone (incl. closed products) can build on it — exactly what a
  *convention* wants. Shortest, most-recognised text.
- ➖ No patent clause; permits closed forks that give nothing back (fine for a spec, less ideal for a
  reference impl you'd like to see improved in the open).

**Apache-2.0**
- ➕ Still fully permissive, plus an **explicit contributor patent grant + retaliation** — better hygiene
  once external contributors and a commercial ecosystem appear. It's also **QLC+'s** choice, a direct
  MIDI-→-lights cousin.
- ➖ Slightly more ceremony (NOTICE file, header recommendation); marginally less ubiquitous than MIT.

**GPL-3.0**
- ➕ **Forces improvements to stay open** — aligns with the community-first spirit and echoes WLED's own
  copyleft instinct; it's what most neighbours (xLights, LedFx, Chataigne, ShowMIDI) use.
- ➖ **Blocks embedding in closed products** → would cut a convention off from the very commercial tools
  we want to interoperate with. Standards are almost never copyleft (they must be freely
  implementable). Viable for a *reference impl*, wrong for the *convention* itself.

**EUPL-1.2**
- ➕ Same **copyleft-but-interoperable** stance as WLED (nice symmetry with the platform), an explicit
  patent grant, and a compatibility clause so it plays with GPL/MPL. A statement of "keep the ecosystem
  open" that WLED users may relate to.
- ➖ Less familiar outside the EU; still copyleft, so it limits closed embedding the way GPL does (just
  at file level). More to explain to contributors.

## Per-project licensing is on the table

Different repos can carry **different licences** — and one may even *need* to:

- **The convention repo** ([wled-midi](https://github.com/openlamp/wled-midi)) wants a **permissive**
  licence (MIT/Apache) + the [§14](../SPEC.md) RF policy, so *anyone* — including closed products — can
  implement it. Copyleft here would defeat the purpose of a standard.
- **Reference implementations** (engine, web, matrix, bome) can lean either way — permissive for reach,
  or copyleft/EUPL if we want forks to stay open. This is the real MIT-vs-Apache-2.0-vs-EUPL debate.
- **[openlamp/midi](https://github.com/openlamp/midi)** touches **Ableton Link (GPLv2+)**. It stays MIT
  by keeping a **process boundary** — Link runs as a separate process / the GPL binding isn't bundled
  into our distributed code, so no derivative-work obligation flows in. If that ever changed (statically
  linking Link into a shipped binary), *that* repo would have to go GPL while the others stayed as they
  are. A concrete case where one project's licence diverges by necessity.

So the likely shape: **permissive + §14 for the convention; a considered choice (MIT / Apache-2.0 /
EUPL) for the reference impls; GPL only where a dependency forces it.** We'll settle it with the WLED
community's input.

## Proposed direction — a leaning (final call still pending WLED feedback)

The instinct: **copyleft fits the project's spirit** (keep improvements open, as WLED does) — *but*
without scaring off makers who need a **closed part to survive**, and without adopting anything that
would restrict legitimate exploitation, **including commercial / closed** use. The reconciliation is a
**layered, best-of-both-worlds** setup:

- **The convention** ([wled-midi](https://github.com/openlamp/wled-midi)) → stays **permissive (MIT) +
  [§14](../SPEC.md)**. A *standard* must be implementable by **everyone, including fully closed
  products** — copyleft here would defeat its purpose.
- **The reference implementations** (engine, web, matrix, bome, midi, live) → **MPL-2.0** (Mozilla
  Public License 2.0), the textbook *best of both worlds*:
  - **Weak / file-level copyleft** → improvements *to our files* stay open (the copyleft spirit, aligned
    with WLED's openness).
  - **Closed-friendly** → a company can embed or wrap the code in a **closed, commercial product**; only
    direct modifications to the MPL files come back. Nobody who needs a closed layer is shut out.
  - **Explicit patent grant + retaliation**, and **compatible with GPL / Apache / EUPL** if code mixes.
- **Respect WLED's EUPL where WLED code is actually involved** — a contribution to WLED itself (a
  usermod) is EUPL, as required. But **we do not migrate our repos to EUPL**: we incorporate no WLED
  source (we speak over the network), so it isn't required, and MPL gives the same weak-copyleft benefit
  without EUPL's narrower familiarity or EU-specific framing — and **without restricting closed
  exploitation** the way full copyleft would.

Net effect: the code stays open and improvements flow back (copyleft), yet **closed and commercial use
stays fully possible** (MPL around the impls, MIT for the standard). Best of both worlds; WLED's spirit
respected; nobody excluded. **We'll confirm with the WLED community before flipping any licence.**

## Practicalities (for when we do decide)

- Relicensing our own code is clean: it's Benoît's code (with Claude as co-author), so there are no
  third-party contributors whose consent would be needed.
- Existing copies already out there keep their old licence — relicensing only governs the project going
  forward. Waiting costs nothing (you can always dual-license or add grants later).
- **Fix on the next publish:** align the PyPI `license` metadata (`openlamp-lamp`, `openlamp-midi`) to
  MIT — the current pyproject is already MIT, so the next release corrects the stale EUPL field.

Whatever we pick, the guiding line holds: **advanced, integrated solutions usable by everyone.**
