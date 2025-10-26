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

    def __init__(self, x, y, z, speed, yaw=0.0):
        self.x = x  # X coordinate of the waypoint (in meters)
        self.y = y  # Y coordinate of the waypoint (in meters)
        self.z = z  # Z coordinate of the waypoint (in meters)
        self.speed = speed  # Speed at the waypoint (in meters/second)
        self.yaw = yaw  # Yaw angle at the waypoint (in radians)
    
    def __repr__(self):
        return f"Waypoint(x={self.x}, y={self.y}, z={self.z}, speed={self.speed}, yaw={self.yaw})"
