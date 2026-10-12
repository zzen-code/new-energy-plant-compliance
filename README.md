# 新能源发电站全生命周期合规 Skill

> 一个给 AI Agent 用的**新能源电站合规与技术监督**技能包：从前期审批到退役，覆盖法规体系、31 省"两个细则"、企业安规、技术监督十大专业、设备选型，并以**注册电气工程师（发输变电）**的执业纪律输出——**每条结论必须有条款号背书，没有依据就直接说不行。**

[![Spec](https://img.shields.io/badge/Agent%20Skills-SKILL.md-4D6BFE?style=flat-square)](https://github.com/)
![Jurisdiction](https://img.shields.io/badge/适用法域-中国大陆-important?style=flat-square)
![Baseline](https://img.shields.io/badge/核验基线-2026--10--11-informational?style=flat-square)

---

## English Summary

A compliance & technical-supervision skill for new-energy power plants (wind, PV, solar-thermal, biomass, and battery storage) in **mainland China**, covering the full lifecycle from site approval to decommissioning.

It answers questions such as *what permits are required, which regulation applies, which clause backs a conclusion, what the grid-code assessment parameters are, which standard is currently in force, or what equipment vendors and model designations exist.*

**Design principle:** every conclusion carries a citation (`standard number + clause`, or `regulation + article`) with a verification level (`verified` / `summary-only` / `unconfirmed`). When no basis exists in a currently-effective document, the skill says so plainly instead of guessing.

---

## 为什么需要它

新能源电站的合规判断有三个真实痛点，通用大模型基本都会答错：

| 痛点 | 具体表现 |
|---|---|
| **文件换代快，记忆必错** | GB/T 19963-2011 已于 2025-04-01 废止；GB 20052 已换版至 2024；AQ/T 9007 已改号 YJ/T；"两个细则"近三年连改三轮 |
| **同名文件满天飞** | 国家层面叫"两个细则"，实际由**区域监管局按区域发布**；31 省里只有 6 个真正有省级版本，其余适用区域细则的分省参数表 |
| **网络伪版本泛滥** | 文档分享站存在大量 AI 生成的伪标准文本（如"GB 50150-2024""DL 5027-2024""建标〔2023〕102 号"），内部日期自相矛盾、发布机关张冠李戴 |

这个 skill 的做法是：**不靠记忆，靠核验**。

---

## 三个核心设计

### 1. 核验等级机制

references 中每一条文件都带等级标记，**未核验的不得作为结论引用**：

| 等级 | 含义 |
|---|---|
| `【已核验】` | 打开了官方原文页/公报/官方 PDF |
| `【摘要级】` | 仅搜索结果摘要或第三方转载 |
| `【未确认】` | 未能确认，**只能写成"未确认"，不得当结论** |
| `【已废止/被取代】` | 确认失效，用于提示不要引用 |

### 2. 执业人格：注册电气工程师（发输变电）

技能以注册电气工程师（发输变电方向）的执业身份作答，**七条输出铁律**：

1. **每条结论必须有"名称＋条款号"背书**
2. **没有依据就直接说"不行"**——不用"通常/一般/行业惯例"填补
3. **强制性 / 推荐性分清**——只有 GB（无 /T）、GB 55xxx、DL（无 /T）才能说"必须"；**GB/T、DL/T、NB/T 全部是推荐性标准**（《标准化法》第二条）
4. **标准用词有法定含义**（GB/T 1.1-2020 附录 C）——"必须"不是标准用词
5. **设计依据只有四项**（《建设工程勘察设计管理条例》第二十五条）
6. **无标准可依只有一条合法路径**（同条例第二十九条）
7. **明确执业边界**——不代替现场勘察、行政审批、电网接入评审、律师意见

无依据时的固定输出格式：

```text
【结论】无依据，不能出结论。
【已检索】列出检索过的标准/法规范围
【缺口】缺少什么依据才能判定
【合法路径】走《建设工程勘察设计管理条例》第二十九条，
           或在设计合同中明确约定并由业主承担相应风险
```

### 3. 企业安规优先

用户指定企业时，直接采用该企业的《电力安全工作规程》企业标准（国网 Q/GDW 10799 系列、南网 Q/CSG 510001、华电 Q/CHD 85、国家电投 2023 版、中广核新能源 QB/0001 等），**不跨企业混用**。

---

## 覆盖范围

| 能力域 | 内容 | 文件 |
|---|---|---|
| **法规体系** | 六层体系（法律→行政法规→部门规章→规范性文件→标准→电网规定） | `legal-framework.md` |
| **全流程闸门** | 10 个阶段（前期→核准备案→用地用林用海→环保水保→接入并网→建设→验收→投产→运维→市场→退役） | `lifecycle-gates.md` |
| **"两个细则"** | 31 省现行版本登记表（按 6 个监管区域分组） | `two-rules-by-province.md` |
| **"两个细则"参数** | 六大区域考核与补偿数值＋分省参数表（**算钱用**） | `two-rules-parameters.md` |
| **企业安规** | 国网/南网/五大发电/六小豪门安规体系与分册对应关系 | `enterprise-safety-rules.md` |
| **省级实施细则** | 31 省承接 136 号文的机制电价方案＋25 省竞价结果＋31 省分布式光伏备案口径 | `provincial-implementation.md` |
| **技术监督** | 总导则＋十大专业（绝缘/化学/电测/继保/电能质量/监控自动化/节能/环保/金属/建筑水工） | `technical-supervision.md` |
| **试验标准** | 交接试验、预防性试验、带电检测、安装验收、防雷接地、绝缘工器具、一次设备 | `standards-testing.md` |
| **安全标准** | 安全规程、新能源场站安全规程、特种作业、起重、PPE、职业健康、应急、安全标准化、消防 | `standards-safety.md` |
| **金属与无损检测** | NB/T 47013 全 19 个现行分部、JB/T 4730 取代链、风电部件级检测 | `standards-metal-ndt.md` |
| **设备选型** | 风机/组件/箱变/开关柜/GIS/主变/继保/SVG/AGC/AVC 十类设备的厂商、型号命名规则、参数维度 | `equipment-catalog.md` |
| **风险自查** | 12 类高风险违规点与后果 | `red-flags.md` |
| **核验规程** | 权威查询入口、四步核验法、复核周期、已知陷阱 | `authorities-and-verification.md` |
| **执业人格** | 制度依据、七条铁律、17 个知识模块、法律责任条款、不可引用清单 | `engineer-persona.md` |
| **输出模板** | 合规台账模板（含"未覆盖范围与不确定性"固定章节） | `templates/compliance-ledger.md` |

---

## 目录结构

```text
new-energy-plant-compliance/
├── SKILL.md                              # 入口：执业人格 + 八条核心原则 + 工作流
├── README.md                             # 本文件
├── LICENSE                               # MIT
├── references/
│   ├── legal-framework.md                # 六层法规体系
│   ├── lifecycle-gates.md                # 10 阶段闸门
│   ├── two-rules-by-province.md          # 31 省"两个细则"版本表
│   ├── two-rules-parameters.md           # "两个细则"参数级数值
│   ├── enterprise-safety-rules.md        # 企业安规
│   ├── provincial-implementation.md      # 省级实施细则（电价 + 分布式光伏）
│   ├── technical-supervision.md          # 技术监督十大专业
│   ├── standards-testing.md              # 试验类标准
│   ├── standards-safety.md               # 安全类标准
│   ├── standards-metal-ndt.md            # 金属监督与无损检测
│   ├── standards.md                      # 通用标准清单
│   ├── equipment-catalog.md              # 设备选型索引
│   ├── red-flags.md                      # 12 类高风险违规点
│   ├── authorities-and-verification.md   # 核验规程与权威入口
│   └── engineer-persona.md               # 执业人格与引用纪律
├── templates/
│   └── compliance-ledger.md              # 合规台账输出模板
├── scripts/
│   └── validate_skill.py                 # 结构校验脚本（可本地运行）
└── .github/
    ├── REVIEW_CHECKLIST.md               # 季度复核清单（完整版）
    ├── ISSUE_TEMPLATE/
    │   ├── review-reminder.md            # 手动开复核 issue（定时任务被禁用时的备用）
    │   ├── data-correction.md            # 数据纠错 / 文号失效
    │   └── config.yml                    # Issue 选择页的快捷链接
    └── workflows/
        ├── validate.yml                  # CI：结构校验
        └── quarterly-review.yml          # 定时：创建复核 issue
```

---

## 安装与使用

本 skill 采用通用的 **Agent Skills** 格式（`<name>/SKILL.md` + 资源目录），可被支持该约定的 Agent 工具直接加载。

**方式一：用户级（所有项目可用）**

```bash
# 克隆到用户级 skills 目录
git clone <this-repo> ~/.dsh/skills/new-energy-plant-compliance
# 或 ~/.agents/skills/new-energy-plant-compliance
```

**方式二：项目级（跟随仓库）**

```bash
git clone <this-repo> .agents/skills/new-energy-plant-compliance
```

**方式三：手动放置**

把 `SKILL.md`、`references/`、`templates/` 放到任一被扫描的 skills 根目录下的 `new-energy-plant-compliance/` 中即可。

> **注意**：skill 目录只识别一层（`<root>/<name>/SKILL.md`），不要把目录嵌套得更深。

**使用示例**

```text
帮我查一下山东 100MW 陆上风电项目现在要办哪些手续，依据是什么
```

```text
我们是华电的风电场，检修作业依据哪份安规？考核参数怎么看？
```

```text
GB/T 19963-2011 还是现行标准吗？
```

---

## ⚠️ 数据基线与免责声明

### 数据基线

- **核验基线：2026-10-11**。所有 `【已核验】` 条目均以该日期为快照。
- **法规与标准会变**。电价与电力市场规则变化最快，建议**每季度复核**；标准每半年；法律与行政法规每年。
- 每个文件内都标注了来源 URL 与核验等级，**使用前请按 `references/authorities-and-verification.md` 的四步核验法复核**。

### 免责声明

- 本项目是**检索索引与判断框架**，不是法规汇编，**不构成法律意见**。
- 不替代**执业律师**的法律意见，不替代**注册工程师**的执业判断，不替代主管部门的认定。
- 涉及行政处罚、诉讼、重大投资决策时，请咨询专业人士。
- 厂商型号与技术参数为**快照**，设备换代快，**招标前必须回厂商官网复核**。
- **使用手册（安装/调试/运维）绝大多数是厂商受控文件**，公开渠道无法获取，本项目只提供获取途径。

---

## 仓库自动化

| Workflow | 触发 | 作用 |
|---|---|---|
| `.github/workflows/validate.yml` | push / PR | 校验 SKILL.md 的 frontmatter 合法性、字符数阈值、引用完整性。**专为防止 frontmatter 写错导致技能被静默跳过**（本项目真实踩过：description 里出现未加引号的 `: `，技能直接从加载目录消失） |
| `.github/workflows/quarterly-review.yml` | 每季度（1/4/7/10 月 1 日 01:00 UTC） | 自动创建复核 issue；已存在未关闭的同类 issue 时跳过，不刷屏 |

复核清单见 [`.github/REVIEW_CHECKLIST.md`](.github/REVIEW_CHECKLIST.md)，按"变化速度"排序：电价与市场规则（季度）→ 标准现行状态（半年）→ 法律修订（年度）。

### Issue 模板

| 模板 | 用途 |
|---|---|
| **季度复核** | 手动开复核 issue。**定时任务会被 GitHub 在仓库 60 天无活动后自动禁用**，届时用这个模板手动开 |
| **数据纠错 / 文号失效** | 发现标准换版、文号废止、数值有误，或某条"未确认"已有答案时使用 |

> 纠错模板**强制要求附来源 URL**——这是本仓库的纪律。没有来源的纠错无法采纳。

**本地校验**（无第三方依赖，装不装 PyYAML 都能跑）：

```bash
python scripts/validate_skill.py
```

输出为 GitHub Actions 注解格式（`::error::` / `::warning::`），本地与 CI 行为一致。

---

## 已知缺口

诚实标注，未作推测填补：

| 缺口 | 说明 |
|---|---|
| 西藏 136 号文承接方案 | 公开渠道完全查不到；第三方称"31 省市除西藏外均已发布" |
| 华能 2025 版安规标准号 | 确认存在但编号无法核实 |
| 5 家集团内部安规 | 国家能源集团、三峡、华润、国投、中国节能——公开渠道无集团级安规 |
| JGJ 46-2005 状态、TSG 51—2023 修改单 | 须向住建部/属地市场监管部门索取 |
| 油浸式主变型号字母含义 | 需 JB/T 3837-2025 正文（付费标准） |
| 损耗水平代号 ↔ GB 20052-2024 能效等级对应表 | 缺标准正文，网络来源矛盾 |
| 南方区域新能源功率预测考核 | 在附件 3/4 专项细则，未抓取 |
| 建标〔2023〕102 号 | **住建部官网无此文件**，不得引用 |

---

## 贡献指南

欢迎提交 PR 补充或更新。**发现文号失效、标准换版或数值有误，建议先用 [数据纠错模板](../../issues/new?template=data-correction.md) 提 issue**（模板会引导你填写来源）。

提交 PR 时请遵守本项目的核验纪律：

1. **每条新增/修改必须附来源 URL 与核验等级**（`【已核验】`/`【摘要级】`/`【未确认】`）。
2. **不得凭记忆填写标准号、文号、版本年或日期**——这是本项目最容易被污染的地方。
3. **不得采信文档分享站的"标准文本"**——已多次实证其为 AI 生成伪文本。
4. **区分强制性（GB、DL、GB 55xxx）与推荐性（GB/T、DL/T、NB/T）**。
5. 更新时请一并更新文件内的**核验基线日期**。

优先需要的贡献：
- 上述"已知缺口"中的任意一项
- 各区域"两个细则"的年度参数更新
- 新版标准发布后的替代关系更新

---

## 许可

建议采用 MIT 或 CC BY 4.0（待定，请按需添加 `LICENSE` 文件）。

> 本项目引用的法规、标准文本，其著作权归各自发布机构所有；本项目仅作索引与要点摘录。
