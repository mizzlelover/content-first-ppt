# roadshow-deck · A content-first deck builder

![License](https://img.shields.io/github/license/mizzlelover/content-first-ppt?style=flat-square)
![Stars](https://img.shields.io/github/stars/mizzlelover/content-first-ppt?style=flat-square)
![Skill](https://img.shields.io/badge/Skill-Agent-111111?style=flat-square)
![Claude Code](https://img.shields.io/badge/Claude%20Code-Supported-6B5B95?style=flat-square)
![Codex](https://img.shields.io/badge/Codex-Supported-222222?style=flat-square)
![Output](https://img.shields.io/badge/Output-single--file%20HTML-0A7CFF?style=flat-square)

> 🌏 **中文版：[README.md](./README.md)**

An AI-agent skill for **Claude Code / Codex** that turns **your own material** into a presentation built **for a specific audience** — one you can actually stand up and deliver. It outputs **one self-contained HTML file** — it specializes in HTML (no PPTX): persistent breadcrumbs, non-linear appendix jumps, and per-slide auto-fit so even dense slides never clip.

Most PPT tools start by picking a good-looking template. This one starts by getting the content right. **Content is the core; visuals are the finish** — even with zero generated images, the typography of the text itself should carry the quality.

> **Design principle**: the most important thing a deck does is **organize the same material differently for different audiences**. Every deck should be content-driven; visuals are only a finishing touch. Get the content right and the audience stops noticing the visuals at all.

---

## Install in 30 seconds

One command, installed for both Claude Code and Codex (recommended):

```bash
npx skills add mizzlelover/content-first-ppt --skill roadshow-deck -a claude-code -a codex
```

Then just tell your agent:

```text
Turn this material into a roadshow deck — but first help me pin down who the audience is.
```

## What makes it different

- **Compute goes into the content first**: it ingests the source in full (every word, mark, and image — no skimming), then models it objectively, *before* any layout.
- **Audience-adaptive**: it confirms the audience with you up front (big boss / line manager / dept head / group exec / external exec / client operator / engineers…) and re-orders the narrative by what that audience cares about — not just reworded copy.
- **Problem-first**: it opens with one line that removes the information gap, then unfolds why-now / pain / how / edge / why-you / how-we-work / business-model — in an order that shifts with the audience.
- **Built for live delivery**: a persistent **breadcrumb** on every page plus **non-linear appendix jump + return** — for when you're interrupted, asked to go deeper, or have more than the body can hold.
- **Readability-first layout**: large type, high contrast, dense information, **no animation**; font scale is hard-validated, and it splits a page rather than shrinking type.
- **Single-file HTML, done well**: one self-contained `.html` that opens anywhere and presents offline; **per-slide auto-fit means dense slides scale to fit instead of clipping** (not screenshots of a webpage).
- **Images optional**: zero-image decks stand on their own; when useful, it calls an image model in one step (provider-agnostic, and it skips silently with no API key).

## Install

### Option 1 — one command (recommended)

```bash
npx skills add mizzlelover/content-first-ppt --skill roadshow-deck -a claude-code -a codex
```

`-a claude-code -a codex` installs for both platforms; omit it to choose interactively. To list the skills in the repo first:

```bash
npx skills add mizzlelover/content-first-ppt --list
```

### Option 2 — paste this to any AI with shell access

> Install the `roadshow-deck` Claude Code skill:
> 1. Make sure `~/.claude/skills/` exists.
> 2. `git clone https://github.com/mizzlelover/content-first-ppt.git /tmp/cfp`
> 3. Copy `/tmp/cfp/roadshow-deck` into `~/.claude/skills/roadshow-deck`.
> 4. Verify `~/.claude/skills/roadshow-deck/` contains `SKILL.md`, `method/`, `core/`.

### Option 3 — manual

The skill itself lives in the repo's `roadshow-deck/` subfolder; drop that into your skills directory:

```bash
git clone https://github.com/mizzlelover/content-first-ppt.git
cp -r content-first-ppt/roadshow-deck ~/.claude/skills/roadshow-deck   # Claude Code (user-level)
# Codex: merge content-first-ppt/roadshow-deck/adapters/codex/AGENTS.md into your project's root AGENTS.md
```

HTML rendering and validation are **pure standard library — zero dependencies**; no `pip install` after `git clone`. (Only the optional image backends need extra packages.)

### Triggers

Once installed, Claude Code discovers and invokes it automatically. Common phrasings:

- "Turn this material into a roadshow deck"
- "Make a slide deck from this document / notes / data"
- "Build a report / proposal / pitch deck"
- "把这份材料做成路演 PPT"

## Capabilities

- 🧠 **Full ingestion** — reads every word, mark, and image; builds an objective model before touching slides
- 🎯 **Audience emphasis matrix** — re-orders the story per audience: altitude and resources for execs, capability and delivery for operators
- 🧭 **Persistent breadcrumb** — small but always-present "where we are now" indicator
- 🔀 **Non-linear appendix** — body pages link out to appendix detail and jump back to where you were
- 🔠 **Hard readability checks** — font scale, contrast, jump targets, structure; errors must be fixed
- 🎨 **Content-driven style** — matches one of 7 mainstream styles by domain / audience / data density, not a fixed template
- 🖼 **Optional images** — OpenAI / Gemini / Stability backends, provider-agnostic, off by default
- 🛡 **Never clips** — overlong slides auto-fit to one screen; the bottom is never cut off
- 📄 **Single-file delivery** — one self-contained HTML, opens anywhere, easy to share

## Good fit / not a fit

**✅ Good**: roadshows, fundraising pitches, project reports, proposals, business reviews, explaining a long document or dataset to a specific person.

**❌ Not**: pure art posters, keynote-stage shows that need item-by-item animation, "just make the webpage pretty" with no regard for information density.

## Platform support

| Platform | Status | Notes |
|----------|--------|-------|
| Claude Code | ✅ Supported | Auto-discovered once in the skills directory; primary target of this release |
| OpenAI Codex | ✅ Supported | Merge `adapters/codex/AGENTS.md` into your root `AGENTS.md`; includes the optional image flow |
| Other CLIs / Agents | ⚪ Not officially targeted yet | The skill is host-agnostic (read files + run Python), but this version is tuned and verified only for the two above |

## Workflow

The skill is a structured protocol the agent runs stage by stage (**the model is the brain; the `core/` scripts are just deterministic hands**):

1. **Ingest in full** — every word and image, nothing dropped (`method/01-ingest.md`)
2. **Model objectively** — organize the raw material, flag gaps (`02-structure.md`)
3. **Confirm the audience** — ask about audience and setting, apply the emphasis matrix (`03-audience.md`)
4. **Problem-first ordering** — sequence by audience, split body vs. appendix (`04-narrative.md`)
5. **Author pages** — assertion headlines + evidence → `deck.json` (`05-authoring.md`)
6. **Visual system** — last step, content-driven style / type / light-dark rhythm (`06-visual-system.md`)

Then validate and render with deterministic scripts:

```bash
python core/build.py validate work/deck.json        # readability + structure checks (must pass)
python core/build.py html     work/deck.json -o out/ # single-file HTML (-o accepts a dir)
python core/build.py styles                          # the 7-style library with contrast ratios
python core/build.py recommend --domain ai --audience technical --density mid  # content → style
```

## Delivery: a single HTML file

- `out/<name>.html` — single file, self-contained, presents offline: `← →` to page, `Enter` for a quick page index, `Backspace` to return, click "expand" to jump to the appendix.
- **Per-slide auto-fit**: an overlong slide scales to one screen instead of clipping; large type, high contrast, readability first.
- Double-click to present — no PowerPoint/Keynote needed; easy to share, screenshot, or project.

## Style library (content-driven, not fixed templates)

You don't pick a skin first. The skill matches a style from content signals (domain / tone / audience / data density), you can override it, and it falls back to `minimal` when signals are weak:

| Style | Tone | Fits |
|-------|------|------|
| `swiss` | Grid · sans-serif · single accent · hairlines | tech / engineering / data / design / product |
| `editorial` | Serif headlines + sans body + mono labels, warm | humanities / brand / culture / media / story |
| `corporate` | Dark, restrained, authoritative, fine gold accents | business / strategy / finance / management |
| `consulting` | Light, blue-grey, chart-driven, structured | data / analysis / reports / operations / research |
| `minimal` | Near black-and-white + single accent, max whitespace | universal, product, the safe default |
| `tech` | Dark, cool cyan / blue accent, modern product feel | AI / SaaS / startup / launch |
| `bold` | Heavy type, high contrast, loud emphasis | fundraising / marketing / vision / campaign |

## Images (optional, off by default)

Used only when they genuinely help, never as decoration. Enable by setting any of `OPENAI_API_KEY` / `GEMINI_API_KEY` / `STABILITY_API_KEY` …; with none set it **skips images and still ships the deck**. It generates text-free concept images by default and overlays text as native blocks to avoid garbled glyphs.

## Repository layout

```
content-first-ppt/
├── README.md / README.en.md   ← repo intro (zh / en)
├── LICENSE                     ← AGPL-3.0
├── CONTRIBUTING.md
└── roadshow-deck/              ← the skill itself (this is what goes into ~/.claude/skills/)
    ├── SKILL.md                ← Claude Code entry point
    ├── method/                 ← methodology (the skill's "brain")
    ├── core/                   ← deterministic rendering (the "hands")
    ├── adapters/codex/         ← Codex integration snippet
    └── examples/               ← sample deck + one ready-to-open render
```

## FAQ

**Why HTML-only, no PPTX?** Concentrating on one medium is what lets the layout, whitespace, readability, and the "never clip" guarantee get polished. A single HTML file double-clicks into a show, is easy to share, and is the easiest format for an agent to read, edit, and verify. Need a static copy? Print to PDF from the browser.

**Why no animation?** A real roadshow isn't a keynote stage. Content should appear all at once, not fly in item by item; animation is a liability there.

**Can I use it with no images?** Yes. Images are off by default; a zero-image deck should still look sharp on typography alone — that's the whole point.

**Can I change the style?** Yes. Style is auto-recommended; you can also set `meta.style` to one of the 7. See `CONTRIBUTING.md` to add more.

## Contributing

Issues and PRs welcome — new styles, more `method/` methodology, extra validation rules, layout fixes. See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License & author

**AGPL-3.0** © 2026 [**谁是专家 (Who-Is-Expert)**](https://github.com/mizzlelover)

This skill (the `method/` methodology, the `core/` render pipeline, and the style library) is original work. You may use, modify, and distribute it, but **derivatives — including network-served versions — must also be released under AGPL-3.0 with attribution preserved**. Full terms in [LICENSE](./LICENSE).
