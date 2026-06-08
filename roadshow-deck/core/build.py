#!/usr/bin/env python3
# roadshow-deck · 内容为王的路演 PPT 技能 / content-first roadshow PPT skill
# Copyright (C) 2026 谁是专家 (Who-Is-Expert) · https://github.com/mizzlelover
# SPDX-License-Identifier: AGPL-3.0-or-later
"""roadshow-deck CLI: turn a deck spec (JSON) into a validated single-file HTML deck.

Usage:
  python core/build.py validate <spec.json>
  python core/build.py html     <spec.json> [-o out.html | -o out_dir/]
  python core/build.py styles
  python core/build.py recommend [--domain D --audience A --density low|mid|high --text "..."]
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import typography as T          # noqa: E402
import validate as V            # noqa: E402
import render_html as RH        # noqa: E402


def _load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _run_validation(deck, force):
    issues = V.validate(deck)
    print(V.format_issues(issues))
    if V.has_errors(issues) and not force:
        print("\n存在 ERROR，已中止渲染（加 --force 可强制生成）。", file=sys.stderr)
        return False
    return True


def _maybe_images(deck, out_dir, a):
    """Optional, off by default. Generate images for `image` blocks that have a
    `gen` prompt but no `src`. Graceful no-op without --images or an API key."""
    if not getattr(a, "images", False):
        return
    try:
        import images as IMG
        IMG.prefill(deck, out_dir, enabled=True)
    except Exception as e:
        print(f"! 配图阶段出错（已跳过，不影响成片）：{e}", file=sys.stderr)


def cmd_validate(a):
    deck = _load(a.spec)
    issues = V.validate(deck)
    print(V.format_issues(issues))
    return 1 if V.has_errors(issues) else 0


def cmd_html(a):
    deck = _load(a.spec)
    if not _run_validation(deck, a.force):
        return 1
    out = a.output or os.path.splitext(a.spec)[0] + ".html"
    # -o may be a directory (or end with a separator): write <dir>/<spec>.html into it.
    if a.output and (os.path.isdir(a.output) or a.output.endswith(("/", os.sep))):
        os.makedirs(a.output, exist_ok=True)
        out = os.path.join(a.output, os.path.splitext(os.path.basename(a.spec))[0] + ".html")
    _maybe_images(deck, os.path.dirname(os.path.abspath(out)), a)
    html = RH.render(deck)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ HTML 已生成: {out}  ({len(html)//1024} KB, {len(deck.get('slides', []))} 页)")
    return 0


def cmd_styles(a):
    import styles as STY
    print("风格库（内容驱动选择；视觉为辅）：")
    for s in STY.list_styles():
        th = T.load_theme(s["id"]); pal = th.get("palette", {})
        cr = T.contrast_ratio(pal.get("text", "#000"), pal.get("bg", "#fff"))
        dom = ",".join((s.get("fit") or {}).get("domains", [])[:5])
        print(f"  {s['id']:11} {s.get('title',''):22} 对比{cr:>5}:1  {th.get('mode')}/{T.look(th)}")
        if s.get("summary"):
            print(f"              {s['summary']}")
        if dom:
            print(f"              适合: {dom}")
    return 0


def cmd_recommend(a):
    import styles as STY, json as _json
    sig = {}
    if a.signals:
        with open(a.signals, encoding="utf-8") as f:
            sig = _json.load(f)
    if a.domain:
        sig["domains"] = a.domain
    if a.tone:
        sig["tones"] = a.tone
    if a.audience:
        sig["audience"] = a.audience
    if a.density:
        sig["data_density"] = a.density
    if a.text:
        sig["text"] = a.text
    r = STY.recommend_style(sig)
    print(f"推荐风格 → {r['style']}")
    print(f"理由：{r['rationale']}")
    print("排名：")
    for x in r["ranked"]:
        print(f"  {x['id']:11} score={x['score']:<3} {x['why']}")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="roadshow-deck", description="content-first roadshow deck builder")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, fn in [("validate", cmd_validate), ("html", cmd_html)]:
        sp = sub.add_parser(name)
        sp.add_argument("spec")
        sp.add_argument("-o", "--output")
        sp.add_argument("--force", action="store_true")
        sp.add_argument("--images", action="store_true", help="启用可选配图生成（需 API key；默认关闭）")
        sp.set_defaults(func=fn)
    sub.add_parser("styles").set_defaults(func=cmd_styles)
    sp = sub.add_parser("recommend")
    sp.add_argument("--signals", help="内容信号 JSON 文件路径")
    sp.add_argument("--domain", action="append", help="可重复，如 --domain ai --domain data")
    sp.add_argument("--tone", action="append")
    sp.add_argument("--audience")
    sp.add_argument("--density", choices=["low", "mid", "high"])
    sp.add_argument("--text", help="原始材料/大纲文本（用于关键词匹配）")
    sp.set_defaults(func=cmd_recommend)
    a = p.parse_args(argv)
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())
