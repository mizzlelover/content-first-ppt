# 00 · 总流程协议（Pipeline）

> 你（宿主大模型）是这个技能的**大脑**：消化材料、客观结构化、确认受众、问题导向编排、写页，都由你按 `method/` 文档执行。
> `core/` 里的 Python 脚本是**确定性的手**：把你产出的 `deck.json` 渲染成单文件 HTML、做可读性校验、（可选）生图。**绝不要让脚本替你做内容判断。**

## 不可动摇的黄金法则（贯穿全程）
1. **内容为王，视觉为辅**：一切以"把内容组织清楚"为第一目标。视觉是锦上添花。
2. **文字排版本身即质感**：零配图也要做到高质感；配图是可选增强，不喧宾夺主。
3. **字号第一 / 远距离可读**：信任 `core/typography.py` 的字阶；**宁可拆页，也不缩字**。
4. **无动效**：不做任何逐项动画/转场。
5. **问题导向、直奔主题**：开场先消除信息不对称（一句话讲清"是什么/做什么"）。
6. **面包屑必备**：每页显示"现在讲到哪"，小而不缺。
7. **非线性可跳转**：深内容/可能被打断的内容放附录，正文挂"展开"链接，可随时返回。

## 五个阶段（每阶段有产物与"放行条件"）
| 阶段 | 文档 | 产物 | 放行条件 |
|---|---|---|---|
| ① 全量摄取 | `01-ingest.md` | `ingest-ledger.md` | 100% 覆盖，无遗漏 |
| ② 客观结构化 | `02-structure.md` | `source-model.json` | 只整理原始材料、客观、标注缺口 |
| ③ 确认受众 | `03-audience.md` | `audience-profile.json` | **已向用户确认**受众与诉求 |
| ④ 问题导向编排 | `04-narrative.md` | `outline`（章节+页骨架） | 顺序贴合受众、开场消除信息差 |
| ⑤ 写页与渲染 | `05-authoring.md` | `deck.json` → `deck.html` | 通过 `validate`，无 ERROR |

> 建议在一个工作目录（如 `./work/`）里按上表落盘各阶段产物，便于回看与迭代。

## 调用 core（确定性渲染）
```bash
python core/build.py validate work/deck.json          # 可读性/结构硬校验
python core/build.py html     work/deck.json -o out/  # 产出单文件 HTML（-o 可给目录或 .html）
python core/build.py styles                            # 查看风格库与对比度
python core/build.py recommend --domain ai --audience technical --density mid  # 内容→风格推荐
```
- 校验有 **ERROR** 必须先修（字号、对比、跳转目标、结构）。**WARN** 尽量清掉（信息密度/字数）。
- **风格由内容驱动**：用 `recommend` 按领域/受众/数据密度匹配，写回 `meta.style`；信号不足回退 `minimal`。可选 `swiss / editorial / corporate / consulting / minimal / tech / bold`。详见 `06-visual-system.md`。

## 何时打断去问用户
- **阶段③ 必须问**：受众是谁、什么场合、多长时间、专业度、想促成什么决定。
- 材料有重大缺口或自相矛盾时，先问清，不要臆造。

## 最终交付
- `deck.html`（单文件、自包含、可离线放映；逐页自动适配、绝不裁切）——本技能的唯一产物。
