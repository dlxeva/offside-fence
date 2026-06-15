# Architecture (concept overview)

> This document describes the system that *would* exist if OffsideFence were a real product. The pipeline is real (Roboflow Sports, OpenCV, broadcast engineering notation). The integration is plausible. The deployment is fictional. The boundary is held by [`ethics.md`](ethics.md) and [`why-this-is-fiction.md`](why-this-is-fiction.md).

## 1. Top-level diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                          Broadcast Feed                              │
│                    (multi-camera · 50p · 1080p+)                     │
└──────────────────────────────┬───────────────────────────────────────┘
                               │ RTSP / SRT
                               ▼
┌──────────────────────────────────────────────────────────────────────┐
│              Pitch Perception Layer (edge · on-prem)                │
│  ┌────────────────────┐  ┌────────────────────┐  ┌────────────────┐  │
│  │  Player Detection  │  │   Pitch Keypoints  │  │  Homography    │  │
│  │  (Roboflow Sports) │  │  (Roboflow Sports) │  │   (OpenCV)     │  │
│  └─────────┬──────────┘  └─────────┬──────────┘  └────────┬───────┘  │
│            └────────────┬──────────┘                       │          │
│                         ▼                                  │          │
│              ┌──────────────────────┐                      │          │
│              │  Tactical State      │◀─────────────────────┘          │
│              │  Engine (offside)    │                                 │
│              └──────────┬───────────┘                                 │
│                         │ decision packet (≤80ms)                     │
└─────────────────────────┼────────────────────────────────────────────┘
                          ▼
┌──────────────────────────────────────────────────────────────────────┐
│                 Haptic Tactical Correction (collar)                  │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                 │
│  │  Training   │   │   Match     │   │  Darwin /   │                 │
│  │   Mode      │   │   Mode      │   │  Inzaghi    │                 │
│  │  (gentle)   │   │  (firm)     │   │  Legacy     │                 │
│  └─────────────┘   └─────────────┘   └─────────────┘                 │
│                          ▲                                           │
│                          │ encrypted backchannel                     │
│  ┌───────────────────────┴──────────────────────────┐                │
│  │         Coaching Tablet / Bench Display          │                │
│  └──────────────────────────────────────────────────┘                │
└──────────────────────────────────────────────────────────────────────┘
```

## 2. Pitch perception layer

The pitch perception layer is the part of the system that is closest to current open-source capability. The three sub-components operate on each broadcast frame independently and feed a shared tactical state engine downstream.

### 2.1 Player detection

Per-frame player detection using a fine-tuned object detector trained on broadcast football imagery. The reference architecture for this module is the Roboflow Sports pipeline (open source, MIT-licensed). Inputs are broadcast frames; outputs are bounding boxes with class labels (player, referee, goalkeeper) and per-detection confidence scores.

**Reference:** `Roboflow/sports` on GitHub, pipeline component `player_detection/`.

### 2.2 Pitch keypoint estimation

Per-frame estimation of pitch landmark keypoints (corner flags, penalty spots, center circle, touchline intersections). Output is a set of 2D image coordinates that correspond to a known set of 3D pitch coordinates. The reference architecture is also the Roboflow Sports pipeline, component `pitch_keypoint_estimation/`.

### 2.3 Homography recovery

Given the 2D keypoints and their known 3D counterparts, recover a per-frame homography transform from image space to a top-down pitch coordinate frame. This is a standard application of OpenCV's `findHomography` followed by RANSAC filtering to reject misdetected keypoints. The output is a 3×3 matrix that places every detected player bounding box foot-position in top-down pitch coordinates.

**Reference:** `OpenCV` modules `calib3d` and `imgproc`. Standard computer-vision textbook material, not OffsideFence-specific.

## 3. Tactical state engine

The tactical state engine consumes per-frame homography-transformed player positions and produces an offside decision in ≤80ms from the moment the ball is played.

### 3.1 Decision inputs

- Last defender position (excluding the goalkeeper, excluding the player under evaluation).
- Ball-played frame timestamp.
- Per-frame tracking ID for the forward under evaluation.
- Forward foot position in top-down pitch coordinates.

### 3.2 Decision logic

The decision is a strict application of the Laws of the Game, *without* the discretionary tolerance that a human assistant referee would apply. This is intentional and is the design choice the concept demonstrator is making explicit: a mechanical offside decision is not the same decision a human assistant referee makes.

```
def decide(forward_pos, last_defender_pos, ball_played_at):
    if forward_pos.x > last_defender_pos.x:  # attacking direction
        return Decision(offside=True, confidence=HIGH)
    return Decision(offside=False, confidence=HIGH)
