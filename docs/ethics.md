# Ethics & boundary statement

> This file is part of the OffsideFence concept demonstrator. It is not a regulatory document, not a legal opinion, and not a substitute for the relevant sports, medical, and privacy frameworks that any *real* player-wearable system would have to clear. It is a written record of the questions we asked before publishing the concept, and the answers we arrived at.

The position taken here is **that the engineering register of this repository should not be confused with a position that the artifact itself is ready, appropriate, or desirable as a real product.**

## 1. The player is not a sensor platform

A player-wearable system that detects offside in real time makes the player's body an extension of the broadcast infrastructure. Even if the hardware were comfortable, certified, and consensual, the player's body becomes:

- A node in a data network that the player does not own.
- A site of measurement that the player did not choose.
- A locus of judgment that the player cannot inspect in real time.

This is a category shift, not a feature. It is closer to a workplace monitoring system that an employee cannot turn off than it is to a heart-rate strap that an athlete uses voluntarily for self-optimization.

OffsideFence as a concept raises this category question explicitly, by design. It is not a position that the category shift is acceptable. It is a question of whether the category shift is even coherent, and what would have to be true for it to be acceptable.

## 2. The offside rule is a human rule, not a measurement problem

The Laws of the Game define offside as a judgment by the assistant referee, informed by position, by movement, by intent at the moment the ball is played, and by a discretionary tolerance for "not gaining an advantage."

A system that mechanically flags a forward as offside in the moment they cross the line *collapses the discretionary tolerance into a binary*. This is not a feature. It is an erosion of the room for human judgment that the Laws deliberately preserve.

OffsideFence as a concept does not propose that this erosion is desirable. It asks: *if* the erosion is technically possible, *what* is the smallest decision we are losing when we collapse the rule into a measurement?

The Inzaghi Legacy operating mode — `feedback disabled, by design, in memoriam` — is the answer the concept arrives at: **the smallest decision we are losing is the one where the forward chooses to be early on purpose, because the play demanded it, and the coach and the forward agreed beforehand that this is the right call.** A system that mechanically prevents that decision is not improving the game. It is removing a decision the game has always had.

## 3. The "Inzaghi mode" is not a joke. It is the position the concept takes.

The naming of an operating mode after Filippo Inzaghi — a forward whose entire career was, famously, a controlled experiment in being just on the right side of offside, and occasionally just on the wrong side of it on purpose — is not a punchline. It is a deliberate choice to make the *most uncomfortable* design decision the one the system explicitly preserves.

A concept demonstrator that included Training / Match / Darwin modes but not Inzaghi Legacy would be a concept demonstrator that proposes mechanical offside correction as desirable. Adding Inzaghi Legacy forces the concept to acknowledge that there are moments when mechanical correction would be wrong. The mode exists to keep that acknowledgement in the artifact, even in fictional form.

## 4. We will not deploy

OffsideFence has not been deployed. It will not be deployed by the author of this concept. It will not be licensed, transferred, or relicensed to a party that intends to deploy it.

If a deployment-grade player-wearable offside system is ever built, it will be built by a different team, under a different name, with a different design space, and likely with a different position on the questions above. This repository is not a contribution to that effort. It is a *comment* on the space in which that effort would sit.

## 5. The boundary the concept respects

The boundary this concept respects is the same boundary the offside rule itself respects: **a position is not a violation, a violation is a judgment, and a judgment requires a person who can be wrong on purpose and be right about it.**

The hardware layer of OffsideFence, in its fictional form, *cannot* be wrong on purpose. That is why Inzaghi Legacy exists. That is why the system, in its conceptual form, has a switch that turns itself off.

A real system in this space, if one is ever built, should also have that switch. Whether it does or does not is a question for that system, not for this one.

## 6. The author of this concept is a single individual

This concept was designed and documented by a single individual, for a single-shot content project, as a deliberate exercise in the boundary between "what computer vision can already do for football" and "what we should or shouldn't strap to a player's body." The author is not a sports scientist, not a clinician, not a regulatory specialist, and not a player. The boundary statement above is the position of a writer, not the position of a field.

If readers of this repository find the boundary statement either too cautious or not cautious enough, the author is interested in the disagreement. The disagreement is the point. See [`../README.md`](../README.md) for contact information.
