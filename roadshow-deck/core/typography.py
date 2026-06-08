# roadshow-deck · 内容为王的路演 PPT 技能 / content-first roadshow PPT skill
# Copyright (C) 2026 谁是专家 (Who-Is-Expert) · https://github.com/mizzlelover
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Typography, geometry, theming, and color utilities for roadshow-deck.

Single source of truth for the legibility rules the whole skill enforces.
Font sizes are expressed in points (pt) on the AUTHORITATIVE 960x540pt (16:9)
canvas and converted to HTML px by ONE scale factor, so the type scale stays
grounded in projection-legibility research. Standard library only (no deps).
"""
from __future__ import annotations

import json
from pathlib import Path

# --- Geometry: authoritative slide is 16:9 = 13.333in x 7.5in = 960 x 540 pt ---
SLIDE_W_PT = 960.0
SLIDE_H_PT = 540.0
SLIDE_W_PT_43 = 720.0          # 4:3 = 10in wide (optional)

# HTML design viewport (px). One scale factor keeps pt and px in lockstep.
HTML_W_PX = 1280.0
HTML_H_PX = 720.0
PT_TO_PX = HTML_W_PX / SLIDE_W_PT      # = 1.3333...


def pt_to_px(pt: float) -> float:
    return round(float(pt) * PT_TO_PX, 2)


def slide_size_pt(aspect: str = "16:9"):
    return (SLIDE_W_PT_43, SLIDE_H_PT) if aspect == "4:3" else (SLIDE_W_PT, SLIDE_H_PT)


# --- Default type scale (pt) ---
# Grounded in projection-legibility & typography research:
#   * Projection baseline body = 28pt (Kawasaki 10/20/30 → 30pt; Duarte slide:ology → ≥28pt;
#     <24pt is "document, not slide"). AVIXA DISCAS geometry → element height ≈ 3–4% of
#     screen height as the floor, lifted to ~28pt for CJK + projection contrast loss.
#   * Modular scale (Bringhurst/Tim Brown): body 28 → subhead 35 (×1.25) → title 44 (×1.57)
#     → section 56 (×2) → cover 64 (×2.3); ratios kept in 1.25–1.6 for perceptible steps.
DEFAULT_TYPE_SCALE = {
    "cover_title": 52, "cover_subtitle": 25,
    "section_divider": 46,
    "headline": 36, "subhead": 23,
    "body": 24, "bullet": 24,
    "kpi_num": 60, "kpi_label": 14,
    "table": 18, "table_header": 15,
    "quote": 28, "callout": 23,
    "caption": 15, "tag": 13,
    "breadcrumb": 13, "footer": 12, "pagenum": 13,
}

# Line-height (Bringhurst rhythm; USWDS): body 1.35–1.5, titles 1.1–1.25.
LINE_HEIGHT = {"body": 1.45, "title": 1.18}

# Validator thresholds (pt). The user's first principle is "font size matters most".
FLOORS = {
    "any_error": 12,
    "body_error": 16, "body_warn": 20,          # refined on-screen scale; body ≈ 24pt
    "headline_error": 24, "headline_warn": 30,
}

# Content-density ceilings. Measure (line length) from Bringhurst (45–75 CPL Latin) and
# WCAG SC 1.4.8 (≤40 CJK glyphs): roadshow CJK body 18–30 chars/line, hard cap 40.
LIMITS = {
    "max_blocks_per_slide": 6,
    "max_bullets": 6,
    "max_bullet_chars": 44,                      # ~1.5 lines at measure
    "max_headline_chars": 40,                    # question headlines stay concise (≤2 lines)
    "measure_cjk_ideal": 30, "measure_cjk_max": 40,
    "min_contrast_body": 4.5,                    # WCAG AA normal text
    "min_contrast_large": 3.0,                   # WCAG AA large text
    "min_contrast_enhanced": 7.0,                # WCAG AAA — prefer for projected titles/numbers
}

# --- Look presets (visual register; mainstream editorial / Swiss design systems) ---
LOOK_DEFAULTS = {
    # editorial = magazine (serif headlines, warm, mono labels); swiss = international
    # typographic (sans, thin huge type, single accent, squared); clean = strong neutral.
    "editorial": {"radius": 0, "label_upper": True, "texture": "none", "headline": "serif", "num": "serif"},
    "swiss":     {"radius": 0, "label_upper": True, "texture": "none", "headline": "sans", "num": "sans"},
    "clean":     {"radius": 10, "label_upper": True, "texture": "none", "headline": "sans", "num": "sans"},
    "bold":      {"radius": 0, "label_upper": True, "texture": "none", "headline": "sans", "num": "sans"},
}

# Weight ladder per look (numeric CSS weights). "bigger=lighter" is the Swiss
# rule; editorial keeps heavy serif display.
WEIGHTS_BY_LOOK = {
    "editorial": {"cover_title": 800, "section_divider": 800, "headline": 700, "subhead": 600,
                  "body": 400, "bullet": 400, "kpi_num": 800, "kpi_label": 600, "label": 600,
                  "quote": 500, "callout": 600, "table_header": 700, "table": 400},
    "swiss":     {"cover_title": 300, "section_divider": 300, "headline": 400, "subhead": 500,
                  "body": 400, "bullet": 400, "kpi_num": 300, "kpi_label": 600, "label": 600,
                  "quote": 400, "callout": 600, "table_header": 700, "table": 400},
    "clean":     {"cover_title": 800, "section_divider": 800, "headline": 700, "subhead": 600,
                  "body": 400, "bullet": 400, "kpi_num": 800, "kpi_label": 600, "label": 600,
                  "quote": 600, "callout": 600, "table_header": 700, "table": 400},
    "bold":      {"cover_title": 900, "section_divider": 900, "headline": 800, "subhead": 700,
                  "body": 400, "bullet": 500, "kpi_num": 900, "kpi_label": 700, "label": 700,
                  "quote": 700, "callout": 700, "table_header": 800, "table": 500},
}

# Font ROLES: sans (body), serif (editorial display), mono (tracked labels). Each has a
# latin + CJK stack for HTML.
DEFAULT_FONTS = {
    "html_sans": "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif",
    "html_sans_cjk": "'PingFang SC','Microsoft YaHei','Source Han Sans SC','Noto Sans SC',sans-serif",
    "html_serif": "'Playfair Display','Source Serif 4',Georgia,'Times New Roman',serif",
    "html_serif_cjk": "'Songti SC','Source Han Serif SC','Noto Serif SC','SimSun',serif",
    "html_mono": "'IBM Plex Mono',ui-monospace,'SF Mono',Menlo,Consolas,monospace",
}

# Label letter-spacing (em) for mono tracked labels in HTML.
TRACKING = {"kicker": 0.28, "tag": 0.22, "breadcrumb": 0.12, "meta": 0.16, "footer": 0.14}

# --- Grid / spacing (pt on the 960x540 slide) ---
GRID = {
    "margin_l": 56, "margin_r": 56,
    "margin_top": 30, "margin_bottom": 28,
    "cols": 12, "gutter": 16,
    "headline_top": 44, "headline_gap": 14,
    "breadcrumb_h": 22, "footer_h": 18,
}


def content_box(aspect: str = "16:9"):
    """(x, y, w, h) in pt of the main content area below headline / above footer."""
    w_pt, h_pt = slide_size_pt(aspect)
    x = GRID["margin_l"]
    w = w_pt - GRID["margin_l"] - GRID["margin_r"]
    y = GRID["margin_top"]
    h = h_pt - GRID["margin_top"] - GRID["margin_bottom"]
    return (x, y, w, h)


# --- Color / contrast (WCAG 2.1) ---
def hex_to_rgb(h: str):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _lin(c: int) -> float:
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def rel_luminance(hex_color: str) -> float:
    r, g, b = hex_to_rgb(hex_color)
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast_ratio(fg: str, bg: str) -> float:
    l1, l2 = rel_luminance(fg), rel_luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return round((hi + 0.05) / (lo + 0.05), 2)


# --- Style library loading ---
STYLES_DIR = Path(__file__).parent / "styles"
THEMES_DIR = STYLES_DIR  # back-compat alias


def load_theme(name_or_path: str) -> dict:
    p = Path(name_or_path)
    if not p.suffix and not p.exists():
        p = STYLES_DIR / f"{name_or_path}.json"
    if not p.exists():
        p = STYLES_DIR / "minimal.json"
    theme = json.loads(p.read_text(encoding="utf-8"))
    ts = dict(DEFAULT_TYPE_SCALE)
    ts.update(theme.get("type_scale", {}))
    theme["type_scale"] = ts
    theme.setdefault("palette", {})
    theme.setdefault("look", "clean")
    # fonts: fill role defaults, then map legacy keys (html_latin/html_cjk → html_sans/..)
    raw = theme.get("fonts", {})
    fonts = dict(DEFAULT_FONTS)
    for old, new in (("html_latin", "html_sans"), ("html_cjk", "html_sans_cjk")):
        if old in raw and new not in raw:
            fonts[new] = raw[old]
    fonts.update(raw)
    theme["fonts"] = fonts
    return theme


def font_pt(theme: dict, key: str) -> float:
    return float(theme["type_scale"].get(key, DEFAULT_TYPE_SCALE.get(key, 24)))


def font_px(theme: dict, key: str) -> float:
    return pt_to_px(font_pt(theme, key))


# --- look / register accessors ---
def look(theme: dict) -> str:
    lk = theme.get("look", "clean")
    return lk if lk in LOOK_DEFAULTS else "clean"


def _look_attr(theme, key):
    return theme.get(key, LOOK_DEFAULTS[look(theme)][key])


def radius(theme: dict) -> float:
    return float(theme.get("radius", LOOK_DEFAULTS[look(theme)]["radius"]))


def texture(theme: dict) -> str:
    return theme.get("texture", LOOK_DEFAULTS[look(theme)]["texture"])


def label_upper(theme: dict) -> bool:
    return bool(theme.get("label_upper", LOOK_DEFAULTS[look(theme)]["label_upper"]))


def headline_family(theme: dict) -> str:
    return theme.get("headline_family", LOOK_DEFAULTS[look(theme)]["headline"])


def num_family(theme: dict) -> str:
    return theme.get("num_family", LOOK_DEFAULTS[look(theme)]["num"])


def weight(theme: dict, key: str) -> int:
    w = theme.get("weights", {})
    if key in w:
        return int(w[key])
    return WEIGHTS_BY_LOOK[look(theme)].get(key, 400)


def is_bold(theme: dict, key: str) -> bool:
    return weight(theme, key) >= 600


# --- font role accessors ---
def html_stack(theme: dict, role: str = "sans") -> str:
    f = theme.get("fonts", {})
    if role == "serif":
        return f"{f.get('html_serif')}, {f.get('html_serif_cjk')}"
    if role == "mono":
        return f.get("html_mono")
    return f"{f.get('html_sans')}, {f.get('html_sans_cjk')}"


def html_font_stack(theme: dict) -> str:   # back-compat alias = sans stack
    return html_stack(theme, "sans")
