# roadshow-deck · 内容为王的路演 PPT 技能 / content-first roadshow PPT skill
# Copyright (C) 2026 谁是专家 (Who-Is-Expert) · https://github.com/mizzlelover
# SPDX-License-Identifier: AGPL-3.0-or-later
"""spec -> single self-contained HTML deck (editorial-grade typography).

Visual register drawn from mainstream editorial / Swiss / Carbon design systems:
serif/sans/mono font roles, a weight ladder, mono-tracked labels, hairline rules,
top-border stat cards, light/dark feature rhythm and ghost numerals. Our
principles are kept: NO animation, breadcrumb wayfinding on every body slide,
non-linear appendix jump + return (JS nav stack), large fonts / high contrast /
info density, and a single offline file. Standard library only.
"""
from __future__ import annotations

import base64
import html
import json
import mimetypes
import os

import typography as T

esc = html.escape


def _img_src(src: str) -> str:
    """Inline a local image as a data-URI so the HTML stays self-contained."""
    if not src or src.startswith(("data:", "http://", "https://")):
        return src
    try:
        if os.path.isfile(src):
            mime = mimetypes.guess_type(src)[0] or "image/png"
            b64 = base64.b64encode(open(src, "rb").read()).decode("ascii")
            return f"data:{mime};base64,{b64}"
    except Exception:
        pass
    return src


# --------------------------------------------------------------------------
# CSS
# --------------------------------------------------------------------------
# KPI sizing: one size per group (same-category elements share a size). Scale the
# WHOLE row by its widest value so siblings never differ in size.
_KPI_PX = T.pt_to_px(T.DEFAULT_TYPE_SCALE["kpi_num"])
_KPI_CONTENTW = T.HTML_W_PX - 2 * T.pt_to_px(T.GRID["margin_l"])


def _val_em(s):
    return sum(0.55 if ch.isascii() else 1.0 for ch in str(s)) or 1


def _split_num(v):
    """Split a stat value into (prefix, number, unit) so the unit/prefix can be
    de-emphasized (editorial numeral style). Returns ('', whole, '') when there
    is no numeric core (e.g. 免税 / 千万级 / AAA / 澳门路28号)."""
    v = str(v)
    pre = ""
    i = 0
    if v[:1] in "约≈~+＋-−":
        pre, i = v[0], 1
    j = i
    while j < len(v) and (v[j].isdigit() or v[j] in ".,"):
        j += 1
    if j == i:
        return "", v, ""
    return pre, v[i:j], v[j:]


