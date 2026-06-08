# roadshow-deck · 内容为王的路演 PPT 技能 / content-first roadshow PPT skill
# Copyright (C) 2026 谁是专家 (Who-Is-Expert) · https://github.com/mizzlelover
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Content-driven style selection.

The skill's core is content-first; visual style is auxiliary and is chosen
*after* the content/audience analysis. This module turns content SIGNALS
(domain, tone, audience, data density, keywords) into a recommended style from
the curated mainstream library in styles/. The host model derives the signals
during the pipeline (method/06) and either trusts the recommendation or
overrides meta.style. Standard library only.
"""
from __future__ import annotations

import json

import typography as T


def _aslist(x):
    if x is None:
        return []
    return [x] if isinstance(x, str) else list(x)


def list_styles():
    out = []
    for p in sorted(T.STYLES_DIR.glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        out.append({"id": d.get("name", p.stem), "title": d.get("title", ""),
                    "summary": d.get("summary", ""), "fit": d.get("fit", {})})
    return out


def recommend_style(signals: dict) -> dict:
    """signals keys (all optional):
       domain(s), tone(s), audience, data_density ('low'|'mid'|'high'),
       keywords[list], text(str, raw material/outline to keyword-match).
    Returns {style, rationale, ranked:[{id,score,why}]}."""
    signals = signals or {}
    domains = set(_aslist(signals.get("domains") or signals.get("domain")))
    tones = set(_aslist(signals.get("tones") or signals.get("tone")))
    audience = signals.get("audience")
    dens = signals.get("data_density")
    kws = set(_aslist(signals.get("keywords")))
    text = signals.get("text") or ""

    ranked = []
    for s in list_styles():
        fit = s.get("fit", {})
        score = 0
        why = []
        dm = domains & set(fit.get("domains", []))
        if dm:
            score += 3 * len(dm); why.append("领域:" + ",".join(sorted(dm)))
        tm = tones & set(fit.get("tones", []))
        if tm:
            score += 2 * len(tm); why.append("语气:" + ",".join(sorted(tm)))
        if audience and audience in set(fit.get("audiences", [])):
            score += 2; why.append("受众:" + audience)
        if dens and fit.get("data_density") in (dens, "any"):
            score += 1; why.append("数据密度:" + dens)
        hits = [k for k in fit.get("keywords", []) if k in kws or (text and k in text)]
        if hits:
            score += len(hits); why.append("关键词:" + ",".join(hits[:5]))
        ranked.append({"id": s["id"], "score": score, "why": "; ".join(why)})

    ranked.sort(key=lambda r: -r["score"])
    top = ranked[0]
    if top["score"] == 0:
        return {"style": "minimal", "ranked": ranked,
                "rationale": "内容信号不足，回退到中性的 minimal（可在 meta.style 手动指定）"}
    return {"style": top["id"], "ranked": ranked, "rationale": top["why"] or top["id"]}
