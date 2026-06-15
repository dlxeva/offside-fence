"""
Collar feedback stub — packet receiver and actuator trigger.

This is a reference function signature for the collar-side firmware
module of OffsideFence. It is NOT an implementation.

The collar is a *dumb* device by design. It does not interpret the
offside rule. It does not have a model of the pitch. It does not have
a model of the player. It receives a decision packet and either acts
on it (pulses the actuator) or does not act on it.

A real implementation would:
  - receive the DTLS-encrypted UDP packet,
  - validate the version, session_id, and seq fields,
  - apply the per-mode threshold and confidence requirement,
  - apply the Inzaghi Legacy override (silence regardless of decision),
  - apply the per-mode intensity scaling (the collar may scale the
    engine's recommendation by its own calibration),
  - drive the haptic actuator on a 60-180ms pulse,
  - emit a heartbeat to the bench display over TCP every 5 seconds,
  - raise a BATT_LOW flag in the next outgoing heartbeat if the
    battery is below threshold.

This stub raises NotImplementedError by design.
"""

from dataclasses import dataclass
from enum import Enum


class Mode(Enum):
    """Operating mode of the collar."""
    TRAINING = 0x01
    MATCH = 0x02
    DARWIN = 0x03
    INZAGHI_LEGACY = 0x04  # silence by design


@dataclass(frozen=True)
class CollarConfig:
    """Per-collar configuration, set at pairing time."""
    collar_id: str
    paired_session_id: int
    mode: Mode
    intensity_scale: float       # 0.0 – 1.0, collar-side calibration
    confidence_threshold: int    # uint8, 0-255, per-mode minimum


@dataclass(frozen=True)
class PacketInput:
    """The decision packet the collar has just received (already decoded)."""
    version: int
    flags: int
    session_id: int
    timestamp_ns: int
    mode: Mode
    outcome: int              # 0x00 NONE, 0x01 ON, 0x02 OFF
    confidence: int
    intensity: int
    repeat_count: int
    seq: int


@dataclass(frozen=True)
class ActuatorCommand:
    """The command the collar would issue to the haptic actuator."""
    pulse_duration_ms: int     # 0 means "do not pulse"
    pulse_amplitude_pct: int   # 0-100, percentage of max actuator amplitude


def on_packet(
    config: CollarConfig,
    packet: PacketInput,
) -> ActuatorCommand:
    """
    Decide whether to pulse the actuator, given a received decision packet.

    Parameters
    ----------
    config : CollarConfig
        The collar's current configuration, set at pairing time.
    packet : PacketInput
        The decision packet the collar has just received.

    Returns
    -------
    ActuatorCommand
        The actuator command. If `pulse_duration_ms` is 0, the collar
        does not pulse.

    Notes
    -----
    The collar's decision tree is intentionally trivial:

      1. If session_id does not match config.paired_session_id: do not
         pulse. The packet is from a different session and is rejected.
      2. If seq is not strictly greater than the last seen seq: do not
         pulse. The packet is a replay or out of order.
      3. If ACTUATOR_EN flag is not set: do not pulse.
      4. If outcome is not OFF: do not pulse. Onside decisions do not
         trigger the actuator.
      5. If confidence is below config.confidence_threshold: do not
         pulse. The collar is configured to fall silent on uncertainty.
      6. If mode is INZAGHI_LEGACY: do not pulse. Silence is the design.
      7. Otherwise: pulse at the configured intensity for the configured
         duration.

    This stub does not implement the decision tree. It raises
    NotImplementedError. The signature is the documentation.
    """
    raise NotImplementedError(
        "feedback_stub is a reference signature, not an implementation. "
        "See src/README.md for the boundary this stub holds."
    )
