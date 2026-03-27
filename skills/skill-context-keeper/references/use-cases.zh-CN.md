# skill-context-keeper 使用场景

`skill-context-keeper` 只负责维护可信的 root task state。
当线程需要可靠地刷新根任务图景，或者需要对 root 状态做 compression 时使用它；如果需求是 subtask local state、packet compression、阶段门控或最终交接，就不该由这个包接管。

## 适用触发示例

- `请使用 skill-context-keeper 刷新根任务状态，然后我们再继续编码。`
- `根据仓库现状重建当前根任务图景，并更新 .agent-state/root/TASK_STATE.md。`
- `现在的根任务摘要已经过时了，请重建事实、未决风险和下一步动作。`
- `刷新根任务状态，并延续未完成工作，但不要写成交接说明。`
- `继续实现前，请先把 .agent-state/root/TASK_STATE.md 更新为包含已验证代码库事实和压缩备注的版本。`

## 不适用触发示例

- `在开始实现前，把这次迁移拆成带检查点的阶段计划。`
- `为 parser-cleanup 打开一个拥有独立局部状态的子任务。`
- `把下一轮压成一个很小的 packet，而不是重写整份状态。`
- `为下一位接手任务的代理写一份最终交接摘要。`
- `创建 release 检查清单，并决定下一个要通过的阶段门。`
- `准备最终给用户的完成说明，并结束这个任务。`
- `把规划、状态刷新和交接生成都作为一套连续性流程来协调。`

## “刷新当前任务状态”表达方式

如果请求的重点就是“刷新状态”，可以直接这样表达：

- `刷新根任务状态。`
- `更新这个任务的 root 状态快照。`
- `根据仓库现状对齐当前根任务摘要，并重写任务状态文件。`
- `在继续实现前，把 .agent-state/root/TASK_STATE.md 刷新到最新。`
- `把根任务里已经变旧的细节压进 archive notes，但保留活跃事实。`

## 事实 / 假设 / 决策示例

以 `.agent-state/root/TASK_STATE.md` 为例：

- Fact：`tests/test_package_contract.py` 已存在，并会检查两份 use-case 参考文档里都有触发与非触发章节。
- Assumption：由于包内示例路径使用 `.agent-state/root/TASK_STATE.md`，下游代理会继续沿用这个 root 状态文件位置。
- Decision：这个包只负责 root-state refresh 和 compression，因此 subtask state、packet、阶段门控和最终交接继续留给同套件中的兄弟包处理。

## 常见输出形态

这个包通常会刷新一个紧凑的状态产物，例如 `.agent-state/root/TASK_STATE.md`，内容包括：

- 来自代码库的已验证事实
- 未解决风险与开放问题
- 需要压缩或归档的陈旧细节
- 推荐的下一步动作
- 在宣告完成前仍需补做的验证
