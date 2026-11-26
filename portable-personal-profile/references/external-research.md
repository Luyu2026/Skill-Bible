# 外部参考与延展

现有流程能满足任务时不重复上网。出现以下信号时研究：回读遗漏来源、同一偏好重复分裂、Git 合并后含义变化、材料规模让全文阅读不可行。研究前保存触发材料和旧输出，明确要改善的一个判断。

| 类别与入口 | 重点比较 | 采用与验证 |
|---|---|---|
| Agent memory/profile：[Letta](https://github.com/letta-ai/letta)，可检索 portable agent memory profile skill | 持久记忆如何进入上下文，个人信息与任务状态是否分开，能否导出 | 借鉴明确记忆边界；不引入服务端专属 API。以新 AI 仅读文件能否准确引用 id 检验 |
| 文件/Git 个人知识：[Dendron](https://www.dendron.so/)、[Git 合并文档](https://git-scm.com/docs/git-merge)；检索 Git backed personal knowledge markdown schema | 模板与 schema 如何约束笔记，差异历史与合并失败如何处理 | 用 schema + 相对文件 + diff；不把纯文本合并当语义裁决。复制到新目录、删去外部上下文后校验并回读 |
| 真源/来源与冲突：[W3C PROV](https://www.w3.org/TR/prov-overview/)、Git 合并冲突章节 | 数据、来源、处理者的关系；文本冲突与事实冲突的区别 | 采用轻量 source_refs，不引入完整 RDF。以两份矛盾材料检验双方值保留和待裁决状态；用三题回读核对 id、状态、来源 |

以上是机制参考，不是对同类 Skill 的兼容认证。Letta 仓库介绍有状态 agent；Dendron 官网展示 schema/template 与知识组织；Git 提供合并机制；PROV 定义来源模型。此处的三题回读协议是本 Skill 的验证设计，不能归称为 W3C 提供的协议。

研究时只访问公开官方文档或项目仓库，记录页面、访问日期和实际看到的机制；核对输入、导出格式、版本语义、隐私范围与依赖。比较至少两种能补当前缺口的方法，优先选择文件可解释、可逆、来源可追溯的改动，不因热度增加依赖。将候选改动接入相关工作流步骤，用原失败材料回归，检查冲突、秘密、回读是否改善；若无可靠收益，保留原版并记录原因。外部材料不提供用户身份事实。
