# OffsideFence™ 越位电子围栏 · Detailed One-Pager

> **Concept Demonstrator · v0.1.0**
> **概念演示 · v0.1.0**
>
> This is the extended version of [`one-pager.md`](one-pager.md). Use the short version for cards and social media; use this version for partner emails and article openings.
>
> 本文件是 [`one-pager.md`](one-pager.md) 的详细版。短版用于分享卡片和社交媒体，详细版用于合作方邮件和文章开头。

---

## OffsideFence™ 越位电子围栏
## OffsideFence™ — Tactical Behavior Correction System for Forwards

> **让每一次前插，都发生在该发生的位置。**
> *Let every run happen where it should.*

**Tagline / 副标语:** Don't just detect offside. Correct it.
**Official term / 官方术语:** Haptic Tactical Correction (触觉战术纠偏)
**Forum term / 论坛术语:** 电一下

---

### The product concept / 产品概念

OffsideFence is a concept demonstrator for a forward-facing player-wearable that closes the loop between offside detection and offside correction. The pitch perception layer is built conceptually on top of [Roboflow Sports](https://github.com/roboflow/sports), an open-source computer-vision pipeline for football. The hardware layer — a haptic collar — is fictional. The integration layer is deliberately incomplete.

OffsideFence 是一个戴在前锋身上的概念可穿戴设备，把越位检测和越位纠正**闭环**。感知层建立在 [Roboflow Sports](https://github.com/roboflow/sports) 开源管线上。硬件层（触觉项圈）是虚构的。集成层**故意不完整**。

The deliverable of the content project is a 58-second product launch video, designed to make sports-tech practitioners pause and ask: *wait, is this actually a thing?*

内容项目的交付物是一支 58 秒的产品发布视频，目的是让体育科技从业者停下来说一句：*等下，这是真的吗？*

---

### Four operating modes / 4 个模式

The collar has four operating modes. The fourth one is silent by design.

| Mode / 模式 | Threshold / 阈值 | Intensity / 强度 | Failure behavior / 失败行为 |
|-------------|------------------|------------------|---------------------------|
| **Training / 训练** | 15cm beyond last defender | 5% of max, 80ms | Silent on uncertainty |
| **Match / 比赛** | 5cm beyond last defender, ≥99.5% confidence | 35% of max, 60ms | Silent on uncertainty |
| **Darwin / 达尔文** | 5cm, intensity scaled by repeat-offense count | 20–60%, 60–180ms | Intensity held on link loss |
| **Inzaghi Legacy / 因扎吉遗志** | *N/A — no feedback by design* | *N/A* | *N/A — silence is the design* |

Darwin is named for the observation of cumulative calibration in skill learning. Inzaghi Legacy is named for Filippo Inzaghi. It is not a joke. See [`ethics.md`](ethics.md) for the full position.

Darwin 模式以技能学习中的累积校准观察命名。Inzaghi Legacy 以菲利波·因扎吉命名。**这不是段子**。完整立场见 [`ethics.md`](ethics.md)。

---

### Architecture / 系统架构

```
Broadcast Feed (multi-camera, 50p, 1080p+)
        ↓ RTSP / SRT
Pitch Perception Layer (edge / on-prem)
  Player Detection (Roboflow Sports)
  Pitch Keypoints (Roboflow Sports)
  Homography (OpenCV)
        ↓
Tactical State Engine (offside decision, ≤80ms)
        ↓ decision packet (OFP/0.1, 20 bytes)
Haptic Tactical Correction Collar
  Training | Match | Darwin | Inzaghi Legacy
        ↑
Coaching Tablet / Bench Display
```

**End-to-end latency / 端到端延迟:** p50 ≈ 76ms, p99 ≈ 170ms
**Wire format / 传输格式:** 20-byte UDP packet, DTLS 1.3 encrypted
**Reference / 参考实现:** protocol stubs in [`../src/`](../src/), protocol spec in [`../spec/ofp-protocol.md`](../spec/ofp-protocol.md)

---

### Boundary statement / 边界声明

This is a concept demonstrator, not a product. The boundary is held by [`why-this-is-fiction.md`](why-this-is-fiction.md) and [`ethics.md`](ethics.md). The short version:

这是一个概念演示，不是产品。边界由 [`why-this-is-fiction.md`](why-this-is-fiction.md) 和 [`ethics.md`](ethics.md) 守住。短版本：

- ❌ **Not a product.** / 不是产品。
- ❌ **Not affiliated with Roboflow.** / 不是 Roboflow 官方合作。
- ❌ **Not a complete runnable system.** The `src/` tree contains protocol stubs and reference function signatures, not an end-to-end pipeline. / 不是完整的可运行系统。`src/` 目录里只有协议 stub 和函数签名，不是端到端管线。
- ❌ **Not a content series.** There is one video, one launch, no IP expansion. / 不是系列内容。视频只有一支，发布只有一次，没有 IP 扩展。
- ❌ **Not a critique of VAR.** It is a fictional hardware layer that *invents a problem VAR doesn't have*. / 不是对 VAR 的批评。是一个**虚构的硬件层**，发明了一个 VAR 根本没有的问题。
- ❌ **Not bound to specific players.** No event piggybacking, no naming individuals. / 不绑定具体球员。不蹭具体事件、不指名道姓。

**What this repository IS good for / 这个仓库适用于：**

- Reading about how a modern pitch perception pipeline can plausibly be extended toward a player-wearable scenario. / 阅读现代球场感知管线如何向球员可穿戴场景合理扩展。
- Studying the latency budget and decision-packet design considerations of a hypothetical ≤80ms offside decision path. / 研究假想 ≤80ms 越位决策路径的延迟预算和决策包设计。
- Understanding why such a system, even if technically feasible, raises questions that the technical layer alone cannot answer. / 理解为什么这样的系统——即使技术可行——也会提出技术层单独无法回答的问题。
- Enjoying a piece of speculative product design as a creative exercise. / 作为一次创作练习，享受一份推测性产品设计。

---

### The position the artifact takes / 这件作品所持的立场

The offside rule is a human rule, not a measurement problem. A system that mechanically prevents a class of decisions the game has historically permitted is not improving the game — it is removing a decision the game has always had.

越位规则是人类规则，不是测量问题。一个机械地阻止某些历史上被允许的决策的系统，不是在改进比赛——它是在移除一项比赛一直拥有的决策。

The Inzaghi Legacy mode exists to encode this position in the artifact, even in fictional form. The mode is silent *even when the decision is certain*, because the certainty is the wrong thing to act on.

Inzaghi Legacy 模式的存在，是为了把这一立场编码进作品（即使以虚构形式）。即使决策确定，模式保持沉默——因为"确定"恰恰是不该去行动的东西。

---

### Asset index / 资产索引

| Asset / 资产 | Location / 位置 |
|--------------|-----------------|
| Architecture diagram / 架构图 | [`architecture.md`](architecture.md) |
| Operating mode specs / 模式规格 | [`mode-specs.md`](mode-specs.md) |
| Protocol spec (OFP/0.1) / 协议规范 | [`../spec/ofp-protocol.md`](../spec/ofp-protocol.md) |
| White paper (arXiv-style) / 白皮书 | [`../white-paper.md`](../white-paper.md) |
| Press kit / 媒体资料 | [`press-kit.md`](press-kit.md) |
| Source stubs / 源码 stub | [`../src/`](../src/) |

---

### Three-line summary / 三句话收束

1. **It takes a funny football meme and turns it into a complete product world.** / **它把一个好笑的足球梗，变成了一个完整的产品世界。**
2. **It lets you simulate a real product launch at minimal cost.** / **它让你用极低成本模拟了一次真实产品发布。**
3. **It provides a new format prototype: use fictional product launches to train product narrative while producing shareable AI content.** / **它给内容品牌提供了一个新栏目原型：用伪产品发布的方式，训练产品叙事，也制造可传播的 AI 内容。**

---

### Contact / 联系方式

This is a single-author concept project. There is no press team, no partnerships inbox, no support team. For any question that this file does not answer, see the contact link in [`../README.md`](../README.md#contact).

这是一个单人概念项目。没有媒体团队、没有合作邮箱、没有支持团队。如果本文件没有回答你的问题，请看 [`../README.md`](../README.md#contact) 里的联系方式。

---

*License: CC BY-NC 4.0 (documentation). All rights reserved (source stubs). See [LICENSE](../LICENSE).*
*许可证：文档采用 CC BY-NC 4.0。源代码 stub 保留所有权利。详见 [LICENSE](../LICENSE)。*
