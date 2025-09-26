"""Data models for the camera and user specification."""


class DatasetSpec:
    """
    Data model for specifications of an image dataset.
    """

    def __init__(self, overlap, sidelap, height, scan_dimension_x, scan_dimension_y, exposure_time_ms):
        self.overlap = overlap  # The ratio (in 0 to 1) of scene shared between two consecutive images
        self.sidelap = sidelap  # The ratio (in 0 to 1) of scene shared between two images in adjacent rows
        self.height = height  # The height of the scan above the ground (in meters)
        self.scan_dimension_x = scan_dimension_x  # The horizontal size of the rectangle to be scanned (in meters)
        self.scan_dimension_y = scan_dimension_y  # The vertical size of the rectangle to be scanned (in meters)
        self.exposure_time_ms = exposure_time_ms  # The exposure time for each image (in milliseconds)


class Camera:
    """
    Data model for a simple pinhole camera.

    References:
    - https://github.com/colmap/colmap/blob/3f75f71310fdec803ab06be84a16cee5032d8e0d/src/colmap/sensor/models.h#L220
    - https://en.wikipedia.org/wiki/Pinhole_camera_model
    """

    pass


class Waypoint:
    """
    Waypoints are positions where the drone should fly to and capture a photo.
    """

    pass
