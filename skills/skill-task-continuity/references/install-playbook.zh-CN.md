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

1. 先在你的工具环境中安装或引入这个组合包。
2. 选定需要初始化的下游仓库根目录。
3. 先用 dry run 预览文件操作：

```bash
python3 skills/skill-task-continuity/scripts/bootstrap_suite.py --target /path/to/downstream-repo --dry-run
```

4. 确认预览结果正确后，再执行真正的启动：

```bash
python3 skills/skill-task-continuity/scripts/bootstrap_suite.py --target /path/to/downstream-repo
```

5. 只有在你明确要覆盖已有下游文件时，才加上 `--force`。

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
