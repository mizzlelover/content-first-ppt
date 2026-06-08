# 贡献指南 · Contributing

欢迎 Issue 和 PR。这个技能的内核是**内容为王、受众自适应、可读性优先**——任何改动请先不破坏这条主线，再谈视觉与功能。

> English speakers: this guide is in Chinese, but the rules are simple — keep the content-first, audience-adaptive, readability-first core intact; don't let docs reference things the code doesn't have; run `validate` before sending a PR. Issues/PRs in English are welcome.

## 仓库与技能的关系

- 仓库根：`README` / `LICENSE` / `CONTRIBUTING`。
- 技能本体：`roadshow-deck/`（`SKILL.md` + `method/` + `core/` + `adapters/` + `examples/`）。装进 `~/.claude/skills/` 的就是这个子目录。

## 本地跑起来

```bash
cd roadshow-deck                                                  # HTML 渲染与校验零依赖（纯标准库）
python core/build.py validate examples/sample-source.deck.json    # 应输出"校验通过"
python core/build.py html     examples/sample-source.deck.json -o examples/out
```

提交前请确保 `validate` 无 **ERROR**，并尽量清掉 **WARN**。

## 改动约定

- **改流程 / 方法论**：动 `method/*.md`。它们是技能的"大脑"，模型据此执行；新增阶段要同步更新 `00-pipeline.md` 的阶段表。
- **改渲染 / 校验**：动 `core/`。`deck.json` 的契约是 `core/schema/deck.schema.json`——改字段先改 schema，再改 `validate.py` 和 `render_html.py`（唯一渲染器，输出单文件 HTML）。
- **加风格**：在 `core/styles/` 新增 `<id>.json`（参考现有 7 套的字段：palette、fonts 角色、look、fit 适配元数据），并让 `core/styles.py` 的推荐器能命中它。`build.py styles` 应能列出，对比度要达标。
- **加校验规则**：动 `core/validate.py`，并在 `method/` 里说明触发条件与修法。
- **文档别说谎**：`method/`、`README`、`SKILL.md` 引用的命令、字段、目录必须真实存在（例如命令是 `styles` 不是 `themes`，字段是 `meta.style`）。

## 不要破坏的初衷

- 内容为王、视觉为辅；**不要为了配图而配图**，不要把字号改小去硬塞内容。
- **必须先确认受众**；开场先消除信息不对称。
- 常驻面包屑、非线性附录跳转 + 返回、无动效——这些是差异化关键点，请保留。

## PR 流程

1. 从 `main` 切分支；
2. 跑通 `validate` 与 `html`（浏览器逐页检查：无裁切、无元素碰撞）；
3. PR 描述里写清"改了什么、为什么、是否影响 `deck.json` 契约"；
4. 涉及视觉的改动，附上前后对比截图更好。

## 许可证

提交即表示你同意你的贡献以 **AGPL-3.0** 授权。详见 [LICENSE](./LICENSE)。