def _css_vars(theme: dict) -> str:
    p = theme.get("palette", {})
    fp = lambda k: f"{T.font_px(theme, k)}px"
    wt = lambda k: str(T.weight(theme, k))
    v = {
        "bg": p.get("bg", "#0E1A2B"), "surface": p.get("surface", "#16263B"),
        "surface-alt": p.get("surface_alt", "#1E3450"), "text": p.get("text", "#F4F8FC"),
        "muted": p.get("muted", "#A7BACE"), "primary": p.get("primary", "#4A90C2"),
        "accent": p.get("accent", "#E2B23C"), "accent-on": p.get("accent_on", "#15233A"),
        "primary-on": p.get("primary_on", "#FFFFFF"), "line": p.get("line", "#2A3D57"),
        "feature-bg": p.get("feature_bg", p.get("text", "#0A1422")),
        "feature-text": p.get("feature_text", p.get("bg", "#F4F8FC")),
        "ok": p.get("ok", "#3FB68B"), "warn": p.get("warn", "#E0913A"), "bad": p.get("bad", "#D9534F"),
        # Carbon-style role tokens derived without opacity (role greys, not alpha): a lighter
        # "helper" grey for labels/captions, and a subtle surface "tint" for fills.
        "secondary": p.get("muted", "#6E6E6E"),
        "helper": "color-mix(in srgb, var(--muted) 70%, var(--bg))",
        "tint": "color-mix(in srgb, var(--surface) 55%, var(--bg))",
        "font-sans": T.html_stack(theme, "sans"), "font-serif": T.html_stack(theme, "serif"),
        "font-mono": T.html_stack(theme, "mono"),
        "font-head": T.html_stack(theme, T.headline_family(theme)),
        "font-num": T.html_stack(theme, T.num_family(theme)),
        "w-cover": wt("cover_title"), "w-div": wt("section_divider"), "w-head": wt("headline"),
        "w-sub": wt("subhead"), "w-body": wt("body"), "w-kpi": wt("kpi_num"),
        "w-label": wt("label"), "w-quote": wt("quote"), "w-callout": wt("callout"),
        "radius": f"{T.radius(theme)}px",
        "fs-cover-title": fp("cover_title"), "fs-cover-sub": fp("cover_subtitle"),
        "fs-section": fp("section_divider"), "fs-headline": fp("headline"),
        "fs-subhead": fp("subhead"), "fs-body": fp("body"), "fs-bullet": fp("bullet"),
        "fs-kpi": fp("kpi_num"), "fs-kpi-label": fp("kpi_label"),
        "fs-table": fp("table"), "fs-table-h": fp("table_header"),
        "fs-quote": fp("quote"), "fs-callout": fp("callout"),
        "fs-caption": fp("caption"), "fs-tag": fp("tag"),
        "fs-crumb": fp("breadcrumb"), "fs-foot": fp("footer"), "fs-page": fp("pagenum"),
        "pad-x": f"{T.pt_to_px(T.GRID['margin_l'])}px",
        "pad-top": f"{T.pt_to_px(T.GRID['margin_top'])}px",
        "pad-bottom": f"{T.pt_to_px(T.GRID['margin_bottom'])}px",
    }
    return ":root{" + ";".join(f"--{k}:{val}" for k, val in v.items()) + "}"


STATIC_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{height:100%;background:#06080c;overflow:hidden;font-family:var(--font-sans);
  -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
#stage{position:fixed;inset:0;display:flex;align-items:center;justify-content:center}
#deck{width:1280px;height:720px;position:relative;transform-origin:center center;
      background:var(--bg);color:var(--text);overflow:hidden}
.slide{position:absolute;inset:0;display:none;flex-direction:column;
       padding:var(--pad-top) var(--pad-x) var(--pad-bottom) var(--pad-x)}
.slide.active{display:flex}
.slide.feat{background:var(--feature-bg);color:var(--feature-text)}
.slide>*{position:relative;z-index:1}

/* ---- editorial labels (mono, tracked) ---- */
.label{font-family:var(--font-mono);font-weight:var(--w-label);text-transform:uppercase}
.crumbbar{display:flex;align-items:center;gap:12px;flex-wrap:wrap;font-family:var(--font-mono);
  font-size:var(--fs-crumb);font-weight:var(--w-label);letter-spacing:.16em;color:var(--muted);
  border-bottom:1px solid var(--line);padding-bottom:8px;margin-bottom:18px}
.crumb{opacity:.5;white-space:nowrap;text-transform:uppercase}
.crumb.active{opacity:1;color:var(--accent)}
.crumb.appx{opacity:1;color:var(--primary)}
.crumb-dot{opacity:.3}

.head{flex:0 0 auto;margin-bottom:20px}
.kicker{font-family:var(--font-mono);font-weight:var(--w-label);font-size:var(--fs-tag);
  letter-spacing:.22em;text-transform:uppercase;color:var(--accent);margin-bottom:14px;
  display:inline-flex;align-items:center;gap:10px}
.kicker::before{content:"";width:22px;height:2px;background:var(--accent)}
.tag{display:inline-block;font-family:var(--font-mono);font-weight:var(--w-label);font-size:var(--fs-tag);
  letter-spacing:.18em;text-transform:uppercase;color:var(--accent);border:1px solid var(--accent);
  padding:5px 12px;margin-bottom:16px}
.headline{font-family:var(--font-head);font-weight:var(--w-head);font-size:var(--fs-headline);
  line-height:1.16;letter-spacing:-.005em;color:inherit}
.subhead{font-family:var(--font-sans);font-weight:var(--w-sub);font-size:var(--fs-subhead);
  color:var(--secondary);margin-top:12px;line-height:1.4;max-width:46em}
