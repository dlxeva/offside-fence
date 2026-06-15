# Operating-mode specifications

> This document is part of the OffsideFence concept demonstrator. It specifies, in fictional form, the four operating modes that the haptic tactical correction collar *would* be configured with, if it were a real product. The specifications are written to feel like product specifications a real engineering team might publish — that is the register the content project is operating in. They are not engineering requirements for a real system, and they are not intended to be implemented.

## The four modes

| Mode | Decision conditions | Intensity | Failure behavior |
|------|---------------------|-----------|------------------|
| **Training** | Forward ≥ 15cm beyond last defender at ball-played frame | Single pulse, 80ms, low amplitude (5% of max) | Silent on low confidence or link loss |
| **Match** | Forward ≥ 5cm beyond last defender at ball-played frame, confidence ≥ 99.5% | Single pulse, 60ms, calibrated amplitude (35% of max) | Silent on link loss; logged on confidence miss |
| **Darwin** | Forward ≥ 5cm beyond last defender, intensity scaled by repeat-offense count in current match (see curve below) | Adaptive, 60–180ms, 20–60% of max | Silent on link loss; intensity held at match-start value on confidence miss |
| **Inzaghi Legacy** | *N/A — no feedback, by design* | *N/A* | *N/A — silence is the design* |

The threshold values are illustrative, not engineered. A real system would tune them against athlete comfort studies, broadcast latency measurements, and FIFA Equipment Regulation review. None of those have been done. They are presented here to give the modes *shape*.

## Mode semantics

### Training

**Intended user:** academy coaches running repetition drills in non-broadcast settings. The forward knows the collar is active. The drill is built around the feedback.

**Design choice:** wide tolerance (15cm) and low intensity (5%) to keep the feedback informative rather than punitive. The mode is the gentlest the system can be while still being the system.

**Failure semantics:** if the decision link is lost, the collar is silent. A training drill with intermittent feedback is worse than no feedback at all, because the forward will calibrate to the silence, and the next pulse will be uninterpretable.

### Match

**Intended user:** professional clubs in competitive fixtures under broadcast. The threshold is tight (5cm) and the confidence requirement is strict (≥99.5%). A false positive on a live match is the worst possible outcome of the system, because it would generate a press cycle and a regulatory conversation in the same week.

**Design choice:** the false-positive cost dominates the false-negative cost. The mode accepts that it will *miss* some offsides rather than *mis-call* some onside positions. This is the opposite trade-off from a human assistant referee, who is given wide tolerance and asked to call what they see.

**Failure semantics:** if the link is lost, the collar is silent and the bench display logs the gap. If a decision packet arrives with confidence < 99.5%, the collar is silent and the gap is logged at higher priority, because a near-miss decision in match mode is a candidate for system retraining in a real product.

### Darwin

**Intended user:** coaches studying opponent tendency build-up. The mode is named for the observation that repeat-offense players do not behave like first-offense players: they calibrate. The Darwin intensity curve attempts to model that calibration by escalating intensity, on the assumption that a forward who has been corrected once and is approaching a second offside is approaching it *aware* of the first correction, and may need a stronger signal to break the pattern.

**Intensity curve (illustrative):**

| Repeat-offense count in current match | Intensity (% of max) | Pulse duration (ms) |
|---------------------------------------|----------------------|---------------------|
| 1 | 20% | 60 |
| 2 | 35% | 80 |
| 3 | 45% | 100 |
| 4 | 55% | 130 |
| 5+ | 60% | 180 |

The curve is monotone non-decreasing by construction. The Darwin mode does not de-escalate within a match. This is a deliberate choice to model the asymmetry between correction and learning: a forward who has been corrected five times in a match has, in some sense, been told the rule, and a sixth correction is no longer *information*, it is *consequence*.

**Failure semantics:** if the link is lost, intensity is held at the match-start value (20%, 60ms) when the link returns, not the current match value. This prevents a returning link from escalating intensity across a gap. If confidence misses, intensity is also held, not reset, on the assumption that the forward's calibration state has not changed during the gap.

**Naming note:** the mode is named after Charles Darwin's observation of cumulative selection, not after any specific player. The cumulative-curve behavior is intended to model the *forward's* cumulative calibration, not any property of the system itself.

### Inzaghi Legacy

**Intended user:** no one. The mode is not for use.

**Design choice:** the collar is silent in this mode regardless of decision. The mode is a configuration option, not a feature.

**Naming note:** the mode is named after Filippo Inzaghi because his career is the canonical case study of a forward who, in the consensus view of football historians, was sometimes early on purpose. The mode exists to encode the position that **a system which mechanically prevents Inzaghi's deliberate-early runs is not improving the game; it is removing a decision the game has always had.**

This is not a joke. It is the position the concept demonstrator takes. See [`ethics.md`](ethics.md) for the full statement.

**Failure semantics:** none. The mode cannot fail. The mode is silence.

## Mode selection in the system

In a real product, the mode would be selected by the coaching staff before match kickoff, locked for the duration of the match, and logged in the bench display. Mode changes mid-match would be restricted to:

- **Training → Match**: at the request of the bench, on confirmation that the match is officially underway.
- **Match → Inzaghi Legacy**: at the request of the *player*, on the player's explicit instruction, with no further confirmation required. This is the only mode the player can self-select.

The asymmetry — that the player can put the collar into Inzaghi Legacy at will, but cannot take it out of any other mode — is the design position the concept demonstrator is taking. The collar is a tool the player can opt out of, not a tool the player can opt in and out of. A real product in this space would have to negotiate this asymmetry with the relevant player-association bodies, the clubs, and the regulators. None of that negotiation has happened, and none of it is designed here.

## What this document is not

- It is not an engineering requirements document. There is no engineering team. There is no implementation.
- It is not a medical or comfort study. The intensity values are illustrative.
- It is not a regulatory submission. FIFA, IFAB, UEFA, the Premier League, La Liga, the Bundesliga, and Serie A have not been contacted, and will not be contacted, on the basis of this concept.
- It is not a clinical validation. The Darwin intensity curve is not derived from any human-subjects data.

For the boundary this concept demonstrator respects, see [`ethics.md`](ethics.md) and [`why-this-is-fiction.md`](why-this-is-fiction.md).
