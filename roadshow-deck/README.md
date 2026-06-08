# roadshow-deck

**内容为王的路演 PPT 技能**（content-first roadshow deck builder）。
把你**自己的材料**，针对**特定受众**，组织成真正能上场的演示——而不是"好看但没信息量"的模板秀。

> 设计理念：PPT 最重要的是「同一份材料面向不同受众的不同组织方式」，且**一切以内容为导向**。
> 视觉是锦上添花，连"美"也主要靠**文字排版的功力**——零配图也应高质感。

## 它和别的 PPT 工具有什么不同
- **算力压在内容上**：先**全量**消化材料（逐字、逐标点、逐图，不遗漏），再**客观结构化**原始材料。
- **受众自适应**：先和你确认受众（大老板/分管/部门经理/集团/外部领导/客户经办/技术…），按侧重重排叙事。
- **问题导向**：开场一句话消除信息不对称，再按"为什么现在/痛点/怎么做/优势/为什么是你/怎么合作/商业模式"展开，顺序随受众变。
- **路演实战导航**：每页**面包屑**（现在讲到哪）+ **非线性附录跳转与返回**（被打断/深挖/正文放不下都不慌）。
- **可读性优先排版**：大字号、强对比、信息密度高、**无动效**；字号比例硬校验。
- **专精单文件 HTML**：自包含、离线放映、可读性优先；**内容超高时逐页自动等比适配、绝不裁切**（不是截图、不依赖 Office）。
- **配图可选**：默认零配图也成立；需要时调生图模型一步到位（provider 无关，无 key 自动跳过）。

## 安装依赖
HTML 渲染与校验**仅用 Python 标准库，零依赖**，无需 `pip install`。（仅可选配图后端需要装包，见末尾。）

## 目录结构
```
roadshow-deck/
├─ SKILL.md            # Claude Code 技能入口（渐进式指引）
├─ README.md           # 本文件（通用说明）
├─ requirements.txt
├─ method/             # 方法论（技能的“大脑”，模型据此执行）
│  ├─ 00-pipeline.md   00 总流程
│  ├─ 01-ingest.md     全量摄取
│  ├─ 02-structure.md  客观结构化（原始材料）
│  ├─ 03-audience.md   确认受众 + 侧重矩阵
│  ├─ 04-narrative.md  问题导向编排
│  ├─ 05-authoring.md  写页（断言+证据）
│  └─ 06-visual-system.md  视觉系统（主题/字体/明暗节奏/配图纪律）
├─ core/               # 确定性渲染（技能的“手”）
│  ├─ schema/deck.schema.json   内容 Spec 契约
│  ├─ build.py         CLI：validate / html / styles / recommend
│  ├─ typography.py    字阶/栅格/对比度（可读性单一事实源）
│  ├─ validate.py      可读性 + 结构硬校验
│  ├─ render_html.py   spec → 单文件 HTML（含逐页自动适配，绝不裁切）
│  └─ styles/          内容驱动的主流风格库 swiss/editorial/corporate/consulting/minimal/tech/bold
├─ adapters/           # 跨 Agent 适配（Codex；Claude Code 由 SKILL.md 原生发现）
└─ examples/           # 样例材料与成片
```

## 快速开始（用样例）
```bash
python core/build.py html examples/sample-source.deck.json -o examples/out
# → examples/out/sample-source.deck.html
python core/build.py styles                                  # 主流风格库（含适配元数据）
python core/build.py recommend --domain data --audience dept-manager --density high   # 内容→风格推荐
```

## 工作流程（推荐让 AI Agent 执行）
1. 读 `method/00-pipeline.md`，按 01→05 阶段执行；
2. 产出符合 `core/schema/deck.schema.json` 的 `deck.json`；
3. `python core/build.py validate deck.json` 过校验；
4. `python core/build.py html deck.json -o out/` 出单文件 HTML。

## 在不同 Agent / CLI 中使用
- **Claude Code**：把 `roadshow-deck/` 放到 `~/.claude/skills/`（个人）或项目 `.claude/skills/`；技能由 `SKILL.md` 自动被发现与触发。
- **OpenAI Codex**：见 `adapters/codex/AGENTS.md`（把其内容并入项目根 `AGENTS.md`）。

## 配图（可选）
设置任一环境变量即启用：`OPENAI_API_KEY` / `GEMINI_API_KEY` / `STABILITY_API_KEY` …。
未设置则**自动跳过配图**，不影响成片。详见 `core/images.py`。

## 设计与调研文档
需求来源、调研与方法论沉淀在**项目仓库**中（安装后的 skill 目录内不含这些文档）。

## 许可证 · License
AGPL-3.0 © 2026 [谁是专家](https://github.com/mizzlelover)
本技能为原创作品；分发或衍生须保留署名并遵循 AGPL-3.0。
