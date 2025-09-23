"""Data models for the camera and user specification."""


class DatasetSpec:
    """
    Data model for specifications of an image dataset.
    """

    pass


class Camera:
    """
    Data model for a simple pinhole camera.

    References:
    - https://github.com/colmap/colmap/blob/3f75f71310fdec803ab06be84a16cee5032d8e0d/src/colmap/sensor/models.h#L220
    - https://en.wikipedia.org/wiki/Pinhole_camera_model
    """

    def __init__(self, fx=4938.56, fy=4936.49, cx=4095.5, cy=3071.5, 
                 sensor_size_x_mm=13.107, sensor_size_y_mm=9.830,
                 image_size_x=8192, image_size_y=6144): # Default values for Skydio VT300L
        self.fx = fx  # Focal length along x axis (in pixels)
        self.fy = fy  # Focal length along y axis (in pixels)
        self.cx = cx  # Optical center of the image along the x axis (in pixels)
        self.cy = cy  # Optical center of the image along the y axis (in pixels)
        self.sensor_size_x_mm = sensor_size_x_mm  # single pixel size * number of pixels in X dimension
        self.sensor_size_y_mm = sensor_size_y_mm  # single pixel size * number of pixels in Y dimension
        self.image_size_x = image_size_x  # Number of pixels in the image along the x axis
        self.image_size_y = image_size_y  # Number of pixels in the image along the y axis


class Waypoint:
    """
    Waypoints are positions where the drone should fly to and capture a photo.
    """

    pass
