# skill-context-keeper 使用场景

`skill-context-keeper` 只负责维护长任务进行中的结构化状态。
当线程需要可靠地刷新“当前任务图景”时使用它；如果需求是阶段门控或最终交接，就不该由这个包接管。

## Positive Trigger Prompts

- `请使用 skill-context-keeper 刷新当前任务状态，然后我们再继续编码。`
- `根据仓库现状重建当前任务图景，并更新 .agent-state/TASK_STATE.md。`
- `现在的摘要已经过时了，请重建事实、未决风险和下一步动作。`
- `刷新当前任务状态，并延续未完成工作，但不要写成交接说明。`
- `继续实现前，请先把 .agent-state/TASK_STATE.md 更新为包含已验证代码库事实的版本。`

## Negative Trigger Prompts

- `在开始实现前，把这次迁移拆成带检查点的阶段计划。`
- `为下一位接手任务的代理写一份最终交接摘要。`
- `创建 release 检查清单，并决定下一个要通过的阶段门。`
- `准备最终给用户的完成说明，并结束这个任务。`
- `把规划、状态刷新和交接生成都作为一套连续性流程来协调。`

## Refresh Wording Patterns

如果请求的重点就是“刷新状态”，可以直接这样表达：

- `刷新当前任务状态。`
- `更新这个任务的工作状态快照。`
- `根据仓库现状对齐当前摘要，并重写任务状态文件。`
- `在继续实现前，把 .agent-state/TASK_STATE.md 刷新到最新。`

## Facts vs Assumptions vs Decisions Example

以 `.agent-state/TASK_STATE.md` 为例：

- Fact：`tests/test_package_contract.py` 已存在，并会检查两份 use-case 参考文档里都有触发与非触发章节。
- Assumption：由于包内示例路径使用 `.agent-state/TASK_STATE.md`，下游代理会继续沿用这个状态文件位置。
- Decision：这个包只负责状态维护，因此阶段门控和最终交接继续留给同套件中的兄弟包处理。

## Typical Output Shape

这个包通常会刷新一个紧凑的状态产物，例如 `.agent-state/TASK_STATE.md`，内容包括：

- 来自代码库的已验证事实
- 未解决风险与开放问题
- 推荐的下一步动作
- 在宣告完成前仍需补做的验证
