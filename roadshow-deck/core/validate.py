# roadshow-deck · 内容为王的路演 PPT 技能 / content-first roadshow PPT skill
# Copyright (C) 2026 谁是专家 (Who-Is-Expert) · https://github.com/mizzlelover
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Semantic + legibility validation for a deck spec (stdlib only).

Encodes the user's first principles as hard checks: large fonts, strong
contrast, one idea per slide, assertion headlines, and valid non-linear jumps.
"""
from __future__ import annotations

import typography as T


def _item_text(it):
    if isinstance(it, str):
        return it
    if isinstance(it, dict):
        return it.get("text", "")
    return str(it)


def _lines(text, w_pt, size_pt):
    if not text:
        return 1
    cpl = max(1, int(w_pt / (size_pt * 1.02)))   # conservative: count wraps, esp. CJK
    return max(1, -(-len(str(text)) // cpl))


def _block_h(b, w, ts):
    """Rough block height in pt — mirrors the renderers, for overflow estimation."""
    t = b.get("type")
    if t == "kpi":
        return 150
    if t in ("compare", "two-col"):
        colw = max(60, (w - 26) / 2 - 48)

        def _colh(c):
            c = c or {}
            items = c.get("items") or ([c.get("text")] if c.get("text") else [])
            body = sum(_lines(_item_text(it), colw, ts["body"]) * ts["body"] * 1.5 for it in items)
            return 44 + body

        return min(340, max(_colh(b.get("left")), _colh(b.get("right"))))
    if t == "process":
        return 140
    if t == "timeline":
        return min(320, 24 + 34 * len(b.get("events", [])))
    if t == "table":
        return min(340, 16 + 36 * (len(b.get("rows", [])) + 1))
    if t == "bullets":
        return max(ts["bullet"] * 1.6,
                   sum(_lines(_item_text(it), w - 34, ts["bullet"]) * ts["bullet"] * 1.5 for it in b.get("items", [])))
    if t == "callout":
        return 28 + _lines(b.get("text", ""), w - 30, ts["callout"]) * ts["callout"] * 1.4
    if t == "paragraph":
        return 12 + _lines(b.get("text", ""), w, ts["body"]) * ts["body"] * 1.5
    if t == "quote":
        return 22 + _lines(b.get("text", ""), w - 30, ts["quote"]) * ts["quote"] * 1.4
    if t == "heading":
        return ts["subhead"] * 1.8
    if t == "image":
        return 240
    if t == "spacer":
        return b.get("height", 16)
    return 60


def validate(deck: dict) -> list:
    issues = []

    def add(level, msg, slide=None):
        issues.append({"level": level, "slide": slide, "msg": msg})

    meta = deck.get("meta", {}) or {}
    if not meta.get("title"):
        add("error", "meta.title 缺失")
    if not meta.get("audience"):
        add("warn", "meta.audience 缺失（受众驱动编排，强烈建议填写）")

    slides = deck.get("slides", []) or []
    if not slides:
        add("error", "slides 为空")
    ids = [s.get("id") for s in slides]
    seen = set()
    for i in ids:
        if i in seen:
            add("error", f"重复的 slide id: {i}")
        seen.add(i)
    idset = set(ids)

    for sec in deck.get("sections", []) or []:
        for sid in sec.get("slides", []):
            if sid not in idset:
                add("error", f"section '{sec.get('id')}' 引用了不存在的 slide '{sid}'")

    # --- theme-level legibility (font floors + contrast) ---
    theme = T.load_theme(meta.get("style") or meta.get("theme") or "minimal")
    ts = theme["type_scale"]
    pal = theme.get("palette", {})
    if ts.get("body", 24) < T.FLOORS["body_error"]:
        add("error", f"正文字号 {ts.get('body')}pt 低于硬下限 {T.FLOORS['body_error']}pt（远距离不可读）")
    elif ts.get("body", 24) < T.FLOORS["body_warn"]:
        add("warn", f"正文字号 {ts.get('body')}pt 偏小，建议 ≥ {T.FLOORS['body_warn']}pt")
    if ts.get("headline", 32) < T.FLOORS["headline_error"]:
        add("error", f"标题字号 {ts.get('headline')}pt 过小")
    if pal.get("text") and pal.get("bg"):
        cr = T.contrast_ratio(pal["text"], pal["bg"])
        if cr < T.LIMITS["min_contrast_large"]:
            add("error", f"正文/背景对比度 {cr}:1 过低（投影不可读）")
        elif cr < T.LIMITS["min_contrast_body"]:
            add("warn", f"正文/背景对比度 {cr}:1 低于 WCAG AA 4.5:1")

    # --- per-slide ---
    has_cover = any(s.get("kind") == "cover" for s in slides)
    if not has_cover:
        add("warn", "缺少封面页(kind=cover)")
    for s in slides:
        sid = s.get("id")
        kind = s.get("kind", "content")
        hl = s.get("headline", "") or ""
        if kind in ("content", "appendix"):
            if not hl:
                add("warn", "内容页缺少断言式标题(headline)——标题应是一句完整论断", sid)
            elif len(hl) > T.LIMITS["max_headline_chars"]:
                add("warn", f"标题过长({len(hl)}字)，建议精简到 ≤ {T.LIMITS['max_headline_chars']} 字", sid)
        blocks = s.get("blocks", []) or []
        if len(blocks) > T.LIMITS["max_blocks_per_slide"]:
            add("warn", f"块数 {len(blocks)} 偏多（建议 ≤ {T.LIMITS['max_blocks_per_slide']}，坚持一页一核心）", sid)
        if kind in ("content", "appendix") and blocks:
            w = T.SLIDE_W_PT - 2 * T.GRID["margin_l"]
            head_lines = _lines(hl, w, ts["headline"])
            head_h = (30 if s.get("tag") else 0) + head_lines * ts["headline"] * 1.25 + (34 if s.get("subhead") else 0)
            need = sum(_block_h(b, w, ts) for b in blocks) + 14 * max(0, len(blocks) - 1)
            avail = T.SLIDE_H_PT - T.GRID["margin_top"] - 26 - head_h - 40 - 36
            if need > avail + 30:
                add("warn", f"内容可能超出版面（预估块高≈{int(need)}pt > 可用≈{int(avail)}pt）——请精简或拆页，勿与页脚重叠", sid)
        for b in blocks:
            if b.get("type") == "bullets":
                items = b.get("items", []) or []
                if len(items) > T.LIMITS["max_bullets"]:
                    add("warn", f"要点 {len(items)} 条偏多（建议 ≤ {T.LIMITS['max_bullets']}）", sid)
                for it in items:
                    txt = _item_text(it)
                    if len(txt) > T.LIMITS["max_bullet_chars"]:
                        add("warn", f"要点过长：“{txt[:16]}…”（建议 ≤ {T.LIMITS['max_bullet_chars']} 字，提炼成关键词）", sid)
        for ln in s.get("links", []) or []:
            if ln.get("target") not in idset:
                add("error", f"非线性跳转目标不存在: {ln.get('target')}", sid)

    for aid in deck.get("appendix", []) or []:
        if aid not in idset:
            add("error", f"appendix 引用不存在的 slide '{aid}'")

    return issues


def format_issues(issues: list) -> str:
    errs = [i for i in issues if i["level"] == "error"]
    warns = [i for i in issues if i["level"] == "warn"]
    if not issues:
        return "✓ 校验通过：未发现问题。"
    lines = [f"校验结果：{len(errs)} 错误, {len(warns)} 警告"]
    for i in errs:
        tag = f"[{i['slide']}] " if i.get("slide") else ""
        lines.append(f"  ✗ ERROR {tag}{i['msg']}")
    for i in warns:
        tag = f"[{i['slide']}] " if i.get("slide") else ""
        lines.append(f"  ! WARN  {tag}{i['msg']}")
    return "\n".join(lines)


def has_errors(issues: list) -> bool:
    return any(i["level"] == "error" for i in issues)
