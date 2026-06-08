# roadshow-deck · 内容为王的路演 PPT 技能

![License](https://img.shields.io/github/license/mizzlelover/content-first-ppt?style=flat-square)
![Stars](https://img.shields.io/github/stars/mizzlelover/content-first-ppt?style=flat-square)
![Skill](https://img.shields.io/badge/Skill-Agent-111111?style=flat-square)
![Claude Code](https://img.shields.io/badge/Claude%20Code-Supported-6B5B95?style=flat-square)
![Codex](https://img.shields.io/badge/Codex-Supported-222222?style=flat-square)
![Output](https://img.shields.io/badge/Output-single--file%20HTML-0A7CFF?style=flat-square)
![原创](https://img.shields.io/badge/%E5%8E%9F%E5%88%9B-%E8%B0%81%E6%98%AF%E4%B8%93%E5%AE%B6-FF4D00?style=flat-square)

> 🌏 **English version: [README.en.md](./README.en.md)**

一个面向 **Claude Code / Codex** 的 AI Agent 技能：把你**自己的材料**、针对**特定受众**，组织成真正能上台讲的路演演示。**专精产出单文件、自包含的 HTML**（不产出 PPTX）：内建常驻面包屑、非线性附录跳转，内容再多也**逐页自动适配、绝不裁切**。

市面上多数 PPT 工具从"挑一个好看的模板"开始，这个技能从"把内容讲清楚"开始。**内容是内核，视觉是末端**——哪怕零配图，靠文字排版本身也要做到高质感。

> **设计理念**：PPT 最重要的能力，是**同一份材料面向不同受众时的不同组织方式**。
> 所有 PPT 都应以内容为导向，视觉只是锦上添花；内容组织到位，能让人完全忽略视觉表达的好坏。

---

## 30 秒安装

一行命令安装到 Claude Code 和 Codex（推荐）：

```bash
npx skills add mizzlelover/content-first-ppt --skill roadshow-deck -a claude-code -a codex
```

装好后直接对 Agent 说：

```text
帮我把这份材料做成一份路演 PPT，先帮我确认讲给谁听。
```

## 它和别的 PPT 工具有什么不同

- **算力压在内容上**：先**全量**消化材料（逐字、逐标点、逐图，不遗漏），再**客观结构化**原始材料——而不是先套版式。
- **受众自适应**：动手前先和你确认受众（大老板 / 分管 / 部门经理 / 集团 / 外部领导 / 客户经办 / 技术…），按侧重重排叙事顺序，而不只是换措辞。
- **问题导向**：开场一句话消除信息不对称，再按"为什么现在 / 痛点 / 怎么做 / 优势 / 为什么是你 / 怎么合作 / 商业模式"展开，顺序随受众变。
- **路演实战导航**：每页**面包屑**标出"现在讲到哪"，外加**非线性附录跳转 + 返回**——被打断、被要求深挖、内容多到正文放不下都不慌。
- **可读性优先排版**：大字号、强对比、信息密度高、**无动效**；字号比例由脚本硬校验，**宁可拆页也不缩字**。
- **专精单文件 HTML**：一份自包含 `.html`，离线放映、随处可开；**逐页自动适配，内容再多也绝不裁切**（不是把网页截图塞进去）。
- **配图可选**：默认零配图也成立；需要时调生图模型一步到位（provider 无关，无 API key 自动跳过、不影响成片）。

## 安装

### 方式一：一行命令（推荐）

```bash
npx skills add mizzlelover/content-first-ppt --skill roadshow-deck -a claude-code -a codex
```

`-a claude-code -a codex` 表示同时装给这两个平台；去掉则交互式选择。想先看一眼仓库里有哪些 skill：

```bash
npx skills add mizzlelover/content-first-ppt --list
```

### 方式二：把下面这段话发给有 shell 权限的 AI

> 帮我安装 `roadshow-deck` 这个 Claude Code skill。步骤：
> 1. 确保 `~/.claude/skills/` 目录存在（不存在就创建）；
> 2. `git clone https://github.com/mizzlelover/content-first-ppt.git /tmp/cfp`；
> 3. 把 `/tmp/cfp/roadshow-deck` 整个目录拷到 `~/.claude/skills/roadshow-deck`；
> 4. 验证 `~/.claude/skills/roadshow-deck/` 下能看到 `SKILL.md`、`method/`、`core/` 三项；
> 5. 告诉我装好了。

### 方式三：手动命令行

技能本体在仓库的 `roadshow-deck/` 子目录里，把它放进 skills 目录即可：

```bash
git clone https://github.com/mizzlelover/content-first-ppt.git
cp -r content-first-ppt/roadshow-deck ~/.claude/skills/roadshow-deck   # Claude Code（个人级）
# Codex：把 content-first-ppt/roadshow-deck/adapters/codex/AGENTS.md 的内容并入项目根 AGENTS.md
```

HTML 渲染与校验**仅用 Python 标准库，零依赖**——`git clone` 后即可直接生成，无需 `pip install`。（仅当你要用可选的配图功能时才需装对应后端。）

### 触发方式

装好后 Claude Code 会在对话里自动发现并调用它。常见触发说法：

- "帮我把这份材料做成路演 PPT"
- "把这份文档/笔记/数据做成演示文稿"
- "做一份汇报 / 提案 / pitch deck"
- "make a slide deck from this" / "turn this into a presentation"

## 能力

- 🧠 **全量摄取**：逐字、逐标点、逐图消化原始材料，先建客观模型再谈 PPT
- 🎯 **受众侧重矩阵**：同一份材料按受众重排叙事，对上层讲高度与资源，对执行层讲能力与落地
- 🧭 **常驻面包屑**：每页小而不缺地标出当前章节层级
- 🔀 **非线性附录**：正文挂"展开"链接跳到附录详述，并可随时返回原位
- 🔠 **可读性硬校验**：字号阶梯、对比度、跳转目标、结构完整性，有 ERROR 必修
- 🎨 **内容驱动选风格**：从 7 套主流风格里按领域 / 受众 / 数据密度自动匹配，而非固定模板
- 🖼 **可选配图**：OpenAI / Gemini / Stability 等生图后端，provider 无关，默认关闭
- 🛡 **绝不裁切**：内容超高的页自动等比适配到一屏，永远不会切掉底部
- 📄 **单文件交付**：一份自包含 HTML，离线放映、随处可开、便于分发

## 适合 / 不适合

**✅ 合适**：路演 / 融资 pitch / 项目汇报 / 方案提案 / 商业评审 / 把长文档或数据讲给特定的人听

**❌ 不合适**：纯艺术海报、需要逐项动画的发布会舞台秀、不在乎信息密度只要"网页好看"的场景

## 平台支持

| 平台 | 状态 | 说明 |
|------|------|------|
| Claude Code | ✅ 支持 | 放进 skills 目录即自动发现与触发，本版本主力打磨对象 |
| OpenAI Codex | ✅ 支持 | 把 `adapters/codex/AGENTS.md` 并入项目根 `AGENTS.md`；含可选配图流程 |
| 其他 CLI / Agent | ⚪ 暂不官方适配 | 技能本身宿主无关（读文件 + 跑 Python 即可），但当前版本只针对上面两个平台做规范与验证 |

## 工作流程

技能本身是一套结构化协议，Agent 按 `method/` 逐阶段执行（**模型是大脑，`core/` 脚本只是确定性的手**）：

1. **全量摄取** — 逐字逐图消化材料，不遗漏（`method/01-ingest.md`）
2. **客观结构化** — 只整理原始材料、客观、标注缺口（`02-structure.md`）
3. **确认受众** — 向你提问受众与场合，套用侧重矩阵（`03-audience.md`）
4. **问题导向编排** — 按受众排叙事顺序，正文 / 附录分流（`04-narrative.md`）
5. **写页** — 断言式标题 + 证据，产出 `deck.json`（`05-authoring.md`）
6. **视觉系统** — 最后一步、内容驱动地匹配风格 / 字体 / 明暗节奏（`06-visual-system.md`）

随后用确定性脚本校验并渲染：

```bash
python core/build.py validate work/deck.json        # 可读性 + 结构硬校验（先过）
python core/build.py html     work/deck.json -o out/ # 产出单文件 HTML（-o 可给目录或 .html）
python core/build.py styles                          # 查看 7 套风格库与对比度
python core/build.py recommend --domain ai --audience technical --density mid  # 内容→风格推荐
```

## 交付：单文件 HTML

- `out/<name>.html` — 单文件、自包含、可离线放映：`← →` 翻页，`Enter` 调出页面索引快速跳转，`Backspace` 返回，点"展开"跳附录。
- **逐页自动适配**：内容再多也等比缩放到一屏，绝不裁切；大字号、高对比、可读性优先。
- 双击即放映，不依赖 PowerPoint / WPS——便于分发、截图、投屏。

两者由**同一份 `deck.json`** 渲染，内容一致。

## 风格库（内容驱动，不是固定模板）

不让你"先选皮肤"，而是从内容信号（领域 / 语气 / 受众 / 数据密度）自动匹配，可被你覆盖，信号不足回退 `minimal`：

| 风格 | 基调 | 适合 |
|------|------|------|
| `swiss` | 网格 · 无衬线 · 单一强调色 · 发丝线 | 科技 / 工程 / 数据 / 设计 / 产品 |
| `editorial` | 衬线大标题 + 无衬线正文 + 等宽标签，暖色人文 | 人文 / 品牌 / 文化 / 媒体 / 叙事 |
| `corporate` | 深色克制、稳重权威、精炼金点缀 | 商业 / 战略 / 财务 / 管理层 |
| `consulting` | 浅色、蓝灰、图表导向、结构清晰 | 数据 / 分析 / 报告 / 运营 / 研究 |
| `minimal` | 近黑白 + 单一强调、极致留白 | 通用安全、产品、不确定时的默认 |
| `tech` | 深色、冷色青 / 蓝强调、现代产品感 | AI / SaaS / 创业 / 发布 |
| `bold` | 重磅字号、高反差、醒目强调 | 融资 / 营销 / 愿景 / campaign |

## 配图（可选，默认关闭）

只在确有帮助时使用，绝不喧宾夺主。设置任一环境变量即启用：`OPENAI_API_KEY` / `GEMINI_API_KEY` / `STABILITY_API_KEY` …；未设置则**自动跳过配图、不影响成片**。默认生成无文字概念图，文字用原生块叠加以规避乱码。

## 目录结构

```
content-first-ppt/
├── README.md / README.en.md   ← 仓库介绍（中 / 英）
├── LICENSE                     ← AGPL-3.0
├── CONTRIBUTING.md
└── roadshow-deck/              ← 技能本体（装进 ~/.claude/skills/ 的就是它）
    ├── SKILL.md                ← Claude Code 技能入口
    ├── README.md               ← 技能说明
    ├── requirements.txt
    ├── method/                 ← 方法论（技能的"大脑"，模型据此执行）
    ├── core/                   ← 确定性渲染（技能的"手"）：build / validate / HTML 渲染器 / 风格库
    ├── adapters/codex/         ← Codex 接入片段
    └── examples/               ← 样例 deck + 一份可直接打开的成片
```

## FAQ

**为什么专精 HTML、不做 PPTX？**
把算力集中在一种载体上，才能把版式、留白、可读性和"绝不裁切"打磨到位。单文件 HTML 双击即放映、便于分发，Agent 也最容易读、改、验证。需要静态稿时，浏览器"打印为 PDF"即可。

**为什么坚持无动效？**
真实路演（内部会、客户路演）不是发布会舞台，内容一眨眼就该平铺出来，不该一项项飞入。动效在这些场景里是负担。

**没有配图也能用吗？**
能。配图默认关闭，零配图靠文字排版也应达到高质感——这是设计初衷之一。

**能换主题色 / 风格吗？**
能。风格由内容自动推荐，你也可以在 `meta.style` 里指定 7 套之一；想扩主题见 `CONTRIBUTING.md`。

**怎么更新？**
重新跑安装命令，或进入本地 skill 目录 `git pull`。

## 贡献

欢迎 Issue / PR：新风格、补 `method/` 方法论、加校验规则、修排版问题。改动约定见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 许可证 & 作者

**AGPL-3.0** © 2026 [**谁是专家**](https://github.com/mizzlelover)

本技能（含 `method/` 方法论、`core/` 渲染管线与风格库）为原创作品。你可以自由使用、修改、分发，但**衍生作品与通过网络提供服务的版本须同样以 AGPL-3.0 开源并保留署名**。完整条款见 [LICENSE](./LICENSE)。
