# 安装操作手册

当下游仓库希望一次性引入整套长任务连续性启动材料时，可以使用这份手册。
这个组合包只负责安装面向下游消费者的模板和说明文档。
不要把它指回公共技能库根目录运行。

## 会引导生成哪些文件

启动脚本会把以下模板复制到下游仓库：

- `AGENTS.md`
- `.agent-state/TASK_STATE.md`
- `.agent-state/HANDOFF.md`
- `.agent-state/DECISIONS.md`
- `.agent-state/RUN_LOG.md`

其中 `TASK_STATE.md` 与 `HANDOFF.md` 是从原子包复制过来的重复模板，这样下游仓库可以从一个包完成初始化，而原子包仍然是这些模板的真实来源。

## 启动流程

1. 先决定安装方式：
   - 只安装 `skill-task-continuity`，先拿到套件入口和 bootstrap 能力
   - 一次安装整套连续性工具链，直接把 4 个包都装好
2. 选定需要初始化的下游仓库根目录。
3. 如果你希望通过自然语言让 Codex 帮你完成初始化，可以直接这样对 Codex 说：

```text
请用 skill-task-continuity 把长任务连续性启动文件引导到 /path/to/downstream-repo。
先预览文件操作，确认无误后再正式写入。
除非我明确要求，否则不要覆盖已有文件。
```

4. 如果你想自己精确控制命令，再先用 dry run 预览文件操作：

```bash
python3 skills/skill-task-continuity/scripts/bootstrap_suite.py --target /path/to/downstream-repo --dry-run
```

5. 确认预览结果正确后，再执行真正的启动：

```bash
python3 skills/skill-task-continuity/scripts/bootstrap_suite.py --target /path/to/downstream-repo
```

6. 只有在你明确要覆盖已有下游文件时，才加上 `--force`。

## 一条命令安装整套工具链

如果你想把 4 个连续性包一次装好，可以直接利用 `skill-installer` 现有的多路径能力：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path \
    skills/skill-context-keeper \
    skills/skill-phase-gate \
    skills/skill-handoff-summary \
    skills/skill-task-continuity
```

如果你需要固定到当前发布版本，再补上 `--ref v0.6.1`。

## 期望的下游布局

```text
AGENTS.md
.agent-state/
  TASK_STATE.md
  HANDOFF.md
  DECISIONS.md
  RUN_LOG.md
```

脚本会自动创建缺失的父目录。
如果不加 `--force`，已有文件会被保留。

## 推荐的首次使用方式

完成启动后：

1. 先阅读下游仓库中的 `AGENTS.md`。
2. 只有当团队确实需要本地辅助提示或示例时，再做轻量调整。
3. 真正执行工作时，仍然直接调用原子技能：
   - `skill-context-keeper`：刷新任务状态
   - `skill-phase-gate`：执行有意义的检查点
   - `skill-handoff-summary`：写暂停或交接摘要

## 可选的仓库本地包装

如果下游仓库需要本地辅助提示，可以放在 `.agents/skills/` 下。
这是一种可选模式，建议保持轻量。
这些文件应该回指原子技能，而不是在仓库里复制出一套分叉的公共文档。
