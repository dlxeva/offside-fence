# OffsideFence: a fictional player-wearable concept for real-time offside correction

**Author:** OffsideFence Concept (single author, content project)
**Date:** 2026-06-15
**Status:** fictional, single-shot
**License:** CC BY-NC 4.0 (documentation), All Rights Reserved (source stubs)

> **This is a fictional white paper.** It is written in the register of an arXiv-style technical paper so that a reader landing on the project can evaluate the technical plausibility of the concept on its own terms. It is *not* a research contribution, *not* a peer-reviewed submission, and *not* a proposal for a deployable system. See [`why-this-is-fiction.md`](why-this-is-fiction.md) for the boundary.

## Abstract

We describe a fictional concept for a forward-facing player-wearable that uses real-time computer vision to detect offside positions in live football matches and delivers haptic feedback at the moment a forward strays beyond the last defender. The pitch-perception layer is built conceptually on top of [Roboflow Sports](https://github.com/roboflow/sports), an open-source computer-vision pipeline for football. The hardware layer is fictional. The integration is deliberately incomplete. The contribution of this document is not a system — it is a *position statement* on the boundary between a real-time offside measurement and the offside judgment the Laws of the Game require, and a *design artifact* that makes the position inspectable. The most consequential design decision the artifact takes is the inclusion of an `Inzaghi Legacy` operating mode in which the wearable is silent by design, in order to preserve the class of deliberate-early decisions the offside rule has historically permitted.

## 1. Introduction

The Laws of the Game, as administered by the International Football Association Board (IFAB), define offside as a judgment by the assistant referee. The judgment is informed by position, by movement, by intent at the moment the ball is played, and by a discretionary tolerance for "not gaining an advantage." A system that mechanically flags a forward as offside in the moment they cross the line *collapses the discretionary tolerance into a binary*. This is not a feature. It is an erosion of the room for human judgment that the Laws deliberately preserve.

This paper describes a fictional system — OffsideFence — that proposes to do exactly that collapsing, and then, in the same design, *un-collapses* it through a built-in operating mode that disables the mechanical correction for a specific class of decisions. The fictional artifact is engineered so that both halves of the position can be inspected at the same time.

The intended reader is an engineer or sports-tech practitioner who arrived at this project from a launch video or social post and is asking: *is this real, and if it were, what would it actually look like?* This paper does not answer the first question (see [`why-this-is-fiction.md`](why-this-is-fiction.md) for that), but it does attempt to answer the second.

## 2. Related work

The academic and applied literature on automatic offside detection is well-established. Notable threads include:

- Multi-camera calibration and tracking for offside decision support, with prototype systems dating to the 2010s.
- The use of broadcast feeds as input, including the homography-recovery approach used by the Roboflow Sports pipeline.
- The "free-kick frame" problem: detecting the precise frame at which the ball is played, which is the temporal anchor for any offside decision.
- FIFA's own semi-automated offside technology, which uses limb-tracking with attached sensor data and a 3D ball-tracking system, deployed at major tournaments from 2022 onward.

The work above is *detection*: it produces a position and a frame, and a human official makes the call. The fictional contribution of OffsideFence is to extend the detection layer with a *correction* layer: a haptic actuator that fires in the same latency window as the detection. No deployed system, as of writing, does this. The closest analogs are the haptic-feedback systems in consumer fitness wearables, which are not time-critical and are not positioned as officiating aids.

The related work that most directly informs the OffsideFence concept is the *position* taken by the Laws of the Game themselves: the discretionary tolerance for "not gaining an advantage" is the room in which the rule is not a measurement, and any system that ignores that room has changed the rule.

## 3. The fictional system

### 3.1 Pipeline

The pitch-perception layer consumes a multi-camera broadcast feed (RTSP/SRT, 50p, 1080p+) and produces per-frame, in top-down pitch coordinates:

- A bounding box and class label for each detected player, referee, and goalkeeper.
- A set of pitch keypoints in image coordinates.
- A homography transform from image space to top-down pitch coordinates.

These three sub-components are the Roboflow Sports pipeline. They are real, they are open source, and they are the technology backbone of the concept.

The tactical state engine consumes the per-frame homography-transformed positions and produces an offside decision in ≤80ms from the moment the ball is played. The decision logic is a strict application of the Laws without the discretionary tolerance. This is a deliberate design choice and is discussed in §5.

The haptic tactical correction collar receives the decision over a low-latency encrypted link (see [`spec/ofp-protocol.md`](spec/ofp-protocol.md)) and either pulses or does not pulse, depending on the operating mode.

### 3.2 Latency budget

The end-to-end latency budget from the ball-played frame to the haptic pulse is shown in Table 1.

**Table 1. Latency budget (target p50 / p99)**

| Stage | p50 | p99 |
|-------|-----|-----|
| Frame ingest | 8 ms | 20 ms |
| Player detection | 25 ms | 45 ms |
| Pitch keypoints | 12 ms | 25 ms |
| Homography + RANSAC | 2 ms | 5 ms |
| Tracking (cross-frame) | 5 ms | 12 ms |
| Ball-played detection | 6 ms | 15 ms |
| **Per-frame inference** | **~58 ms** | **~120 ms** |
| Decision + packetization | 4 ms | 10 ms |
| Network (edge → collar) | 8 ms | 25 ms |
| Collar receive + actuator | 6 ms | 15 ms |
| **End-to-end** | **~76 ms** | **~170 ms** |

The p99 of ~170ms is the binding constraint. A forward in full sprint moves 25–30cm in 170ms. A system with this latency profile will, on some decisions, *flag a position the forward has already left*, and on others, *miss a position the forward has already entered*. Neither failure is acceptable in a deployed product, and the latency profile in Table 1 is *not* a defense of deployability. It is a defense of *plausibility*: a fictional system can be specified at this latency and not be obviously impossible.

A real system would have to either (a) accept a higher tolerance, (b) drop into match mode with a wider confidence interval, (c) accept that some mechanically-detected offsides will be wrong, or (d) all of the above. None of these are problems this concept demonstrator solves; they are inherited from the problem space.

## 4. Operating modes

The collar supports four operating modes. Full specifications are in [`docs/mode-specs.md`](docs/mode-specs.md); the summary is in Table 2.

**Table 2. Operating modes**

| Mode | Threshold | Intensity | Failure behavior |
|------|-----------|-----------|------------------|
| Training | 15 cm beyond last defender | 5% of max, 80ms | Silent on uncertainty |
| Match | 5 cm beyond last defender, ≥99.5% confidence | 35% of max, 60ms | Silent on uncertainty |
| Darwin | 5 cm, intensity scaled by repeat-offense count | 20–60%, 60–180ms | Intensity held on link loss |
| Inzaghi Legacy | *N/A — no feedback by design* | *N/A* | *N/A* |

The Darwin mode is named after the observation of cumulative selection in evolutionary biology, and is intended to model a forward's cumulative calibration to the feedback over a match. It is not named after any specific player.

The Inzaghi Legacy mode is named after Filippo Inzaghi. The mode is silent by design, regardless of the decision. The mode exists to preserve, in the design of the artifact, the class of deliberate-early decisions the offside rule has historically permitted. See §5 for the full position.

## 5. The position the artifact takes

The offside rule is a human rule, not a measurement problem. A mechanical offside decision is not the same decision a human assistant referee makes. A system that mechanically prevents a class of decisions the game has historically permitted is not improving the game; it is removing a decision the game has always had.

The Inzaghi Legacy mode is the artifact's position on this. The mode is engineered to be silent *even when the decision is certain*, because the certainty is the wrong thing to act on.

This is not a critique of VAR. It is a critique of a hypothetical category of system that VAR does not currently include: a system that *corrects* rather than *detects*. The critique is built into the artifact as a switch, not as an essay. The switch is named after a forward whose career is the canonical case study in being early on purpose, because the class of decisions being preserved is the class he was making.

A real system in this space would have to negotiate this position with the player-association bodies, the clubs, and the regulators. The negotiation is not designed here. The position is. The position is that a switch like Inzaghi Legacy must exist in any system that proposes mechanical offside correction, because the offside rule requires a judgment, and a judgment requires a person who can be wrong on purpose and be right about it.

## 6. Boundary

This paper does not propose a deployable system. It does not propose a research program. It does not propose a regulatory position. It proposes a *design artifact* that takes a position on the boundary between a measurement and a judgment, in the register of a system specification, so that the position can be inspected.

The artifact is fictional. The artifact is not a product. The artifact is not a startup. The artifact is not affiliated with Roboflow, with any club, with any federation, with any broadcaster, with any equipment manufacturer, or with any sports-tech company. The boundary is held by [`why-this-is-fiction.md`](why-this-is-fiction.md) and [`ethics.md`](ethics.md).

## 7. Acknowledgements

The pitch-perception layer is built conceptually on top of Roboflow Sports, an open-source computer-vision pipeline for football published under MIT license. Roboflow Sports is referenced here as a technology backbone, not a commercial partner. The author is not affiliated with Roboflow, and Roboflow has not endorsed this concept.

The latency-budget framing in §3.2 is influenced by broadcast engineering practice. The Darwin-mode framing in §4 is influenced by the academic literature on cumulative calibration in skill-learning. The Inzaghi-Legacy-mode framing in §5 is the author's own position and is not derived from any specific deployed system, because no such system exists.

## 8. License

This document is published under CC BY-NC 4.0. The reference source stubs in `src/` are published under All Rights Reserved. See [`LICENSE`](../LICENSE) for full terms.

## 9. Citation

If you cite this concept in a piece of writing, please cite it as:

> OffsideFence Concept. (2026). *OffsideFence: a fictional player-wearable concept for real-time offside correction* (concept demonstrator). GitHub. https://github.com/dlxeva/offside-fence

Please do not cite it as a peer-reviewed paper. It is not one.
