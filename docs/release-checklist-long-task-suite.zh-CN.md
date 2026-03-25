# 长任务连续性套件发布清单

[English](release-checklist-long-task-suite.md)

当你要把长任务连续性套件准备到可合并、可打 tag、可发布 GitHub Release 的状态时，请按这份清单执行。

## 1. 发布前基本检查

- 确认工作树干净：`git status --short`
- 确认目标版本仍然是 `v0.6.1`；如果又插入了新的用户可见范围，先重新判断版本再打 tag。
- 重新检查仓库入口和索引页：
  - [README.md](../README.md)
  - [README.zh-CN.md](../README.zh-CN.md)
  - [skills/README.md](../skills/README.md)
  - [skills/README.zh-CN.md](../skills/README.zh-CN.md)
- 确认 [CHANGELOG.md](../CHANGELOG.md) 与本次发布范围一致，没有描述尚未完成的内容。

## 2. 本地校验

运行所有已发布包的测试：

```bash
for test_dir in skills/*/tests; do
  python3 -m unittest discover -s "$test_dir" -p 'test_*.py' -v
done
```

运行 `skill-governance` 的额外打包健全性检查：

```bash
(cd skills/skill-governance && python3 scripts/manage_skill.py --validate-only)
```

运行连续性 eval 检查：

```bash
python3 -m unittest discover -s evals -p 'test_*.py' -v
python3 evals/run_evals.py
```

## 3. 文档与索引核对

- 确认四个连续性包仍然能从根 README 和 `skills/` 索引页找到。
- 确认四个包的职责仍然不重叠：
  - `skill-context-keeper` = 只负责状态刷新
  - `skill-phase-gate` = 只负责检查点
  - `skill-handoff-summary` = 只负责交接摘要
  - `skill-task-continuity` = 只负责套件启动与组合
- 确认各包 `README.md` 里的安装段落仍然指向公开发布路径 `skills/<skill-name>/`。
- 确认发布说明文档仍然链接到这份清单和连续性包的 smoke-test 命令。

## 4. 从已推送分支或 `main` 运行安装 Smoke Test

如果发布分支已经推送到 GitHub，先对这个精确 ref 做 smoke test：

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

如果你想验证当前 `main`，就用同一组命令，但去掉 `--ref`：

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

## 5. PR 就绪检查

- 打开或更新 draft PR。
- 确认 `.github/workflows/pull-request-checks.yml` 在 PR 上通过。
- 确认 PR 标题和摘要仍然准确描述本次发布内容。

## 6. 变更日志与版本确认

- 确认下一次发布仍然是 `v0.6.1`。
- 确认所有固定 tag 的安装示例都使用 `v0.6.1`。
- 确认 `CHANGELOG.md` 已经达到“基本不用再改就能发”的状态。

## 7. 打 Tag 与 GitHub Release

- 合并发布 PR。
- 创建并推送 tag：

```bash
git tag v0.6.1
git push origin v0.6.1
```

- 使用准备好的 release notes draft 创建 GitHub Release。

## 8. 发布后 Tag 版 Smoke Verification

对已发布 tag 再做一遍连续性包安装 smoke test：

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
    --ref v0.6.1 \
    --dest "$tmpdir"
done
```

- 确认 tag 安装解析到预期的包路径。
- 确认 GitHub Release 页面能把读者正确带到 `skills/` 下的四个已发布包。