.big,.headline,.sectitle{text-wrap:balance}

/* content body fills the space below the head; .cfit holds the blocks and is the
   unit that auto-scales to fit (see fitSlide() in JS) so nothing is ever clipped. */
.cbody{flex:1 1 auto;display:flex;flex-direction:column;justify-content:center;
         min-height:0;overflow:hidden;font-size:var(--fs-body);line-height:1.5}
.cbody.top{justify-content:flex-start}
.cfit{display:flex;flex-direction:column;gap:20px;width:100%;transform-origin:top left}
p.par{font-size:var(--fs-body);line-height:1.6;color:var(--secondary);max-width:38em}

/* bullets — square marker, no box */
ul.bul{list-style:none;display:flex;flex-direction:column;gap:16px;max-width:42em}
ul.bul>li{position:relative;padding-left:28px;font-size:var(--fs-bullet);line-height:1.5;font-weight:var(--w-body)}
ul.bul>li:before{content:"";position:absolute;left:2px;top:.6em;width:9px;height:9px;background:var(--accent)}
ul.sub{list-style:none;margin-top:8px;display:flex;flex-direction:column;gap:6px}
ul.sub>li{position:relative;padding-left:22px;font-size:calc(var(--fs-bullet)*.84);color:var(--helper)}
ul.sub>li:before{content:"—";position:absolute;left:2px;color:var(--accent)}

/* agenda — numbered outline (no breadcrumb duplication) */
ol.agenda{list-style:none;display:flex;flex-direction:column}
ol.agenda li{display:flex;align-items:baseline;gap:28px;padding:16px 0;border-bottom:1px solid var(--line)}
ol.agenda li:first-child{border-top:1px solid var(--line)}
ol.agenda .n{font-family:var(--font-num);font-weight:var(--w-kpi);font-size:calc(var(--fs-headline)*.9);
  color:var(--accent);line-height:1;font-feature-settings:"tnum";min-width:1.8em}
ol.agenda .t{font-size:var(--fs-subhead);font-weight:600;line-height:1.2}

/* KPI — Carbon stat card: thin accent top-border, mono caps label, big tnum number */
.kpis{display:flex;gap:32px;flex-wrap:wrap;align-items:stretch}
.kpi{flex:1 1 0;min-width:150px;display:flex;flex-direction:column;border-top:2px solid var(--accent);padding-top:16px}
.kpi .num{font-family:var(--font-num);font-weight:var(--w-kpi);font-size:var(--fs-kpi);color:inherit;
  line-height:.9;letter-spacing:-.03em;font-feature-settings:"tnum";white-space:nowrap}
.kpi .num .u{font-size:.42em;font-weight:500;color:var(--helper);margin:0 .04em;letter-spacing:0}
.kpi .lab{font-family:var(--font-mono);font-weight:var(--w-label);font-size:var(--fs-kpi-label);
  letter-spacing:.18em;text-transform:uppercase;color:var(--helper);margin-top:16px;line-height:1.4}
.kpi .delta{font-size:var(--fs-kpi-label);margin-top:6px;color:var(--ok)}

/* table — Carbon hairline rows, flush-left */
table.tbl{width:100%;border-collapse:collapse;font-size:var(--fs-table)}
table.tbl th,table.tbl td{border-bottom:1px solid var(--line);padding:13px 20px;text-align:left;vertical-align:top;line-height:1.45}
table.tbl th:first-child,table.tbl td:first-child{padding-left:0}
table.tbl th:last-child,table.tbl td:last-child{padding-right:0}
table.tbl th{font-family:var(--font-mono);font-weight:700;font-size:var(--fs-table-h);
  letter-spacing:.1em;text-transform:uppercase;color:var(--helper);border-bottom:1.5px solid var(--muted)}
table.tbl td{color:var(--secondary)}
table.tbl td:first-child{color:inherit;font-weight:500}

/* compare / two-col — hairline framed (squared, Swiss) */
.cols{display:flex;gap:24px}
.col{flex:1 1 0;border:1px solid var(--line);padding:24px 26px;background:var(--tint)}
.col h3{font-family:var(--font-sans);font-weight:700;font-size:var(--fs-subhead);margin-bottom:16px;color:inherit}
.col.win{border-top:3px solid var(--accent)}
.col.win h3{color:var(--accent)}
.col ul.bul{gap:12px}
.col ul.bul>li{font-size:calc(var(--fs-body)*.96)}

