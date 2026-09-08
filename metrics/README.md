# Skill-Bible 分发数据

这里的机制只读取 GitHub 已提供的仓库层面聚合指标，用于判断分发和入口效果；它不是用户行为监控。

## 收集范围

- 仓库 Star、Fork、Watch、Issue；
- Release 数与资源下载量；
- 有效 owner 授权后可读取近 14 天浏览、clone、来源和热门路径。

不会收集或上传用户提示词、材料、文件、输出、账户信息、IP 地址或本地 Skill 调用。

## 运行

不带授权时，脚本只尝试读取 GitHub 公开元数据，并明确标记 owner 指标不可用：

```bash
python3 metrics/collect_github_distribution.py
```

要读取 GitHub Insights 中的流量数据，由仓库 owner 在运行环境中提供有效的 `GITHUB_TOKEN` 或 `SKILL_BIBLE_GITHUB_TOKEN`。Token 不会写入仓库、报告或日志。

## 解释边界

- 浏览、clone、下载是分发信号，不等于安装、调用或用户结果；
- 当前 Skill-Bible 没有收集单个 Skill 的本地调用数据；
- 真实使用与结果数据只应在未来用户主动使用账户型产品或持续服务时，以明示、最小化的产品事件方式记录。
