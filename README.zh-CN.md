# codex-skill-library

[English](README.md)

一个用于集中发布可安装 Codex skills 的仓库。

## 这个仓库适合谁

这个仓库主要面向以下人群：

- 想从一个统一入口安装和浏览 Codex skills 的使用者
- 想先阅读说明，再决定是否采用某个 skill 的读者
- 想维护一套规范、可发布、可持续演进 skill 集合的维护者

## 这里能找到什么

| 区域 | 作用 |
| --- | --- |
| `skills/` | 可单独安装的已发布 skill 包 |
| 包内 `README.md` | 某个 skill 最适合用户开始阅读的入口 |
| 包内 `references/` | 面向读者的示例、说明和双语参考资料 |
| 包内 `docs/` | 某些 skill 需要的维护者发布说明 |

## 当前可用 Skill

| Skill | 适用场景 | 文档 |
| --- | --- | --- |
| `skill-governance` | 用任务式入口治理 skill 资产，包括新增、启用、体检、修复、审计和补文档 | [EN](skills/skill-governance/README.md) / [中文](skills/skill-governance/README.zh-CN.md) |

## 快速开始

1. 先看 [skills/README.zh-CN.md](skills/README.zh-CN.md) 浏览当前可用 skill。
2. 进入具体 skill 包的 `README.md` 了解它是否适合你的场景。
3. 使用 `skill-installer` 进行安装，通常直接安装到默认的 Codex 共享库。
4. 需要更详细示例时，继续阅读该包下的 `references/`。

## 安装示例

从当前仓库安装 `skill-governance`：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-governance
```

固定安装当前发布版本：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-governance \
  --ref v0.5.1
```

也可以直接使用 GitHub tree URL：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --url https://github.com/Golden-Promise/codex-skill-library/tree/main/skills/skill-governance
```

## 阅读入口

- English skill index: [skills/README.md](skills/README.md)
- 中文技能索引: [skills/README.zh-CN.md](skills/README.zh-CN.md)
- `skill-governance` 包说明: [EN](skills/skill-governance/README.md) / [中文](skills/skill-governance/README.zh-CN.md)
- English publishing guide: [docs/publishing.md](docs/publishing.md)
- 中文发布说明: [docs/publishing.zh-CN.md](docs/publishing.zh-CN.md)

## 仓库结构

```text
codex-skill-library/
  README.md
  README.zh-CN.md
  CHANGELOG.md
  docs/
  skills/
    README.md
    README.zh-CN.md
    skill-governance/
```

## 给维护者

仓库级的版本、发布流程和校验说明统一放在 [docs/publishing.zh-CN.md](docs/publishing.zh-CN.md)。
如果你是第一次发布这个仓库，建议先看那份文档，而不是直接从包内运行时说明开始。