/* process — numbered steps, hairline top */
.proc{display:flex;gap:24px;align-items:stretch}
.step{flex:1 1 0;border-top:2px solid var(--line);padding-top:16px;display:flex;flex-direction:column;gap:10px}
.step .n{font-family:var(--font-num);font-weight:var(--w-kpi);font-size:calc(var(--fs-headline)*0.92);
  color:var(--accent);line-height:.9;letter-spacing:-.02em;font-feature-settings:"tnum"}
.step .tx{font-size:calc(var(--fs-body)*.94);line-height:1.45;color:var(--secondary)}

/* timeline */
.tl{display:flex;flex-direction:column;gap:14px}
.tl .row{display:flex;gap:18px;align-items:baseline;border-bottom:1px solid var(--line);padding-bottom:12px}
.tl .t{flex:0 0 150px;font-family:var(--font-mono);font-weight:600;letter-spacing:.04em;color:var(--primary)}

/* quote / callout */
blockquote.q{border-left:3px solid var(--accent);padding:4px 24px;font-family:var(--font-head);
  font-weight:var(--w-quote);font-size:var(--fs-quote);line-height:1.45;font-style:italic;color:var(--text)}
.callout{background:var(--tint);border-left:4px solid var(--primary);
  padding:20px 26px;font-size:var(--fs-callout);font-weight:var(--w-callout);line-height:1.5;color:var(--text)}
.callout.highlight{border-left-color:var(--accent)}
.callout.risk,.callout.warn{border-left-color:var(--warn)}
.callout.bad{border-left-color:var(--bad)}

/* image */
.fig{display:flex;flex-direction:column;align-items:center;gap:8px}
.fig img{max-width:100%;max-height:380px;border-radius:var(--radius);border:1px solid var(--line);object-fit:cover}
.fig .ph{width:100%;height:240px;border:1.5px dashed var(--line);border-radius:var(--radius);display:flex;
  align-items:center;justify-content:center;color:var(--muted);font-family:var(--font-mono);
  font-size:var(--fs-caption);letter-spacing:.1em}
.fig .cap{font-family:var(--font-mono);font-size:var(--fs-caption);letter-spacing:.06em;color:var(--muted)}

/* footer: non-linear jump + return + page number */
.footer{flex:0 0 auto;display:flex;align-items:center;gap:12px;margin-top:14px;
        border-top:1px solid var(--line);padding-top:10px}
.jump{font-family:var(--font-mono);font-size:var(--fs-foot);letter-spacing:.1em;color:var(--accent);
  background:transparent;border:1px solid var(--accent);padding:7px 14px;cursor:pointer}
.jump:before{content:"\\2197  "}
.ret{font-family:var(--font-mono);font-size:var(--fs-foot);letter-spacing:.1em;color:var(--accent);
  background:transparent;border:1px solid var(--accent);padding:7px 14px;cursor:pointer}
.ret:before{content:"\\2190  "}
.spacerf{flex:1 1 auto}
.pagenum{font-family:var(--font-mono);font-size:var(--fs-page);letter-spacing:.16em;color:var(--helper)}

/* cover / divider / back (feature slides) */
.slide.cover{justify-content:center;align-items:flex-start}
.cover .big{font-family:var(--font-head);font-weight:var(--w-cover);font-size:var(--fs-cover-title);
  line-height:1.12;letter-spacing:-.015em;max-width:20em}
.cover .cov-rule{width:56px;height:3px;background:var(--accent);margin-top:28px}
.cover .sub{font-family:var(--font-head);font-weight:var(--w-sub);font-size:var(--fs-cover-sub);
  opacity:.82;margin-top:20px;max-width:34em;line-height:1.4}
.cover .metaline{font-family:var(--font-mono);font-size:var(--fs-foot);letter-spacing:.2em;
  text-transform:uppercase;opacity:.55;margin-top:36px}
