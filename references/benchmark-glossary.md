# Agent 基准测试速查表

模型发布图/新闻条目里常见 Agent 能力基准。解释口径：**这些基准测「Agent 干活能力」，不是聊天智商**。

## 终端/代码干活类

| 基准 | 测什么 | 题型/场景 |
|------|--------|----------|
| Terminal Bench 2.1 | 终端操作能力 | 真·命令行环境。给开发任务，agent 自己敲命令、跑脚本、装依赖、改文件、看报错再修。无图形界面。（tbench.ai，harbor 生态） |
| NL2Repo | 自然语言→整个代码仓库 | 给文字需求，生成一整个能跑的代码仓库（多文件、有结构、可执行）。最接近「一句话要一个项目」 |
| DeepSWE | 长周期编码任务 | 真实 GitHub issue → agent 改仓库解决。要读代码、定位、改、跑测试验证，一气呵成干一大段活。（deepswe.net） |
| DSBench-FullStack | 全栈开发（DeepSeek 内部集） | 给需求做完整前后端项目，端到端全栈交付 |
| DSBench-Hard | Coding Agent 难题（DeepSeek 内部集） | FullStack 同家族，专挑硬骨头题 |

## 工具/流程编排类

| 基准 | 测什么 | 题型/场景 |
|------|--------|----------|
| Toolathlon-Verified | 工具调用十项全能 | 三档递进：单工具调用（查日历）→ 多工具串联（预约+通知人）→ 开放场景（只给目标，自己选工具组合路径）。Verified=结果经人工/机器验证。（HKUST-NLP，github.com/hkust-nlp/toolathlon） |
| AutomationBench (Public) | 办公自动化流程 | 多步骤自动化任务（τ-bench 系），按真实业务流程一步步操作完成 |

## 网络安全类

| 基准 | 测什么 | 题型/场景 |
|------|--------|----------|
| Cybergym | 网络安全任务 | 漏洞挖掘/渗透场景，agent 在靶场找漏洞、利用、修复。微软 MDASH 抓漏洞框架也拿这个当标尺。（cybergym.io） |

## 综合专业工作流类

| 基准 | 测什么 | 题型/场景 |
|------|--------|----------|
| Agents' Last Exam (ALE) | 真实专业工作流 | 伯克利牵头、250+ 行业专家、55 子行业、1500+ 任务。测 agent 独立完成「值钱的」专业任务。最难一档——最强模型早期仅 8.6% 通过率。（github.com/rdi-berkeley/agents-last-exam） |

## 速记归类

- **终端/代码干活类**：Terminal Bench、NL2Repo、DeepSWE、DSBench（两个）
- **工具/流程编排类**：Toolathlon、AutomationBench
- **网络安全类**：Cybergym
- **综合专业工作流类**：ALE

## 解释给用户时的格式

「表格 + 一句话归类 + 一句含金量总结」三段式，实测效果好（2026-07-31 V4-Flash 基准表解释，未被纠正）。含金量总结套路：挑涨幅最大的数字（如 DeepSWE 7.3→54.4 涨 7 倍）说明「不是会说话，是能干活的进步」。

## 来源锚点（验证时用）

- Terminal-Bench: https://www.tbench.ai/ + github.com/harbor-framework/terminal-bench
- NL2Repo: github.com/multimodal-art-projection/NL2RepoBench
- DeepSWE: https://deepswe.net/
- Toolathlon: github.com/hkust-nlp/toolathlon（ICLR 2026）
- ALE: github.com/rdi-berkeley/agents-last-exam + agents-last-exam.org
- Cybergym: cybergym.io（微软 MDASH 用其漏洞检测基准）
