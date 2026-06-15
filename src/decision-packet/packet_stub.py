"""
OFP/0.1 decision packet stub — encoder and decoder.

This is a reference implementation of the packet format described in
`spec/ofp-protocol.md`. It is NOT a working implementation.

The encoder takes a DecisionPacket dataclass and returns 20 bytes.
The decoder takes 20 bytes and returns a DecisionPacket dataclass.

A real implementation would:
  - pack fields in big-endian order,
  - validate the version byte,
  - validate the session_id and seq fields,
  - validate the mode byte against the registered enum,
  - apply DTLS encryption on the wire (out of scope for this stub).

This stub raises NotImplementedError by design.
"""

from dataclasses import dataclass
from enum import Enum


class Mode(Enum):
    """Operating mode of the haptic tactical correction collar."""
    TRAINING = 0x01
    MATCH = 0x02
    DARWIN = 0x03
    INZAGHI_LEGACY = 0x04


class DecisionOutcome(Enum):
    """Outcome of a single decision evaluation."""
    NONE = 0x00
    ON = 0x01
    OFF = 0x02


@dataclass(frozen=True)
class DecisionPacket:
    """The 20-byte decision packet sent over the OFP/0.1 wire."""
    version: int           # uint8, currently 0x01
    flags: int             # uint8 bitfield (bit 0: ACTUATOR_EN, bit 1: BATT_LOW, bit 2: LINK_TEST)
    session_id: int        # uint16
    timestamp_ns: int      # uint64, nanoseconds since Unix epoch
    mode: Mode             # uint8
    outcome: DecisionOutcome  # uint8
    confidence: int        # uint8, 0-255 (scaled from float 0.0-1.0)
    intensity: int         # uint8, 0-255
    repeat_count: int      # uint8, 0-255
    seq: int               # uint16


PACKET_SIZE_BYTES = 20


def encode_packet(packet: DecisionPacket) -> bytes:
    """
    Encode a DecisionPacket into 20 bytes, big-endian, OFP/0.1 wire format.

    See `spec/ofp-protocol.md` §2.1 for the binary layout.
    """
    raise NotImplementedError(
        "packet_stub.encode_packet is a reference signature, not an "
        "implementation. See src/README.md for the boundary this stub holds."
    )


def decode_packet(raw: bytes) -> DecisionPacket:
    """
    Decode 20 bytes of OFP/0.1 wire format into a DecisionPacket.

    See `spec/ofp-protocol.md` §2.1 for the binary layout.
    """
    raise NotImplementedError(
        "packet_stub.decode_packet is a reference signature, not an "
        "implementation. See src/README.md for the boundary this stub holds."
    )