.slide.back{justify-content:center;align-items:flex-start}
.slide.divider{justify-content:center}
.divider .secidx{font-family:var(--font-num);font-weight:var(--w-div);font-size:var(--fs-cover-sub);
  color:var(--accent);font-feature-settings:"tnum"}
.divider .sectitle{font-family:var(--font-head);font-weight:var(--w-div);font-size:var(--fs-section);
  margin-top:12px;line-height:1.12;letter-spacing:-.01em}
.ghost{position:absolute;right:48px;bottom:-40px;font-family:var(--font-num);font-weight:800;
  font-size:340px;line-height:.8;color:var(--feature-text);opacity:.045;font-feature-settings:"tnum";z-index:0}
.hint{position:fixed;right:14px;bottom:10px;color:#3a4658;font-family:monospace;font-size:12px;z-index:10}

/* page preview / index overlay — toggled with Enter (click a thumb to jump) */
#ov{position:fixed;inset:0;z-index:50;display:none;overflow:auto;background:rgba(6,8,12,.93);
    padding:52px 40px;grid-template-columns:repeat(auto-fill,280px);gap:24px 26px;
    justify-content:center;align-content:start}
body.ov #ov{display:grid}
.ovcell{cursor:pointer}
.ovmini{width:280px;height:157.5px;overflow:hidden;background:var(--bg);border:2px solid #2a3340;border-radius:4px;position:relative}
.ovcell:hover .ovmini,.ovcell.cur .ovmini{border-color:var(--accent)}
.ovmini .slide{position:absolute;left:0;top:0;width:1280px;height:720px;display:flex;
    transform:scale(.21875);transform-origin:top left;pointer-events:none}
.ovnum{margin-top:7px;text-align:center;font-family:var(--font-mono);font-size:13px;color:#9aa6b6;letter-spacing:.08em}
.ovcell.cur .ovnum{color:var(--accent)}
#ovhint{position:fixed;top:16px;left:50%;transform:translateX(-50%);z-index:51;display:none;
    font-family:var(--font-mono);font-size:12px;letter-spacing:.16em;color:#9aa6b6;text-transform:uppercase}
body.ov #ovhint{display:block}
"""


# --------------------------------------------------------------------------
# block rendering
# --------------------------------------------------------------------------
def _t(x):
    return x.get("text", "") if isinstance(x, dict) else str(x)


def _bullets(items):
    out = ["<ul class='bul'>"]
    for it in items:
        if isinstance(it, dict):
            out.append(f"<li>{esc(it.get('text',''))}")
            subs = it.get("sub") or []
            if subs:
                out.append("<ul class='sub'>" + "".join(f"<li>{esc(_t(s))}</li>" for s in subs) + "</ul>")
            out.append("</li>")
        else:
            out.append(f"<li>{esc(str(it))}</li>")
    out.append("</ul>")
    return "".join(out)


def _col(c, win=False):
    title = esc(c.get("title", "")) if isinstance(c, dict) else ""
    cls = "col win" if win else "col"
    inner = ""
    if isinstance(c, dict):
        if c.get("items"):
            inner = _bullets(c["items"])
        elif c.get("text"):
            inner = f"<p class='par'>{esc(c['text'])}</p>"
    return f"<div class='{cls}'><h3>{title}</h3>{inner}</div>"


def render_block(b: dict) -> str:
    t = b.get("type")
    if t == "heading":
        return f"<div class='headline' style='font-size:var(--fs-subhead)'>{esc(b.get('text',''))}</div>"
    if t == "paragraph":
        return f"<p class='par'>{esc(b.get('text',''))}</p>"
    if t == "bullets":
        return _bullets(b.get("items", []))
    if t == "kpi":
        ms = b.get("metrics", [])
        nkpi = max(1, len(ms))
        cardw = (_KPI_CONTENTW - (nkpi - 1) * 30) / nkpi
        cap_em = (cardw * 0.92) / _KPI_PX
        maxw = max((_val_em(m.get("value", "")) for m in ms), default=1) or 1
        scale = max(0.4, min(1.0, cap_em / maxw))
        st = f" style='font-size:calc(var(--fs-kpi)*{scale:.2f})'" if scale < 0.995 else ""
        cards = []
        for m in ms:
            pre, num, suf = _split_num(m.get("value", ""))
            nh = (f"<span class='u'>{esc(pre)}</span>" if pre else "") + esc(num) + (f"<span class='u'>{esc(suf)}</span>" if suf else "")
            delta = f"<div class='delta'>{esc(m.get('delta',''))}</div>" if m.get("delta") else ""
            cards.append(f"<div class='kpi'><div class='num'{st}>{nh}</div>"
                         f"<div class='lab'>{esc(m.get('label',''))}</div>{delta}</div>")
        return f"<div class='kpis'>{''.join(cards)}</div>"
    if t == "table":
        head = "".join(f"<th>{esc(str(c))}</th>" for c in b.get("columns", []))
        body = "".join("<tr>" + "".join(f"<td>{esc(str(c))}</td>" for c in row) + "</tr>" for row in b.get("rows", []))
        return f"<table class='tbl'><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"
    if t == "compare":
        return f"<div class='cols'>{_col(b.get('left',{}), win=True)}{_col(b.get('right',{}))}</div>"
    if t == "two-col":
        return f"<div class='cols'>{_col(b.get('left',{}))}{_col(b.get('right',{}))}</div>"
    if t == "process":
        items = b.get("items", [])
        steps = "".join(f"<div class='step'><span class='n'>{i+1:02d}</span><span class='tx'>{esc(_t(it))}</span></div>"
                        for i, it in enumerate(items))
        return f"<div class='proc'>{steps}</div>"
    if t == "timeline":
        rows = "".join(f"<div class='row'><div class='t'>{esc(e.get('time',''))}</div>"
                       f"<div>{esc(e.get('text',''))}</div></div>" for e in b.get("events", []))
        return f"<div class='tl'>{rows}</div>"
    if t == "quote":
        return f"<blockquote class='q'>{esc(b.get('text',''))}</blockquote>"
    if t == "callout":
        return f"<div class='callout {esc(b.get('variant','info'))}'>{esc(b.get('text',''))}</div>"
    if t == "image":
        cap = f"<div class='cap'>{esc(b.get('caption',''))}</div>" if b.get("caption") else ""
        if b.get("src"):
            return f"<div class='fig'><img src='{esc(_img_src(b['src']))}' alt='{esc(b.get('alt',''))}'>{cap}</div>"
        hint = esc((b.get("gen") or {}).get("prompt", "配图"))
        return f"<div class='fig'><div class='ph'>IMAGE · {hint[:36]}</div>{cap}</div>"
    if t == "spacer":
        return f"<div style='height:{T.pt_to_px(b.get('height',16))}px'></div>"
    return ""


# --------------------------------------------------------------------------
# slide chrome
# --------------------------------------------------------------------------
def _breadcrumb(deck, slide):
    secs = deck.get("sections", []) or []
    if not secs:
        return ""
    cur = slide.get("section")
    is_appx = slide.get("kind") == "appendix" or slide.get("id") in (deck.get("appendix", []) or [])
    parts = []
    for i, sec in enumerate(secs):
        if i:
            parts.append("<span class='crumb-dot'>/</span>")
        active = (sec.get("id") == cur and not is_appx)
        parts.append(f"<span class='{'crumb active' if active else 'crumb'}'>{esc(sec.get('title',''))}</span>")
    if is_appx:
        parts.append("<span class='crumb-dot'>/</span><span class='crumb appx'>附录 · APPENDIX</span>")
    return f"<div class='crumbbar'>{''.join(parts)}</div>"


def _footer(deck, slide, idx, total, target_ids):
    chips = "".join(f"<button class='jump' onclick=\"jump('{esc(ln['target'])}')\">{esc(ln.get('label',''))}</button>"
                    for ln in slide.get("links", []) or [])
    is_target = slide.get("id") in target_ids or slide.get("kind") == "appendix"
    ret = "<button class='ret' onclick='back()'>返回 BACK</button>" if is_target else ""
    is_appx = slide.get("kind") == "appendix" or slide.get("id") in (deck.get("appendix", []) or [])
    pn = "附录 APPENDIX" if is_appx else f"{idx:02d} / {total:02d}"
    return (f"<div class='footer'>{chips}{ret}<div class='spacerf'></div>"
            f"<div class='pagenum'>{pn}</div></div>")


def _render_slide(deck, slide, idx, total, target_ids, tex):
    kind = slide.get("kind", "content")
    sid = esc(slide.get("id", f"s{idx}"))
    meta = deck.get("meta", {})

    if kind == "cover":
        title = esc(slide.get("headline") or meta.get("title", ""))
        sub = esc(slide.get("subhead") or meta.get("subtitle", ""))
        mline = " · ".join(x for x in [meta.get("org"), meta.get("author"), meta.get("date")] if x)
        return (f"<section class='slide cover feat {tex}' id='{sid}'>"
                f"<div class='big'>{title}</div><div class='cov-rule'></div><div class='sub'>{sub}</div>"
                f"<div class='metaline'>{esc(mline)}</div></section>")
    if kind == "back":
        body = "".join(render_block(b) for b in slide.get("blocks", []) or [])
        return (f"<section class='slide back feat {tex}' id='{sid}'>"
                f"<div class='big' style='font-family:var(--font-head);font-weight:var(--w-cover);"
                f"font-size:var(--fs-cover-title);line-height:1.1;letter-spacing:-.02em'>"
                f"{esc(slide.get('headline') or '谢谢')}</div>"
                f"<div class='sub' style='font-size:var(--fs-cover-sub);opacity:.78;margin-top:18px'>"
                f"{esc(slide.get('subhead',''))}</div>{body}</section>")
    if kind == "section-divider":
        sec = next((s for s in deck.get("sections", []) if s.get("id") == slide.get("section")), {})
        num = ""
        for i, s in enumerate(deck.get("sections", []), 1):
            if s.get("id") == slide.get("section"):
                num = f"{i:02d}"
        return (f"<section class='slide divider feat {tex}' id='{sid}'>"
                f"{_breadcrumb(deck, slide)}"
                f"<div class='ghost'>{num}</div>"
                f"<div class='secidx'>{num}</div>"
                f"<div class='sectitle'>{esc(slide.get('headline') or sec.get('title',''))}</div></section>")

    # content / appendix / agenda
    crumb = "" if kind == "agenda" else _breadcrumb(deck, slide)
    if kind == "agenda":
        secs = deck.get("sections", []) or []
        items = "".join(f"<li><span class='n'>{i+1:02d}</span><span class='t'>{esc(s.get('title',''))}</span></li>"
                        for i, s in enumerate(secs))
        blocks_html = f"<ol class='agenda'>{items}</ol>"
        headline = slide.get("headline") or "目录"
    else:
        blocks_html = "".join(render_block(b) for b in slide.get("blocks", []) or [])
        headline = slide.get("headline", "")
    tag = f"<div class='kicker'>{esc(slide.get('tag'))}</div>" if slide.get("tag") else ""
    sub = f"<div class='subhead'>{esc(slide.get('subhead'))}</div>" if slide.get("subhead") else ""
    return (f"<section class='slide' id='{sid}'>{crumb}"
            f"<div class='head'>{tag}<h1 class='headline'>{esc(headline)}</h1>{sub}</div>"
            f"<div class='cbody'><div class='cfit'>{blocks_html}</div></div>"
            f"{_footer(deck, slide, idx, total, target_ids)}</section>")


JS = """
var IDS = __IDS__;
var stack = [];
function curIdx(){var s=document.querySelector('.slide.active');return s?IDS.indexOf(s.id):0;}
/* auto-fit: scale a slide's content block down ONLY if it would overflow, so the
   deck never clips. Slides that fit keep their full (research-grounded) type size. */
function fitSlide(el){if(!el)return;var cb=el.querySelector('.cbody');if(!cb)return;
  var cf=cb.querySelector('.cfit');if(!cf)return;cf.style.transform='';cb.classList.remove('top');
  var avail=cb.clientHeight,need=cf.scrollHeight;
  if(need>avail+0.5){cb.classList.add('top');cf.style.transform='scale('+Math.max(0.5,avail/need).toFixed(4)+')';}}
function show(i){if(i<0||i>=IDS.length)return;document.querySelectorAll('.slide').forEach(function(el){el.classList.remove('active');});
  var el=document.getElementById(IDS[i]);el.classList.add('active');fitSlide(el);history.replaceState(null,'','#'+IDS[i]);}
function goId(id){var i=IDS.indexOf(id);if(i>=0)show(i);}
function jump(id){stack.push(IDS[curIdx()]);goId(id);}   /* non-linear: remember origin */
function back(){if(stack.length){goId(stack.pop());}}     /* return to where you jumped from */
function next(){show(curIdx()+1);}
function prev(){show(curIdx()-1);}
var OV=document.getElementById('ov');
function buildOv(){
  if(OV.dataset.built)return;
  IDS.forEach(function(id,i){
    var cell=document.createElement('div');cell.className='ovcell';cell.dataset.i=i;
    var mini=document.createElement('div');mini.className='ovmini';
    var clone=document.getElementById(id).cloneNode(true);clone.removeAttribute('id');
    mini.appendChild(clone);
    var num=document.createElement('div');num.className='ovnum';num.textContent=(i+1)+' / '+IDS.length;
    cell.appendChild(mini);cell.appendChild(num);
    cell.addEventListener('click',function(){var k=+this.dataset.i;closeOv();show(k);});
    OV.appendChild(cell);
  });
  OV.dataset.built='1';
}
function markCur(){var c=curIdx();OV.querySelectorAll('.ovcell').forEach(function(el){el.classList.toggle('cur',+el.dataset.i===c);});}
function openOv(){buildOv();markCur();document.body.classList.add('ov');var c=OV.querySelector('.ovcell.cur');if(c)c.scrollIntoView({block:'center'});}
function closeOv(){document.body.classList.remove('ov');}
function toggleOv(){document.body.classList.contains('ov')?closeOv():openOv();}
document.addEventListener('keydown',function(e){
  if(e.key==='Enter'){e.preventDefault();toggleOv();return;}
  if(e.key==='Escape'){closeOv();return;}
  if(document.body.classList.contains('ov'))return;
  if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' '){e.preventDefault();next();}
  else if(e.key==='ArrowLeft'||e.key==='PageUp'){e.preventDefault();prev();}
  else if(e.key==='Home'){show(0);}else if(e.key==='End'){show(IDS.length-1);}
  else if(e.key==='Backspace'){e.preventDefault();back();}
});
function fit(){var d=document.getElementById('deck');var s=Math.min(window.innerWidth/1280,window.innerHeight/720);
  d.style.transform='scale('+s+')';}
window.addEventListener('resize',fit);
window.addEventListener('load',function(){fit();var h=location.hash.slice(1);if(h&&IDS.indexOf(h)>=0)goId(h);else show(0);});
"""


def render(deck: dict, theme: dict = None) -> str:
    meta = deck.get("meta", {})
    theme = theme or T.load_theme(meta.get("style") or meta.get("theme") or "minimal")
    tex = ""   # no feature-slide background texture (grid/dot removed per user preference)
    slides = deck.get("slides", []) or []
    total = len(slides)
    target_ids = set()
    for s in slides:
        for ln in s.get("links", []) or []:
            target_ids.add(ln.get("target"))

    body = "".join(_render_slide(deck, s, i + 1, total, target_ids, tex) for i, s in enumerate(slides))
    ids = json.dumps([s.get("id") for s in slides], ensure_ascii=False)
    js = JS.replace("__IDS__", ids)
    title = esc(meta.get("title", "Deck"))
    return (
        "<!doctype html><html lang='" + esc(meta.get("language", "zh")) + "'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<title>{title}</title><style>{_css_vars(theme)}{STATIC_CSS}</style></head>"
        f"<body><div id='stage'><div id='deck'>{body}</div></div>"
        "<div id='ov'></div><div id='ovhint'>选择页面 · Enter / Esc 关闭</div>"
        "<div class='hint'>← → 翻页 · Enter 索引 · Backspace 返回</div>"
        f"<script>{js}</script></body></html>"
    )
