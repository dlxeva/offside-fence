# `src/` — Reference stubs

> **This directory is documentation. It is not a software product.**

The four files in this directory are protocol stubs and reference function signatures for the OffsideFence concept. They exist so that a reader can confirm that the function signatures match the architecture document, and that the failure semantics match the boundary statement.

**They are not intended to be run, imported, tested, packaged, or distributed.** Each file raises `NotImplementedError` by design.

## What is here

```
src/
├── README.md
├── offside-decision/
│   └── decision_stub.py        # tactical state engine: offside decision
├── field-calibration/
│   └── calib_stub.py           # homography recovery + RANSAC
├── decision-packet/
│   └── packet_stub.py          # OFP/0.1 packet encode/decode
└── collar/
    └── feedback_stub.py        # collar-side: packet receive + actuator
```

Four modules. Four stubs. Each module's stub is the smallest possible artifact that *looks like* the corresponding layer of the architecture in [`../docs/architecture.md`](../docs/architecture.md), and the smallest possible artifact that *cannot be mistaken for a runnable implementation*.

## What is not here

- No `pyproject.toml`. No `setup.py`. No `requirements.txt`. There is nothing to install.
- No `tests/`. There is nothing to test.
- No `__init__.py` modules. There are no packages to import.
- No CI configuration. There is no continuous integration to configure.
- No README in each module. The docstring on each stub is the documentation.

The absence is the design. A reader who arrives at this directory and finds four stubs and no `pip install` path is being shown, by the absence, that this is a concept demonstrator and not a software project.

## The four stubs, summarized

### `offside-decision/decision_stub.py`

The tactical state engine's decision function. Takes per-frame homography-transformed positions, returns a decision (`onside` or `offside`) and a confidence. In a real system this would be a tight inner loop running at broadcast frame rate.

**In the stub:** the function signature matches the architecture. The function body is `raise NotImplementedError`.

### `field-calibration/calib_stub.py`

Homography recovery from pitch keypoints. In a real system this would be a per-frame OpenCV call with RANSAC filtering.

**In the stub:** the function signature matches the architecture. The function body is `raise NotImplementedError`.

### `decision-packet/packet_stub.py`

The OFP/0.1 packet encoder and decoder. The packet format is specified in [`../spec/ofp-protocol.md`](../spec/ofp-protocol.md). A real implementation would serialize the 20-byte decision packet described there.

**In the stub:** the encoder takes a `DecisionPacket` dataclass and returns `bytes`. The decoder does the reverse. The bodies are `raise NotImplementedError`.

### `collar/feedback_stub.py`

The collar-side packet receiver and actuator trigger. In a real system this would be an embedded firmware module on the collar's microcontroller. The collar is a *dumb* device by design — it does not interpret the decision, it acts on it or does not act on it, depending on the mode.

**In the stub:** the function signature matches the protocol. The function body is `raise NotImplementedError`.

## Why the stubs raise `NotImplementedError`

The OffsideFence concept demonstrator takes a position on the boundary between a runnable system and a design artifact. The position is that a runnable system in this space would be a category shift — into sports medicine, into player consent, into officiating regulation, into equipment certification. None of those categories are designed here.

A `NotImplementedError` is a small, honest way to mark that boundary in code. It says: *this is what the function would look like, this is what it would take, this is not built.* It is more honest than a partial implementation, because a partial implementation invites a reader to think the rest is on the way.

## License

The four stub files in this directory are published under **All Rights Reserved**. They may be read in the context of this repository. They may not be copied, modified, redistributed, or used as the basis of a derivative work.

The decision to reserve rights on the stubs — while the documentation is under CC BY-NC 4.0 — is deliberate. The documentation is meant to be read, shared, and discussed. The stubs are meant to be looked at, nodded at, and not built on.

For the full license terms, see [`../LICENSE`](../LICENSE).
