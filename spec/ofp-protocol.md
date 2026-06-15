# OFP/0.1 — Offside Fence Protocol

> **Status:** fictional specification, version 0.1
> **Audience:** engineers who arrived at this repository and want to know what the collar *would* speak, if it were a real product.
> **Scope:** decision-packet format, transport, security, and failure modes for the link between the tactical state engine and the haptic tactical correction collar.

This is a *protocol specification*, not a software implementation. There is no reference implementation. The packet format described below is a plausible design; it is not the design any real engineering team has agreed on, because there is no real engineering team.

## 1. Naming

- **Protocol name:** Offside Fence Protocol
- **Version:** `OFP/0.1`
- **Wire format:** length-prefixed binary, big-endian
- **Default port:** `7421/udp` (registered for the fictional protocol)
- **Transport:** UDP for decision packets, TCP for control plane
- **Encryption:** DTLS 1.3 for UDP, TLS 1.3 for TCP
- **Authentication:** collar-side X.509 certificate, pinned to the bench display at pairing time

## 2. Decision packet format

The decision packet is the unit of communication from the tactical state engine to the collar. It is the *only* packet the collar acts on. The collar has no other inputs.

### 2.1 Binary layout

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|     version   |   flags       |           session_id           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
+                    timestamp (ns, 64-bit)                     +
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|     mode      |   decision    |   confidence  |   intensity   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|     repeat_count (uint8)      |   padding      |   seq (16)  ...
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### 2.2 Field definitions

| Field | Size | Encoding | Description |
|-------|------|----------|-------------|
| `version` | 1 | uint8 | Protocol version. Current: `0x01` |
| `flags` | 1 | bitfield | Bit 0: `ACTUATOR_EN` (collar should pulse if conditions met). Bit 1: `BATT_LOW`. Bit 2: `LINK_TEST`. Bits 3-7: reserved. |
| `session_id` | 2 | uint16 | Match-day session identifier. Collar rejects packets with mismatched session. |
| `timestamp` | 8 | uint64, ns | Wall-clock time at which the decision was made, in nanoseconds since Unix epoch. |
| `mode` | 1 | uint8 | `0x01` Training, `0x02` Match, `0x03` Darwin, `0x04` Inzaghi Legacy. |
| `decision` | 1 | uint8 | `0x00` No decision (e.g., no ball-played frame detected). `0x01` Onside. `0x02` Offside. |
| `confidence` | 1 | uint8 | Confidence in the decision, 0–255, scaled from the engine's float output. |
| `intensity` | 1 | uint8 | Recommended actuator intensity, 0–255. The collar may apply its own scaling. |
| `repeat_count` | 1 | uint8 | Repeat-offense count in the current match (Darwin mode only). |
| `seq` | 2 | uint16 | Sequence number, monotonically increasing per session. |

Total payload: **20 bytes** (not counting UDP/IP headers).

### 2.3 Decision semantics

The collar is a *dumb* device. It does not interpret the offside rule. It does not evaluate the decision. It does not have a model of the pitch. It does not have a model of the player.

The collar receives a decision packet and either:

- Acts on it (if `ACTUATOR_EN` is set, the `decision` is `0x02`, the `confidence` is above the per-mode threshold, and the link is healthy), or
- Does not act on it (every other case).

There is **no** case in which the collar *modifies* the decision. The collar is a haptic relay. The decision lives in the tactical state engine, and the engine is the only system with the authority to make a call.

This is the single most important design constraint in the protocol. The collar is not allowed to be smart. If the collar is smart, the collar is a second opinion, and a second opinion with a haptic actuator is a regulatory and ethical category shift that this concept demonstrator does not undertake to design.

## 3. Failure modes on the wire

| Wire condition | Collar behavior |
|----------------|-----------------|
| Packet arrives with `ACTUATOR_EN` clear | No actuation. Log. |
| Packet arrives with `confidence` < per-mode threshold | No actuation. Log. |
| Packet arrives with `session_id` mismatch | No actuation. Log. Refuse all packets with the mismatched session. |
| Packet arrives with `seq` not strictly monotonic | No actuation. Log. |
| No packet received for > 500ms | **Fall silent.** Announce link gap to bench display over TCP. |
| Battery low (collar-side) | Set `BATT_LOW` flag in next outgoing heartbeat. Continue normal actuation. |
| DTLS handshake failure on link startup | Collar remains in safe mode. No actuation. |

The asymmetry — that the collar falls silent on uncertainty — is the design position. A real product would have to defend this position in front of the player-association bodies, the clubs, and the regulators. The defense is: **a missed correction is recoverable; an unwarranted correction is not.**

## 4. Control plane (TCP)

A separate TCP connection carries the control plane: pairing, mode selection, session lifecycle, and heartbeat. The collar's control plane speaks the same protocol family (`OFP/0.1`) but on TCP. The control-plane message set is small:

| Message | Direction | Purpose |
|---------|-----------|---------|
| `PAIR_REQUEST` | collar → bench | Collar requests pairing with bench display. |
| `PAIR_ACCEPT` | bench → collar | Bench display accepts, with pinned X.509 fingerprint. |
| `MODE_SET` | bench → collar | Sets the operating mode. Collar confirms. |
| `MODE_GET` | collar → bench | Collar queries current mode. |
| `HEARTBEAT` | collar → bench (every 5s) | Status: battery, link, mode, last packet seq. |
| `SESSION_BEGIN` | bench → collar | Marks the start of a match-day session. |
| `SESSION_END` | bench → collar | Marks the end. Collar returns to safe mode. |
| `PLAYER_OPT_OUT` | **player → collar** | Player-initiated mode change to Inzaghi Legacy. **No bench confirmation required.** |

The last row is the only message in the protocol the player can originate. The asymmetry is intentional and is the same asymmetry documented in [`../docs/mode-specs.md`](../docs/mode-specs.md).

## 5. Security

- All decision packets are DTLS-encrypted. The collar does not accept plaintext.
- All control-plane messages are TLS-encrypted over TCP.
- The collar's X.509 certificate is pinned to the bench display at pairing time. A collar that presents a different certificate is refused.
- The bench display's certificate is pinned to the tactical state engine at deployment time.
- No remote firmware updates over the wire. Firmware updates require a physical connection to the bench display and a signed manifest from the engineering team.
- No telemetry leaves the bench display. The control plane is local to the stadium network.

A real product would also need: a hardware secure element on the collar, a revocation list for stolen or compromised benches, a key-rotation procedure, and an incident-response protocol for suspected link compromise. None of these are designed here.

## 6. What this protocol is not

- It is not an open standard. There is no standardization body. There is no IETF draft.
- It is not a published reference implementation. There is no `pip install ofp`. There is no GitHub release.
- It is not a regulatory submission. There is no FIFA, IFAB, or equipment-regulation review.
- It is not a patent. No patent has been filed on this design. The design is published in the documentation under CC BY-NC 4.0; the protocol *name* (`Offside Fence Protocol`) is used as a fictional identifier, not as a trademark.

## 7. Versioning

| Version | Date | Notes |
|---------|------|-------|
| `0.1` | 2026-06-15 | Initial fictional specification. No prior versions. |

This is the only version. There will be no `0.2`. The protocol is a design artifact, not a living specification.

## 8. Acknowledgements

The protocol's design constraints are influenced by broadcast engineering practice (low-latency UDP for time-sensitive control, TCP for configuration), by DTLS/TLS protocol design, and by the design register of fictional-but-rigorous technical specifications. The protocol is not derived from any specific deployed sports-wearable system, because no such system is in production as of writing.
