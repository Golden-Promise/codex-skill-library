# skill-context-packet 提示词模板

当你希望 `skill-context-packet` 把下一轮压成一个 minimum context object，而不是去处理完整状态刷新、gate 或 handoff 时，可以使用这些模板。

## 适用触发示例

- `请用 skill-context-packet 把下一轮压缩到 .agent-state/root/PACKET.md。`
- `请为这个子任务写一个紧凑 packet，只保留仍然相关的事实。`
- `把这份状态缩成一个 packet-first 的重启对象，并以一条精确命令结束。`

## 不适用触发示例

- `在继续之前先刷新完整的根任务状态。`
- `为一个子任务打开独立局部状态。`
- `在编辑之前先跑一次高风险改动 gate。`
- `为下一次会话写暂停 handoff。`

## 压缩下一轮

```text
请用 skill-context-packet 压缩下一轮。
写入或刷新 .agent-state/root/PACKET.md 或 .agent-state/subtasks/<slug>/PACKET.md，
只保留目标、收敛后的范围、最小有用输入、
已验证事实、硬约束、风险、退出条件和下一条命令，
并保持边界收敛：只处理 packet compression。
```

## 把膨胀的状态文件重写成 Packet

```text
这份状态文件对下一轮来说太大了。
请把它压缩成面向下一位 owner 的 minimum context object。
删除陈旧细节，只保留下一轮必须知道的内容，
并以精确的下一条命令或 prompt 结束。
不要顺手刷新完整状态，不要跑 gate，也不要生成 handoff。
```
