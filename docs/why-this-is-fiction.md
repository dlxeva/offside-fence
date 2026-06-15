# Why this is fiction

> If you arrived here from a video, social post, press mention, or a friend saying "isn't this the offside collar thing?", **start here.**

## TL;DR

OffsideFence is a **concept demonstrator** created for a single-shot content project. It is not a real product. It is not a startup. It is not a research prototype. It is not affiliated with any club, federation, broadcaster, equipment manufacturer, or sports-tech company.

The pipeline that *would* power it (player detection, pitch keypoint estimation, homography, tracking) is real and open source. The hardware that *would* deliver the haptic correction is fictional. The integration that *would* tie them together at broadcast latency is deliberately not built.

## Why we are putting this disclaimer on a concept demonstrator

Most fiction-on-the-internet either:

1. Presents itself as real (and gets away with it for a while), or
2. Presents itself obviously as parody (and the joke lands but the seriousness is gone).

OffsideFence is in a third category. It is engineered *to be* indistinguishable from a real product, because the deliverable of the content project is the moment of doubt:

> *"Wait, is this actually a thing?"*

That moment only works if the artifact is rigorous. It also only works if the artifact is *honest about being a concept*, because a viewer who walks away genuinely believing there is a real product on the market has been deceived, and the joke has been spoiled for them when they find out.

This file is the place where we say it: **the artifact is fictional, the engineering standard is real, and the moment of doubt is the point.**

## What is real

- The computer-vision pipeline that detects players, estimates pitch keypoints, and recovers a homography transform of the field. This is open source, well-documented in the academic and applied literature, and referenced in [`white-paper.md`](../white-paper.md).
- The protocol design for a low-latency decision-to-collar link. Specifications in [`spec/ofp-protocol.md`](../spec/ofp-protocol.md) describe a plausible, implementable interface, not a working system.
- The naming, terminology, and operating-mode taxonomy (Training / Match / Darwin / Inzaghi Legacy). These are written to feel like product decisions that a real engineering team would have made, because that is the register the content project is operating in.

## What is fictional

- The hardware. There is no collar. There is no haptic actuator design. There is no battery life chart. There is no comfort study. There is no certification pathway (FCC, CE, FIFA Equipment Regulations).
- The integration. The pipeline in the diagram would not, in its current published form, deliver an offside decision in the ≤80ms window required for haptic correction. The latency math is plausible; the demonstration is not built.
- The product. There is no price. There is no order form. There is no roadmap, no fundraising, no early access, no press list, no partnerships inbox, no support team.
- The clinical claim. OffsideFence has not been tested on athletes, has not been cleared by any sports medical body, and has not been the subject of any human-subjects research.

## What we will not do

- We will not sell, pre-sell, take reservations for, or accept payment for any OffsideFence product.
- We will not solicit contact information, mailing list signups, or "expression of interest" submissions.
- We will not respond to media inquiries as if OffsideFence is a real product in development.
- We will not issue corrections, updates, or "coming soon" announcements that imply a real product roadmap.
- We will not enter into any partnership, sponsorship, or co-marketing arrangement on the basis of this concept.

If a real product is ever built under a different name by a different team, it will not be a continuation of this project. This repository will be archived before any such announcement, and the README will be updated to point at the actual product.

## What this repository *is* good for

- Reading about how a modern pitch perception pipeline can plausibly be extended toward a player-wearable scenario.
- Studying the latency budget and decision-packet design considerations of a hypothetical ≤80ms offside decision path.
- Understanding why such a system, even if technically feasible, raises questions that the technical layer alone cannot answer (see [`ethics.md`](ethics.md)).
- Enjoying a piece of speculative product design as a creative exercise.

## Contact

This is a single-author concept project. There is no press team.

For genuine inquiries about the content project that produced this repository, see the [project entry on the author's public notebook](../README.md#contact).
