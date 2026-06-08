# roadshow-deck · 内容为王的路演 PPT 技能 / content-first roadshow PPT skill
# Copyright (C) 2026 谁是专家 (Who-Is-Expert) · https://github.com/mizzlelover
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Optional, provider-agnostic image generation — SECONDARY polish only.

The deck MUST be fully usable and high-quality with ZERO generated images.
This module is a no-op unless an API key is configured (graceful degradation).

Default behavior generates TEXT-FREE conceptual imagery; any text is overlaid as
native deck elements, which avoids garbled glyphs (especially CJK) and keeps the
content legible. Backend is auto-selected from environment variables so the same
skill works under whichever host platform the user runs.

SDKs are imported lazily inside each backend, so importing this module never
fails even if no image SDK is installed.

NOTE: exact model identifiers evolve; verify against current provider docs.
"""
from __future__ import annotations

import base64
import os
import pathlib


def available_backend():
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    if os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"):
        return "gemini"
    if os.environ.get("STABILITY_API_KEY"):
        return "stability"
    return None


def _style_prompt(prompt, style=None, need_text=False):
    """Image discipline: the output is MATERIAL to
    embed inside a slide, not a finished slide. Leave room for overlaid text and
    ban the usual AI-image tells."""
    base = (prompt or "").strip()
    parts = []
    if base:
        parts.append(base if base.endswith((".", "。", "!", "?")) else base + ".")
    parts.append("Clean, modern, professional editorial illustration; flat; high-contrast; "
                 "generous negative space so a title or label can be overlaid in the deck.")
    if style:
        parts.append(style.strip().rstrip(".") + ".")
    if not need_text:
        parts.append("Do NOT render any text, letters, numbers, or captions.")
    parts.append("This is an image to EMBED inside a slide, not a finished slide: no header, "
                 "footer, page number, title bar, byline, frame, border, or slide chrome. "
                 "Avoid cartoon, 3D render, neon, glossy SaaS-template look, fake logos, and watermarks. "
                 "Single coherent landscape composition, subject centered within a safe margin. "
                 "If this belongs to a set, keep ratio, scale, margins and line weight consistent with the group.")
    return " ".join(parts)


def _aspect_size(size, backend):
    """Map a 'WxH' request to a size the backend accepts."""
    try:
        w, h = (int(x) for x in str(size).lower().split("x"))
    except Exception:
        w = h = 1024
    landscape, portrait = w > h * 1.1, h > w * 1.1
    if backend == "openai":
        return "1536x1024" if landscape else "1024x1536" if portrait else "1024x1024"
    return f"{w}x{h}"


# --- backends (best-effort; return path on success, None on failure) ------
def _openai(prompt, out_path, size, transparent):
    try:
        from openai import OpenAI
        client = OpenAI()
        kw = dict(model="gpt-image-1", prompt=prompt, size=_aspect_size(size, "openai"))
        if transparent:
            kw["background"] = "transparent"
        r = client.images.generate(**kw)
        data = base64.b64decode(r.data[0].b64_json)
        pathlib.Path(out_path).write_bytes(data)
        return out_path
    except Exception as e:
        print(f"! OpenAI 生图失败：{e}")
        return None


def _gemini(prompt, out_path, size):
    try:
        from google import genai
        client = genai.Client()
        # Model id may change; Imagen / Gemini native image. Verify current docs.
        resp = client.models.generate_images(model="imagen-3.0-generate-002", prompt=prompt)
        img = resp.generated_images[0].image
        data = getattr(img, "image_bytes", None)
        if data is None:
            return None
        pathlib.Path(out_path).write_bytes(data)
        return out_path
    except Exception as e:
        print(f"! Gemini/Imagen 生图失败：{e}")
        return None


def _stability(prompt, out_path, size):
    try:
        import requests
        key = os.environ["STABILITY_API_KEY"]
        r = requests.post(
            "https://api.stability.ai/v2beta/stable-image/generate/core",
            headers={"authorization": f"Bearer {key}", "accept": "image/*"},
            files={"none": ""},
            data={"prompt": prompt, "output_format": "png"},
            timeout=120,
        )
        if r.status_code == 200:
            pathlib.Path(out_path).write_bytes(r.content)
            return out_path
        print(f"! Stability 生图失败：HTTP {r.status_code}")
        return None
    except Exception as e:
        print(f"! Stability 生图失败：{e}")
        return None


def generate(prompt, out_path, size="1536x1024", style=None, transparent=False,
             need_text=False, backend=None):
    """Generate one image. Returns out_path on success, or None (graceful no-op)."""
    backend = backend or available_backend()
    if backend is None:
        return None
    full = _style_prompt(prompt, style, need_text)
    if backend == "openai":
        return _openai(full, out_path, size, transparent)
    if backend == "gemini":
        return _gemini(full, out_path, size)
    if backend == "stability":
        return _stability(full, out_path, size)
    return None


def prefill(deck: dict, out_dir: str, enabled: bool = False) -> int:
    """For image blocks that have a `gen` prompt but no `src`, generate the image
    and set `src`. No-op unless enabled AND a backend key is configured."""
    if not enabled:
        return 0
    backend = available_backend()
    if backend is None:
        print("! 未配置生图 API key（OPENAI_API_KEY 等），跳过配图——不影响成片。")
        return 0
    assets = os.path.join(out_dir, "assets")
    os.makedirs(assets, exist_ok=True)
    n = 0
    for s in deck.get("slides", []) or []:
        for b in s.get("blocks", []) or []:
            gen = b.get("gen") or {}
            if b.get("type") == "image" and not b.get("src") and gen.get("prompt"):
                out_path = os.path.join(assets, f"{s.get('id','s')}_{n}.png")
                r = generate(gen["prompt"], out_path, size=gen.get("size", "1536x1024"),
                             style=gen.get("style"), transparent=gen.get("transparent", False),
                             need_text=gen.get("need_text", False), backend=backend)
                if r:
                    b["src"] = r
                    n += 1
    print(f"✓ 生成配图 {n} 张（backend={backend}）" if n else "未生成配图（无待生成的 image 块）")
    return n
