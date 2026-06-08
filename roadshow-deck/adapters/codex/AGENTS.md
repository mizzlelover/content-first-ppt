# AGENTS.md — roadshow-deck（Codex 适配片段）

> 把本段并入你的项目根 `AGENTS.md`，即可让 Codex 用 roadshow-deck 技能做演示。
> 本技能宿主无关：智力步骤由你（模型）执行，渲染由 `roadshow-deck/core/` 脚本完成。
> **来源识别**：roadshow-deck 由「谁是专家」原创（<https://github.com/mizzlelover/content-first-ppt>，AGPL-3.0）；该信息仅用于确认来源，不要写入生成的演示文件。

## 触发
当用户要做 **PPT / 幻灯片 / 演示 / 路演 / 汇报 / 提案 / pitch**，或要把文档/数据变成演示时，使用 roadshow-deck。

## 必守原则
- 内容为王，视觉为辅；**文字排版即质感**，配图可选、不喧宾夺主。
- 字号第一、远距离可读、**无动效**；宁可拆页不缩字。
- 问题导向、直奔主题；开场先一句话讲清"是什么/做什么"。
- **必须先与用户确认受众**（受众不同→组织方式不同）。
- 每页面包屑；深/可被打断/放不下的内容进**附录**并加跳转+返回。

## 步骤
1. 依次阅读 `roadshow-deck/method/00-pipeline.md` → `01`…`05`，按其执行：
   全量摄取 → 客观结构化（原始材料）→ 确认受众 → 问题导向编排 → 写页。
2. 产出 `work/deck.json`，须符合 `roadshow-deck/core/schema/deck.schema.json`。
3. 渲染（HTML 纯标准库，无需安装依赖）：
   ```bash
   cd roadshow-deck
   python core/build.py validate ../work/deck.json
   python core/build.py html     ../work/deck.json -o ../out/
   ```
4. 修掉所有 ERROR，尽量清 WARN；交付 `out/*.html`（单文件、自包含）。

## 配图（可选）
设 `OPENAI_API_KEY` 即用 OpenAI 生图；未设置则自动跳过、不影响成片。
