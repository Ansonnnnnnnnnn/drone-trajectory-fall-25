import typing as T
import math

import numpy as np

from src.data_model import Camera, DatasetSpec, Waypoint
from src.camera_utils import (
    compute_image_footprint_on_surface,
    compute_ground_sampling_distance,
)


def compute_distance_between_images(
    camera: Camera, dataset_spec: DatasetSpec
) -> np.ndarray:
    """Compute the distance between images in the horizontal and vertical directions for specified overlap and sidelap.

    Args:
        camera: Camera model used for image capture.
        dataset_spec: user specification for the dataset.

    Returns:
        The horizontal and vertical distance between images (as a 2-element array).
    """
    footprint = compute_image_footprint_on_surface(camera, dataset_spec.height)
    distance_x = footprint[0] * (1 - dataset_spec.overlap)
    distance_y = footprint[1] * (1 - dataset_spec.sidelap)
    return np.array([distance_x, distance_y])


def compute_speed_during_photo_capture(
    camera: Camera, dataset_spec: DatasetSpec, allowed_movement_px: float = 1
) -> float:
    """Compute the speed of drone during an active photo capture to prevent more than 1px of motion blur.

    Args:
        camera: Camera model used for image capture.
        dataset_spec: user specification for the dataset.
        allowed_movement_px: The maximum allowed movement in pixels. Defaults to 1 px.

    Returns:
        The speed at which the drone should move during photo capture.
    """
    gsd = compute_ground_sampling_distance(camera, dataset_spec.height)
    return (allowed_movement_px * gsd) / (dataset_spec.exposure_time_ms / 1000)


def generate_photo_plan_on_grid(
    camera: Camera, dataset_spec: DatasetSpec
) -> T.List[Waypoint]:
    """Generate the complete photo plan as a list of waypoints in a lawn-mower pattern.

    Args:
        camera: Camera model used for image capture.
        dataset_spec: user specification for the dataset.

    Returns:
        Scan plan as a list of waypoints.

    """
    max_distance = compute_distance_between_images(camera, dataset_spec)
    min_speed = compute_speed_during_photo_capture(camera, dataset_spec)
    waypoints = []
    x_points = math.ceil(dataset_spec.scan_dimension_x / max_distance[0])
    y_points = math.ceil(dataset_spec.scan_dimension_y / max_distance[1])
    curr_x = 0
    curr_y = 0
    for i in range(0, y_points):
        if i % 2 == 0:
            for j in range(0, x_points):
                waypoints.append(Waypoint(curr_x, curr_y, dataset_spec.height, min_speed))
                curr_x += max_distance[0]
            curr_y += max_distance[1]
            curr_x -= max_distance[0]
        else:
            for j in range(x_points):
                waypoints.append(Waypoint(curr_x, curr_y, dataset_spec.height, min_speed, math.pi))  # Facing backwards (180 degrees is pi radians)
                curr_x -= max_distance[0]
            curr_y += max_distance[1]
            curr_x += max_distance[0]
    return waypoints


def each_flight_time_computation(distance: float, max_speed: float, acceleration: float, start_speed: float, end_speed: float) -> float:
    """Compute the time required to fly a certain distance with given max_speed and acceleration constraints.

    Args:
        distance: The distance to be flown (in meters).
        max_speed: The maximum velocity of the drone (in m/s).
        acceleration: The acceleration and deceleration rate of the drone (in m/s^2).
        start_speed: The speed at the start of the segment (in m/s).
        end_speed: The speed at the end of the segment (in m/s).

    Returns:
        The time required to fly the given distance (in seconds).
    """
    if distance == 0:
        return 0.0
    time_to_accelerate = (max_speed - start_speed) / acceleration
    time_to_decelerate = (max_speed - end_speed) / acceleration
    distance_to_accelerate = (0.5 * (max_speed - start_speed) + start_speed) * time_to_accelerate
    distance_to_decelerate = (0.5 * (max_speed - end_speed) + end_speed) * time_to_decelerate
    if (distance_to_accelerate + distance_to_decelerate) >= distance:
        # If the distance is too short to reach maximum speed, just accelerate and then decelerate.
        peak_velocity = math.sqrt((2 * distance + (start_speed ** 2 / acceleration) + (end_speed ** 2 / acceleration)) / (2 / acceleration ))
        time_to_accelerate = (peak_velocity - start_speed) / acceleration
        time_to_decelerate = (peak_velocity - end_speed) / acceleration
        return time_to_accelerate + time_to_decelerate
    else:
        # Otherwise, we will accelerate to maximum speed, cruise, and then decelerate.
        distance_to_cruise = distance - distance_to_accelerate - distance_to_decelerate
        time_to_cruise = distance_to_cruise / max_speed
        return time_to_accelerate + time_to_cruise + time_to_decelerate


def full_flight_time_computation(camera: Camera, dataset_spec: DatasetSpec, velocity: float, acceleration: float):
    """Compute the total time required to complete the photo plan.

    Args:
        camera: Camera model used for image capture.
        dataset_spec: user specification for the dataset.
        velocity: The cruising velocity of the drone (in m/s).
        acceleration: The acceleration and deceleration rate of the drone (in m/s^2).

    Returns:
        The total time required to complete the photo plan (in seconds).
    """
    waypoints = generate_photo_plan_on_grid(camera, dataset_spec)
    total_time = 0.0
    times = [0]
    for i in range(1, len(waypoints)):
        start = waypoints[i - 1]
        end = waypoints[i]
        distance = math.sqrt((end.x - start.x) ** 2 + (end.y - start.y) ** 2 + (end.z - start.z) ** 2)
        new_time = each_flight_time_computation(distance, velocity, acceleration, start.speed, end.speed)
        times.append(new_time)
        total_time += new_time
    return times, total_time