```

This is the only decision the engine makes. The complexity of the real system is in the *inputs* — robust tracking, reliable homography under broadcast camera motion, low-latency ball-played frame detection — not in the rule itself.

**Reference stub:** [`../src/offside-decision/decision_stub.py`](../src/offside-decision/decision_stub.py). The stub returns a `NotImplemented` error by design; see the file's docstring for the reasoning.

### 3.3 Latency budget

| Stage | Target (p50) | Target (p99) |
|-------|--------------|--------------|
| Frame ingest (RTSP/SRT) | 8 ms | 20 ms |
| Player detection (per frame) | 25 ms | 45 ms |
| Pitch keypoints (per frame) | 12 ms | 25 ms |
| Homography + RANSAC | 2 ms | 5 ms |
| Tracking (cross-frame) | 5 ms | 12 ms |
| Ball-played detection | 6 ms | 15 ms |
| **Per-frame total (inference)** | **~58 ms** | **~120 ms** |
| Decision + packetization | 4 ms | 10 ms |
| Network (edge → collar) | 8 ms | 25 ms |
| Collar receive + actuator trigger | 6 ms | 15 ms |
| **End-to-end (ball-played → haptic)** | **~76 ms** | **~170 ms** |

The end-to-end p99 of ~170ms is uncomfortably close to the threshold at which a forward in full sprint can move 25–30cm after the ball is played. A real system would need to either (a) accept a higher tolerance, (b) drop into match mode with a wider confidence interval, or (c) accept that some mechanically-detected offsides will be wrong. None of these are problems this concept demonstrator solves; they are problems any real system in this space would inherit.

## 4. Haptic tactical correction layer

The collar. This is the fictional hardware. The decision-packet interface is specified in [`../spec/ofp-protocol.md`](../spec/ofp-protocol.md). The actuator, the battery, the comfort study, the certification pathway — none of these exist, and none are designed here.

What is *specified* is the operating-mode taxonomy. Each mode defines (a) the decision conditions under which the actuator would be triggered, (b) the intensity curve, and (c) the failure-mode behavior (what the collar does when the decision link is lost, when the battery is low, when the broadcast feed is unavailable).

For full mode specifications, see [`mode-specs.md`](mode-specs.md). The short version:

| Mode | Behavior | Failure mode |
|------|----------|--------------|
| Training | Single short pulse, low intensity, after a 200ms latency check | Falls silent |
| Match | Decision-validated pulse, no false positive > 0.5% | Falls silent |
| Darwin | Adaptive intensity, tracks repeat-offense count | Falls silent |
| **Inzaghi Legacy** | **No feedback. By design.** | **No feedback. By design.** |

The pattern across the first three modes is *fail silent* — when the system cannot guarantee a high-confidence decision, the collar does not pulse. The pattern in Inzaghi Legacy is *silent always* — the mode exists to model a class of decisions the system is explicitly not allowed to make.

## 5. Coaching tablet / bench display

A real product would have a coaching-side interface: which players are currently wearing collars, which mode each collar is in, the live decision log, the per-player repeat-offense count, and the per-match aggregate feedback for post-game analysis. This is sketched in the top-level diagram and is the part of the system that would, in a real product, be the most defensible from a sports-medicine and consent perspective: the player is the only one whose body is in the loop; the coach sees the *aggregate*, not the live decision-to-actuator trigger.

The concept demonstrator does not specify the coaching-side interface. It is mentioned here only to make the asymmetry explicit.

## 6. Failure semantics

| Failure | Concept-level response |
|---------|------------------------|
| Loss of broadcast feed | Collar falls silent. No decision. No feedback. |
| Loss of pitch perception (e.g., camera blocked) | Collar falls silent. |
| Decision confidence < threshold | Collar falls silent. |
| Decision link lost (collar offline) | Coaching tablet logs the gap. |
| Battery low | Collar pulses once, long, then falls silent. |
| **Inzaghi Legacy mode active** | **Collar silent regardless of decision.** |

The asymmetry between the first six rows and the seventh row is the design position the concept demonstrator is taking. Mechanical offside correction is a *fallible* decision. The system is engineered to fail silent when it is uncertain. Inzaghi Legacy is the mode in which the system is engineered to be silent *even when it is certain*, because the certainty is the wrong thing to act on.

This is not a feature comparison against an existing product. There is no existing product in this space. This is a position statement on what a system in this space *would have to look like* if it were to be built at all.

## 7. Reference implementation status

The `src/` tree contains protocol stubs and reference function signatures only. It is not a runnable pipeline, and it is not intended to become one. The intent of the reference stubs is to make the architecture inspectable: a reader can confirm that the function signatures match the architecture, and that the failure semantics match the boundary statement.

| Module | Status |
|--------|--------|
| `src/offside-decision/decision_stub.py` | Signature + docstring only |
| `src/field-calibration/calib_stub.py` | Signature + docstring only |
| `src/decision-packet/packet_stub.py` | Signature + docstring only |
| `src/collar/feedback_stub.py` | Signature + docstring only |

None of these are intended to be `pip install`-able. None of these have tests. This is a design artifact, not a software product.
