# Changelog

> All notable changes to the OffsideFence concept demonstrator are documented in this file.
>
> This is a single-shot concept artifact. There will be no further versions. The changelog is published in the register of a real project, because the register is the deliverable.

## Format

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) for the documentation; source stubs are versioned separately (and not at all) under the All-Rights-Reserved terms in [`LICENSE`](LICENSE).

## [0.1.0] — 2026-06-15

### Added
- Initial concept publication.
- Architecture diagram in [`docs/architecture.md`](docs/architecture.md) with end-to-end latency budget.
- Operating-mode specifications for Training, Match, Darwin, and Inzaghi Legacy in [`docs/mode-specs.md`](docs/mode-specs.md).
- OFP/0.1 decision-packet protocol specification in [`spec/ofp-protocol.md`](spec/ofp-protocol.md).
- Reference source stubs for the four modules: decision engine, pitch calibration, packet codec, and collar firmware. All stubs raise `NotImplementedError` by design.
- White paper (arXiv-style, fictional) in [`white-paper.md`](white-paper.md).
- Boundary statement in [`docs/why-this-is-fiction.md`](docs/why-this-is-fiction.md) and [`docs/ethics.md`](docs/ethics.md).
- Press kit in [`docs/press-kit.md`](docs/press-kit.md).
- License terms: CC BY-NC 4.0 for documentation, All Rights Reserved for source stubs.

### Naming
- Product: **OffsideFence™ 越位电子围栏**
- Official term: **Haptic Tactical Correction**
- Forum term (Chinese football fan culture): **电一下**
- Protocol: **OFP/0.1** (Offside Fence Protocol)
- Modes: **Training** / **Match** / **Darwin** / **Inzaghi Legacy**
- Pipeline: **Pitch Perception Layer** → **Tactical State Engine** → **Haptic Tactical Correction Collar**

### Acknowledgements
- Pitch perception layer is built conceptually on top of [Roboflow Sports](https://github.com/roboflow/sports), open source under MIT. Not affiliated. Not endorsed.

### Position
- The Inzaghi Legacy mode is the position the concept demonstrator takes. The mode is silent by design, to preserve the class of deliberate-early decisions the offside rule has historically permitted. See [`docs/ethics.md`](docs/ethics.md) for the full statement.

### Not added (and not planned)
- No roadmap. No firmware updates. No issue tracker for product support. No partnerships. No fundraising. No Series A. No demo day. See [`docs/why-this-is-fiction.md`](docs/why-this-is-fiction.md) for the boundary.

## [Unreleased]

Nothing. This is a single-shot artifact. There is no `[Unreleased]` section because nothing is unreleased.

[0.1.0]: https://github.com/dlxeva/offside-fence/releases/tag/v0.1.0
