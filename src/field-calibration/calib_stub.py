"""
Pitch calibration stub — homography recovery.

This is a reference function signature for the homography layer of
OffsideFence. It is NOT an implementation.

The real layer would:
  - consume per-frame pitch keypoint detections (image coordinates),
  - match them to known pitch landmarks (3D pitch coordinates),
  - recover a per-frame homography transform from image space to top-down
    pitch coordinates,
  - apply RANSAC to reject misdetected keypoints,
  - apply temporal smoothing across frames to suppress jitter.

This stub raises NotImplementedError by design.
"""

from dataclasses import dataclass
from typing import Sequence

import numpy as np  # type annotation only; not used in the stub body


@dataclass(frozen=True)
class ImageKeypoint:
    """A detected pitch keypoint in broadcast-frame image coordinates."""
    image_xy: tuple[float, float]   # (x, y) in pixel space
    pitch_3d: tuple[float, float, float]  # (x, y, z) in pitch space, meters
    confidence: float               # 0.0 – 1.0


@dataclass(frozen=True)
class Homography:
    """A 3x3 homography transform from image space to top-down pitch space."""
    matrix: np.ndarray  # shape (3, 3), dtype float64
    inlier_count: int
    reprojection_error_px: float


def recover_homography(
    keypoints: Sequence[ImageKeypoint],
    min_inliers: int = 6,
    max_reproj_error_px: float = 4.0,
) -> Homography | None:
    """
    Recover a homography from image keypoints to pitch coordinates.

    Parameters
    ----------
    keypoints : Sequence[ImageKeypoint]
        Detected pitch keypoints from a single broadcast frame. In a real
        implementation, this would be the output of the Roboflow Sports
        pitch_keypoint_estimation module.
    min_inliers : int
        Minimum number of inlier keypoints required to accept the
        recovered homography. Below this threshold, the function returns
        None and the tactical state engine falls silent for the frame.
    max_reproj_error_px : int
        Maximum allowed reprojection error, in pixels, for an inlier.
        Keypoints with error above this threshold are rejected.

    Returns
    -------
    Homography | None
        The recovered homography, or None if the keypoint set is
        insufficient or too noisy.

    Notes
    -----
    A real implementation would call OpenCV's `findHomography` with
    `method=cv2.RANSAC`, then apply the inlier mask to compute the
    inlier count and the reprojection error. The result would be
    temporally smoothed across frames (e.g., exponential moving average
    on the matrix elements) to suppress per-frame jitter.

    This stub does not call OpenCV. It does not implement RANSAC. It
    raises NotImplementedError. The signature is the documentation.
    """
    raise NotImplementedError(
        "calib_stub is a reference signature, not an implementation. "
        "See src/README.md for the boundary this stub holds."
    )
