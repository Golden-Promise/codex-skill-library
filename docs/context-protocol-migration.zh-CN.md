# Context Protocol 迁移指南

## 这份文档适合谁

如果你已经熟悉旧版长任务连续性套件，但需要理解这次模型变化，就看这份文档。

如果你属于下面这些情况，可以跳过它：

- 你是第一次直接使用当前六包套件
- 你只需要一个原子包，不关心整个工作流
- 你直接看包内 README，不需要历史桥接说明

## 为什么要改模型

旧版连续性框架是有用的，但它仍然把太多事情都归到“state vs gate vs handoff”里。
这让两个关键能力长期处于弱建模状态：

- 有隔离边界的 child-task context
- 下一轮最小上下文注入

`context protocol` 把这两件事提升成了一等对象。

## 旧模型 vs 新模型

| 旧心智模型 | Context Protocol 中的替代物 |
| --- | --- |
| 只有一份持续膨胀的 task state | 把 `root/` state 和 `subtasks/` state 分开 |
| summary 是主要的连续性对象 | packet 成为默认的 next-turn injection object |
| `skill-phase-gate` 经常像连续性中心 | `skill-phase-gate` 现在只是 optional checkpoint |
| handoff 基本等于扁平的 `.agent-state/HANDOFF.md` | handoff 现在可以作用在 root 或 subtask 范围 |
| orchestration 主要围绕四个包 | 现在是六个包加一套分层 repo layout |

## 包映射关系

### 精神上仍然延续的部分

- `skill-context-keeper`
  - 仍然负责可信的 root-task refresh
  - 现在也显式负责 root-state compression
- `skill-handoff-summary`
  - 仍然负责 continuation-oriented pause artifact
  - 现在同时支持 root 和 subtask scope
- `skill-task-continuity`
  - 仍然负责 bootstrap 和 package routing
  - 现在启动的是分层协议布局，而不是扁平布局

### 新增的一等能力

- `skill-subtask-context`
  - 负责 `.agent-state/subtasks/<slug>/` 下的 bounded child-task state
- `skill-context-packet`
  - 负责 `.agent-state/root/PACKET.md` 或 `.agent-state/subtasks/<slug>/PACKET.md` 下的最小 next-turn packet

### 被刻意收窄的部分

- `skill-phase-gate`
  - 不再充当连续性系统中心
  - 只在 risky work 周围提供 optional operational checkpoint

## 如何采用新的工作流

### 推荐路径

1. 先从 beginner mode 开始。
2. bootstrap `AGENTS.md`、`.agent-state/INDEX.md` 和 `.agent-state/root/`。
3. 继续用 `skill-context-keeper` 做 root-state refresh。
4. 当 root summary 开始嘈杂时，用 `skill-subtask-context` 拆出一个有边界的 child task。
5. 当下一轮不需要整份 state 文件时，用 `skill-context-packet` 写 packet。
6. 只有当 checkpoint 本身真的有价值时，才使用 `skill-phase-gate`。
7. 当工作暂停或换人时，再用 `skill-handoff-summary`。

### Beginner Mode

大多数时候你只需要：

- `.agent-state/INDEX.md`
- `.agent-state/root/TASK_STATE.md`
- `.agent-state/root/PACKET.md`
- `.agent-state/root/HANDOFF.md`

在你真正出现不同 owner、不同 scope 或不同 risk boundary 的 child task 之前，都可以停留在这里。

### Expanded Mode

当下面任意一点成立时，再进入 expanded mode：

- root task 已经带了太多互不相关的局部细节
- 另一位 agent 应该接手一段有边界的工作
- packet-sized continuation 比加载整份 root summary 更合理
- stale detail 已经让 active state 难以阅读

## 常见误区

### 把 Packet 当成 Full State

packet 不是持久的 canonical record。
它是最小 next-turn injection object。
如果你持续把完整历史塞进 packet，就失去了压缩的意义。

### 把 Child-Task 细节继续堆在 Root State 里

如果一个 child task 已经有自己的文件、风险和退出条件，就应该给它自己的 state。
否则 root summary 很快就会变成所有上下文腐烂的地方。

### 继续把 `skill-phase-gate` 当成连续性中心

如果主要问题是 stale state，用 `skill-context-keeper`。
如果主要问题是 bounded child-task isolation，用 `skill-subtask-context`。
如果主要问题是 context budget，用 `skill-context-packet`。

### 工作并未暂停却去写 Handoff

如果工作还在持续，下一轮只是需要一个更小的注入面，那就应该写 packet，而不是 handoff。

## 不变的部分

- 对外安装路径仍然保持在 `skills/<skill-name>/`
- 套件仍然是 repo-first、documentation-first
- 路由边界仍然刻意保持狭窄
- static evals 仍然是维护者的主要回归面

## 快速决策表

| 需要什么 | 用哪个包 |
| --- | --- |
| 刷新主任务图景 | `skill-context-keeper` |
| 打开或刷新 child task | `skill-subtask-context` |
| 把下一轮压成最小上下文 | `skill-context-packet` |
| 为 risky change 加 checkpoint | `skill-phase-gate` |
| 在暂停或转交前留下 durable note | `skill-handoff-summary` |
| 启动套件或决定下一个包 | `skill-task-continuity` |
