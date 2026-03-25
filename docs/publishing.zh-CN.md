# 发布 codex-skill-library

[English](publishing.md)

这份说明面向 `codex-skill-library` 的仓库级发布、版本和维护流程。

## 适用对象

这份文档是给仓库维护者看的，不是给某个 skill 的普通使用者看的。

## 发布目标

- 保持 `skill-installer` 可用的稳定安装路径
- 让仓库级说明清晰、规范、便于阅读
- 让 skill 包内运行时文档与仓库发布说明分层明确

## 推荐发布流程

1. 检查各个 skill 包 README、仓库索引页和发布文档是否清晰、可发布。
2. 在 [CHANGELOG.md](../CHANGELOG.md) 中更新对读者可见的改动，并确认本次发布的目标 tag。
3. 在打开或合并 PR 之前，先跑完包级测试、eval 测试和连续性种子矩阵。
4. 让 PR checks workflow 再次验证同一组核心包合同和 eval 合同。
5. 在打 tag 之前，先从已推送的发布分支或 `main` 跑一遍安装 smoke test。
6. 分支达到可合并状态后，创建发布 tag 和 GitHub Release。
7. 发布后再对 tag 版本重复一次 smoke test，并记录后续事项。

## 校验命令

仓库中所有已发布包的测试：

```bash
for test_dir in skills/*/tests; do
  python3 -m unittest discover -s "$test_dir" -p 'test_*.py' -v
done
```

`skill-governance` 的额外打包健全性检查：

```bash
(cd skills/skill-governance && python3 scripts/manage_skill.py --validate-only)
```

长任务连续性套件的校验方式：

```bash
python3 -m unittest discover -s evals -p 'test_*.py' -v
python3 evals/run_evals.py
```

套件运行器现在除了仓库形状检查之外，还会按提示词正负向、事件命名空间和严格产物映射来评分。
路由评分还要求已发布的 `SKILL.md` 和 README 中保留触发提示，而可选的 guardrail 字段会以静态元数据合同来校验。

## Pull Request Checks

Pull request 应运行 [.github/workflows/pull-request-checks.yml](../.github/workflows/pull-request-checks.yml)。
这个 workflow 故意保持简单：先跑 `skills/*/tests` 下的包级测试，再跑连续性 eval 单测，最后跑连续性种子矩阵。

## 版本规则

- 使用仓库级 tag，例如 `v0.1.0`、`v0.2.0`、`v1.0.0`
- 向后兼容的增强提升次版本
- 如果包结构或工作流有破坏性变化，则提升主版本
- 对外安装路径尽量保持稳定，例如 `skills/skill-governance`
- 对当前这次长任务连续性发布加固来说，如果没有新的用户可见范围插入，下一次次版本发布应为 `v0.6.0`

## 连续性包的安装 Smoke Test

如果你要对一个“已推送但还没打 tag”的发布分支做 smoke test，请加上 `--ref <branch-name>`，并把安装输出导向隔离的临时目录：

```bash
tmpdir="$(mktemp -d)"

for path in \
  skills/skill-context-keeper \
  skills/skill-phase-gate \
  skills/skill-handoff-summary \
  skills/skill-task-continuity
do
  python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
    --repo Golden-Promise/codex-skill-library \
    --path "$path" \
    --ref <branch-name> \
    --dest "$tmpdir"
done
```

如果你要对当前 `main` 做 smoke test，就使用同一组命令，但去掉 `--ref`：

```bash
tmpdir="$(mktemp -d)"

for path in \
  skills/skill-context-keeper \
  skills/skill-phase-gate \
  skills/skill-handoff-summary \
  skills/skill-task-continuity
do
  python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
    --repo Golden-Promise/codex-skill-library \
    --path "$path" \
    --dest "$tmpdir"
done
```

发布后，再对 tag 版本重复同一组 smoke test：

```bash
tmpdir="$(mktemp -d)"

for path in \
  skills/skill-context-keeper \
  skills/skill-phase-gate \
  skills/skill-handoff-summary \
  skills/skill-task-continuity
do
  python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
    --repo Golden-Promise/codex-skill-library \
    --path "$path" \
    --ref v0.6.0 \
    --dest "$tmpdir"
done
```

如果你要直接检查公开包页面，也可以用 GitHub tree URL，例如：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --url https://github.com/Golden-Promise/codex-skill-library/tree/main/skills/skill-task-continuity
```

## 发布清单

完整的连续性套件发布清单见 [docs/release-checklist-long-task-suite.zh-CN.md](release-checklist-long-task-suite.zh-CN.md)，其中包含打 tag、GitHub Release 和 post-release smoke verification 步骤。

## 维护说明

- 仓库级说明放在根目录 `README.md` 和 `docs/`
- 运行时说明保留在具体 skill 包内部
- 静态套件校验放在 `evals/`，方便维护者在不运行模型的情况下验证触发覆盖、包边界、事件命名空间和产物映射
- 当 `evals/cases.csv` 出现可选列时，把 `max_commands` 视为正整数合同，把 `max_verbosity` 视为 `low` / `medium` / `high` 的元数据检查
- 如果仓库面向公开分享，关键说明建议提供中英文两个版本
