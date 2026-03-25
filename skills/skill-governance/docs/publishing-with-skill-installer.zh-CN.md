# 使用 Skill Installer 发布

English version: [publishing-with-skill-installer.md](publishing-with-skill-installer.md)

这份文档面向发布 `skill-governance` 当前包的维护者。
它刻意放在包内 `docs/` 下，而不是 `references/`，避免和运行时技能说明混在一起。

## 适用对象

如果你要把 `skill-governance` 作为一个公开 skill 包来发布，可以从这份文档开始。

## 目标

把当前包发布到 GitHub，并满足这三点：

- 公开仓库里可读性好
- 可以被 `skill-installer` 正常安装
- 发布说明不污染运行时 skill 文档

## 当前仓库中的发布结构

这个包当前发布在多-skill 仓库 `codex-skill-library` 中。

```text
repo-root/
  README.md
  LICENSE
  .gitignore
  CHANGELOG.md
  skills/
    README.md
    skill-governance/
      README.md
      SKILL.md
      docs/
      agents/
      scripts/
      references/
      tests/
```

安装命令：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-governance
```

如果要固定安装当前发布版本，可使用：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-governance \
  --ref v0.5.1
```

## 当前仓库中的根文件

这个仓库已经包含公开发布所需的根目录文件：

- 根目录 `README.md`： [../../../README.md](../../../README.md)
- 根目录 `LICENSE`： [../../../LICENSE](../../../LICENSE)
- 根目录 `.gitignore`： [../../../.gitignore](../../../.gitignore)
- 根目录 `CHANGELOG.md`： [../../../CHANGELOG.md](../../../CHANGELOG.md)
- `skills/README.md`： [../../README.md](../../README.md)

## 版本建议

这个包本身不需要在 `SKILL.md` 里额外维护一个运行时版本字段。
对外发布时，更推荐给整个仓库做版本管理：

- 使用 Git tag，例如 `v0.1.0`、`v0.2.0`、`v1.0.0`
- 在 `CHANGELOG.md` 里记录对读者可见的改动
- 保持安装路径稳定，例如 `skills/skill-governance`
- 如果需要明确的下载节点，可以同步发布 GitHub Releases

推荐的节奏：

- 第一次公开发布可以从 `v0.1.0` 开始
- 向后兼容的功能增强提升次版本
- 工作流或目录布局有破坏性变化时提升主版本

## 发布检查清单

- `SKILL.md` frontmatter 里的 `name` 与目录名一致，并使用连字符命名。
- `agents/openai.yaml` 包含 `display_name`、`short_description` 和 `default_prompt`。
- `references/` 只放运行时读者指南，不放仓库级发布说明。
- 仓库级说明通过 `README.md` 和 `docs/` 提供安装与发布信息。
- 如果按多 skill 仓库发布，建议补齐 `CHANGELOG.md`、`LICENSE` 和 `.gitignore`。
- 发布前移除 `__pycache__/`、`.pyc` 和编辑器生成的杂项文件。
- 执行：

```bash
python3 scripts/manage_skill.py --validate-only
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

## GitHub Tree URL 示例

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --url https://github.com/Golden-Promise/codex-skill-library/tree/main/skills/skill-governance
```
