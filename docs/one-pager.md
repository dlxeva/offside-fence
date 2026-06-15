# OffsideFence™ 越位电子围栏 · One-Pager

> **Concept Demonstrator · v0.1.0**
> **概念演示 · v0.1.0**

---

## OffsideFence™ 越位电子围栏
## OffsideFence™ — Tactical Behavior Correction System for Forwards

> **让每一次前插，都发生在该发生的位置。**
> *Let every run happen where it should.*

---

A concept demonstrator for a forward-facing wearable that uses real-time computer vision to detect offside positions and delivers **Haptic Tactical Correction** the instant a forward strays beyond the last defender.

In Chinese football fan culture, the device has already been nicknamed: **电一下** — *literally: "a small shock"*.

一个用实时计算机视觉检测越位位置、在球员越过最后一名防守球员瞬间发出**触觉战术纠偏**的概念可穿戴设备。中文球迷已经给它起了名字：**电一下**。

---

### Four operating modes / 4 个模式

| Mode / 模式 | Behavior / 行为 |
|-------------|-----------------|
| **Training / 训练** | Single short pulse at 200ms latency threshold. Low intensity. / 单次短脉冲，200ms 延迟阈值，低强度 |
| **Match / 比赛** | Decision-validated haptic feedback, no false positive > 0.5%. / 决策验证后的触觉反馈，假阳性 < 0.5% |
| **Darwin / 达尔文** | Adaptive intensity curve; intensity tracks repeat-offense count in a match. / 自适应强度曲线，强度跟随本场累计越位次数 |
| **Inzaghi Legacy / 因扎吉遗志** | **No feedback. The collar stays silent. The forward is left to commit the same offside for the seventh time, on purpose, in memoriam.** / **不反馈。项圈保持沉默。前锋被允许再越位一次，故意地，作为纪念。** |

---

### What this is / 它是什么

> A concept demonstrator built conceptually on top of [Roboflow Sports](https://github.com/roboflow/sports), an open-source computer-vision pipeline for football.
>
> **Shell layer** = real AI technology (player detection, pitch keypoints, homography, tactical radar)
> **Reversal layer** = collar + Haptic Tactical Correction
> **Expression layer** = "The deeper AI gets into football, the more we find that some problems are not unsolvable — they are things the player does not want to remember."
>
> 基于 [Roboflow Sports](https://github.com/roboflow/sports) 开源管线的概念演示。
> **壳子层** = 真实 AI 技术（球员检测 / 球场关键点 / 单应性变换 / 战术雷达）
> **反转层** = 项圈 + 触觉战术纠偏
> **表达层** = 「AI 越深入足球，有些问题不是算不出来，是球员本人不想记」

---

### Boundary statement / 边界声明

- ❌ **Not a product.** We are not making this. We are not raising funding. We are not taking pre-orders. / **不是产品。** 不做。不融资。不接受预订
- ❌ **Not affiliated with Roboflow.** Roboflow is referenced as a technology backbone, not a commercial partner. / **不是 Roboflow 官方合作。** Roboflow 是技术背书，不是商业关系
- ❌ **Not a content series.** There is one video, one launch, no IP expansion. / **不量产内容。** 视频只一支，反转爆点只能打一次
- ❌ **Not bound to specific players.** No event piggybacking, no naming individuals. / **不绑定具体球员。** 不蹭具体事件、不指名道姓
- ✅ **Engineered to standard.** First reaction of the top 1% of engineers: "wait, is this real?" / **工程标准做满。** 让前 1% 工程师第一反应"等下，这是真的吗？"
- ✅ **Concept demonstrator.** The repository is documentation + protocol + stubs, not a manufacturable product. / **概念演示。** 仓库是文档 + 协议 + stub，不是可制造产品

---

### One-line positioning / 一句话定位

> A concept demonstrator for a "forward offside correction collar" packaged in the visual register of a real product launch — engineered to make sports-tech practitioners pause and ask whether it is real.
>
> 借 Roboflow sports 开源管线包装的"前锋越位纠正项圈"概念产品，做成正经科技发布会风格的短视频内容。

---

### Three-line summary / 三句话收束

1. **It takes a funny football meme and turns it into a complete product world.** / **它把一个好笑的足球梗，变成了一个完整的产品世界。**
2. **It lets you simulate a real product launch at minimal cost.** / **它让你用极低成本模拟了一次真实产品发布。**
3. **It provides a new format prototype: use fictional product launches to train product narrative while producing shareable AI content.** / **它给内容品牌提供了一个新栏目原型：用伪产品发布的方式，训练产品叙事，也制造可传播的 AI 内容。**

---

### Links / 链接

- 📖 [Why this is fiction](why-this-is-fiction.md) — is this real? / 这是真的吗？
- ⚖️ [Ethics & boundary statement](ethics.md) — the position we take / 我们持什么立场
- 📄 [White paper (arXiv-style)](../white-paper.md) — full technical spec / 完整技术规格
- 🔌 [OFP/0.1 protocol spec](../spec/ofp-protocol.md) — collar wire format / 项圈通信协议
- 💻 [GitHub repository](https://github.com/dlxeva/offside-fence) — source / 源代码
- 📰 [Press kit](press-kit.md) — for media / 给媒体

---

*License: CC BY-NC 4.0 (documentation). All rights reserved (source stubs). See [LICENSE](../LICENSE).*
*许可证：文档采用 CC BY-NC 4.0。源代码 stub 保留所有权利。详见 [LICENSE](../LICENSE)。*
