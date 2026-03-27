# skill-context-packet 用例

`skill-context-packet` 用于把下一轮 root 或 subtask 压缩成一个 minimum context object。
当下一位 agent 只该加载最小有用 packet，而不是整份状态文件时，就应该触发它。

## 适用触发示例

- `请用 skill-context-packet 把下一轮压缩到 .agent-state/root/PACKET.md。`
- `请为 parser-cleanup 这个子任务写一个紧凑 packet，只保留仍然相关的事实。`
- `状态文件对下一轮来说太大了，请把它压成 packet-first 的重启对象。`
- `在活跃 owner 之间交接时，只准备 minimum context object，不要重写整个任务。`
- `请更新 packet，让下一位 agent 能从精确的下一条命令开始。`

## 不适用触发示例

- `在继续之前先刷新完整的根任务状态。`
- `为一个新子任务建立局部状态和 merge notes。`
- `在这个高风险多文件改动前先跑 preflight gate。`
- `给下一次会话写暂停 handoff。`
- `在这个仓库里启动整套连续性工具链。`

## Packet 措辞模式

当需求明确是“packet 压缩”时，可以使用这类措辞：

- `把下一轮压成一个 packet。`
- `为下一位 agent 写 minimum context object。`
- `只保留仍然重要的事实、约束和下一条命令。`
- `把这份状态缩成一个 packet-first 的重启说明。`

## 典型输出形态

这个包通常会刷新 `.agent-state/root/PACKET.md` 或 `.agent-state/subtasks/<slug>/PACKET.md`，其中包括：

- 下一轮目标
- 最小有用范围和输入列表
- 值得保留的事实与约束
- 风险、退出条件和下一条命令
