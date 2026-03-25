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

1. 检查 skill 包 README 和仓库级文档是否清晰可读。
2. 在 [CHANGELOG.md](../CHANGELOG.md) 中更新对读者可见的改动。
3. 在每个已发布 skill 包内运行校验和测试。
4. 提交发布状态，并创建如 `v0.1.0` 这样的 Git tag。
5. 推送 tag，并按需创建 GitHub Release。
6. 用真实的 `skill-installer` 命令验证 GitHub 安装流程。

## 校验命令

当前包的校验方式：

```bash
cd skills/skill-governance
python3 scripts/manage_skill.py --validate-only
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

长任务连续性套件的校验方式：

```bash
python3 evals/run_evals.py
python3 -m unittest discover -s evals -p 'test_*.py' -v
```

## 版本规则

- 使用仓库级 tag，例如 `v0.1.0`、`v0.2.0`、`v1.0.0`
- 向后兼容的增强提升次版本
- 如果包结构或工作流有破坏性变化，则提升主版本
- 对外安装路径尽量保持稳定，例如 `skills/skill-governance`

## 安装验证

通过仓库路径验证安装：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-governance
```

通过 GitHub tree URL 验证安装：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --url https://github.com/Golden-Promise/codex-skill-library/tree/main/skills/skill-governance
```

## 维护说明

- 仓库级说明放在根目录 `README.md` 和 `docs/`
- 运行时说明保留在具体 skill 包内部
- 静态套件校验放在 `evals/`，方便维护者在不运行模型的情况下验证触发覆盖和包边界
- 如果仓库面向公开分享，关键说明建议提供中英文两个版本
