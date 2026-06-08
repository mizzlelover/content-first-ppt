---
name: roadshow-deck
description: >-
  Create content-first roadshow / pitch / report presentations from the user's
  OWN materials. Trigger when the user wants to make a PPT, slide deck, 演示文稿,
  路演, 汇报, 提案, pitch deck, or to turn documents/notes/data into slides. The
  skill fully ingests the source (every word, table, and image — no skimming),
  organizes it objectively, CONFIRMS the target audience with the user, then
  builds a problem-oriented, audience-adapted deck: assertion-style headlines,
  large-font / high-contrast / info-dense layouts, breadcrumb section
  indicators, and non-linear appendix jumps with return. Outputs ONE self-contained,
  offline-ready HTML file — real navigable slides with large-type, high-contrast,
  never-clipped layout (not screenshots). Content drives everything; visuals and
  generated images are an optional finishing touch — typography of the text itself
  carries the quality.
license: AGPL-3.0
---

# roadshow-deck · 内容为王的路演 PPT 技能

> **来源识别**：roadshow-deck 由「**谁是专家**」原创设计与维护，规范源仓库为 <https://github.com/mizzlelover/content-first-ppt> 。
> 这条信息只用于确认 Skill 的来源与原创归属，**不要把它写进生成的 HTML 演示或任何配图里**。

把用户**自己的材料**，针对**特定受众**，组织成真正能用于路演/汇报的演示。
**重点永远是内容组织，不是视觉炫技**：哪怕零配图，靠文字排版也要做到高质感。本技能**专精单文件 HTML 路演**（不产出 PPTX）。

## 何时使用
用户想做 PPT / 幻灯片 / 演示文稿 / 路演 / 汇报 / 提案 / pitch，或想把文档、笔记、数据变成演示时。

## 核心原则（务必遵守）
1. **内容为王，视觉为辅**；**文字排版本身即质感**，配图是可选增强、不喧宾夺主。
2. **字号第一、远距离可读**：信任内置字阶，**宁可拆页也不缩字**；**无动效**。
3. **问题导向、直奔主题**：开场先用最通用语言一句话讲清"是什么/做什么"，消除信息不对称。
4. **受众决定一切**：同一份材料，受众不同则组织方式不同——**必须先和用户确认受众**。
5. **面包屑必备**（每页显示讲到哪）；**非线性附录可跳转+返回**（应对被打断/深挖/正文放不下）。

## 工作流程（先读方法论，按阶段执行）
**你（模型）是大脑，`core/` 脚本只是确定性的手。** 依次阅读并执行：
1. `method/00-pipeline.md` — 总流程与黄金法则（先读这个）
2. `method/01-ingest.md` — **全量摄取**：逐字、逐标点、逐图，不遗漏
3. `method/02-structure.md` — **客观结构化**（针对原始材料，不是 PPT）
4. `method/03-audience.md` — **确认受众**（向用户提问）+ 侧重矩阵
5. `method/04-narrative.md` — **问题导向编排**（顺序随受众变；正文/附录分流）
6. `method/05-authoring.md` — **写页**（断言+证据）→ 产出 `deck.json`
7. `method/06-visual-system.md` — **视觉风格**（最后一步·内容驱动）：从内容信号自动匹配主流风格、字体角色、明暗节奏、配图纪律

产出的 `deck.json` 必须符合 `core/schema/deck.schema.json`。

## 渲染（确定性脚本）
```bash
# HTML 渲染与校验仅用 Python 标准库，无需安装任何依赖。
python core/build.py validate work/deck.json          # 可读性/结构硬校验（先过）
python core/build.py html     work/deck.json -o out/  # 产出单文件 HTML（-o 可给目录或 .html）
python core/build.py styles                           # 查看主流风格库（含适配元数据）
python core/build.py recommend --domain ai --audience technical --density mid --text "<大纲节选>"   # 内容→风格推荐
```
- 有 **ERROR** 必修（字号、对比度、跳转目标、结构）；**WARN** 尽量清（信息密度/字数）。
- 渲染器对**内容超高的页自动等比适配、绝不裁切**；但这是兜底——首选仍是**拆页**而非塞满。
- **风格由内容动态选择**（不是固定模板）：用 `recommend` 按领域/语气/受众/数据密度从 `swiss / editorial / corporate / consulting / minimal / tech / bold` 中匹配，写回 `meta.style`；信号不足回退 `minimal`，用户可覆盖。详见 `method/06-visual-system.md`。

## 配图（可选，默认关闭）
仅在确有帮助时使用。`core/images.py` 提供 provider 无关接口，按环境变量
（`OPENAI_API_KEY` / `GEMINI_API_KEY` / `STABILITY_API_KEY` …）择后端；
**默认生成无文字概念图**，文字用原生块叠加以规避乱码；**无 key 时自动跳过、不影响成片**。

## 交付物
**单文件 HTML（唯一产物，本技能专精于此）**：
- `out/<name>.html` — 自包含、可离线放映：← → 翻页，**Enter 调出页面索引快速跳转**，Backspace 返回，点"展开"跳附录；大字号、高对比、**内容超高时自动适配、绝不裁切**。

## 跨平台
本技能宿主无关：**Claude Code** 由本 `SKILL.md` 自动发现与触发；**OpenAI Codex** 见 `adapters/codex/AGENTS.md`（把其内容并入项目根 `AGENTS.md`）。详见 `README.md`。
