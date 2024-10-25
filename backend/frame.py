import cv2
import numpy as np
import time_debug
from interface import SettingsStructure

Line_detection_threshold = 0


class Frame:
    global Line_detection_threshold
    frame_monochrom = None
    frame_filtered_3 = None
    frame_filtered_2 = None
    frame_filtered_1 = None
    frame_collapsed = None
    lines = None
    pixel_sums = None
    recursion_counter = 0

    red = np.array([np.uint8(0), np.uint8(0), np.uint8(255)])
    yellow = np.array([np.uint8(0), np.uint8(255), np.uint8(255)])
    white = np.array([np.uint8(255), np.uint8(255), np.uint8(255)])
    black = np.array([np.uint8(0), np.uint8(0), np.uint8(0)])

    resize = True

    def __init__(self, frame, settings: SettingsStructure, lines):
        self.brightness = 50
        self.settings = settings
        self.frame = frame# [settings.cam_settings.frame_cutout.min:settings.cam_settings.frame_cutout.max, :]
        time_debug.print_time("cutout frame")
        if self.resize:
            height, width, _ = self.frame.shape
            self.frame_height = 300
            self.frame_width = int(self.frame_height / height * width)
            if self.frame_width > 4096:
                self.frame_width = 4096
            self.frame = cv2.resize(self.frame, (self.frame_width, self.frame_height))

        self.frame = self.remove_fisheye(image=self.frame, strength=settings.fisheye/10)
        self.calculate_brightness()

        self.frame_height, self.frame_width, _ = self.frame.shape

        self.min_color = np.array([settings.colourFilter.hue.min,
                                   settings.colourFilter.saturation.min,
                                   settings.colourFilter.value.min])
        self.max_color = np.array([settings.colourFilter.hue.max,
                                   settings.colourFilter.saturation.max,
                                   settings.colourFilter.value.max])
        self.expected_lines = settings.lines
        self.line_detection_threshold = Line_detection_threshold
        self.lines = lines
        time_debug.print_time("finished initializing")

    def get_frame(self, with_rows=False, with_level=False, filter=None):
        if filter is None or filter == 'none':
            new_frame = self.frame.copy()
            if with_rows:
                new_frame = self.add_line(new_frame)
            if with_level:
                new_frame = self.overlay_number(new_frame)
            return new_frame
        elif filter == "mono":
            return self.get_frame_monochrom()
        elif filter == "filter_1":
            return self.get_frame_filtered_1()
        elif filter == "filter_2":
            return self.get_frame_filtered_2()
        elif filter == "pixel_counter":
            return self.get_frame_pixel_sums(with_rows=with_rows)
        print(f"Filter {filter} does not exist")
        return self.frame.copy()

    def calculate_brightness(self):
        """
        Calculate the overall brightness of an image represented as a numpy array.

        Parameters:
        image (numpy.ndarray): Image array with values in range [0, 255]
            Can be grayscale (2D) or RGB/RGBA (3D)

        Returns:
        float: Average brightness value between 0 (darkest) and 255 (brightest)
        """
        # Handle different image formats
        if len(self.frame.shape) == 3:  # RGB/RGBA image
            # Convert to grayscale using standard weights
            # Uses ITU-R BT.601 conversion formula: Y = 0.299 R + 0.587 G + 0.114 B
            grayscale = np.dot(self.frame[..., :3], [0.299, 0.587, 0.114])
        else:  # Already grayscale
            grayscale = self.frame

        # Calculate mean brightness
        self.brightness = np.mean(grayscale)

    def get_frame_monochrom(self):
        if self.frame_monochrom is not None:
            return self.frame_monochrom

        new_frame = cv2.cvtColor(self.get_frame(), cv2.COLOR_BGR2HSV)  # filter works better when using HSV color coding
        self.frame_monochrom = cv2.inRange(new_frame, self.min_color, self.max_color)
        time_debug.print_time("created monochrom frame")
        return self.frame_monochrom

    def get_frame_filtered_1(self):
        if self.frame_filtered_1 is not None:
            return self.frame_filtered_1

        frame = self.get_frame_monochrom()
        output = np.zeros_like(frame, dtype=np.uint8)
        for row in range(frame.shape[0]):
            diff = np.diff(frame[row], prepend=0, append=0)
            runs = np.where(diff != 0)[0].reshape(-1, 2)
            run_lengths = runs[:, 1] - runs[:, 0]
            valid_runs = runs[run_lengths > self.settings.filter_1]
            for start, end in valid_runs:
                output[row, start:end] = 255

        self.frame_filtered_1 = output
        time_debug.print_time("applied filter 1")
        return self.frame_filtered_1

    def get_frame_filtered_2(self):
        if self.frame_filtered_2 is not None:
            return self.frame_filtered_2
        frame = np.transpose(self.get_frame_filtered_1())
        output = np.zeros_like(frame, dtype=np.uint8)
        for row in range(frame.shape[0]):
            diff = np.diff(frame[row], prepend=0, append=0)
            runs = np.where(diff != 0)[0].reshape(-1, 2)
            run_lengths = runs[:, 1] - runs[:, 0]
            valid_runs = runs[run_lengths > self.settings.filter_2]
            for start, end in valid_runs:
                output[row, start:end] = 255

        self.frame_filtered_2 = np.transpose(output)
        time_debug.print_time("applied filter 2")

        return self.frame_filtered_2

    @staticmethod
    def remove_fisheye(image, strength=2.0):
        """
        Remove fisheye distortion from an image using a simple radial distortion model.

        Parameters:
        image (numpy.ndarray): Input image in numpy array format
        strength (float): Distortion correction strength (default 2.0)
                         Values between 1.5 and 3.0 usually work best

        Returns:
        numpy.ndarray: Corrected image without fisheye distortion
        """
        if strength == 0:
            return image

        # Get image dimensions
        height, width = image.shape[:2]
        center_x = width / 2
        center_y = height / 2

        # Create coordinate maps
        y, x = np.indices((height, width))

        # Calculate distance from center
        dx = (x - center_x) / center_x
        dy = (y - center_y) / center_y
        r = np.sqrt(dx ** 2 + dy ** 2)

        # Apply distortion correction
        # Using a modified equation that better preserves the image
        r_new = (1 / r) * np.arctan(r * strength) / strength

        # Handle the center point to avoid division by zero
        r_new[r == 0] = 1

        # Calculate new coordinates
        x_new = dx * r_new
        y_new = dy * r_new

        # Scale back to image coordinates
        x_new = (x_new * center_x + center_x).astype(np.float32)
        y_new = (y_new * center_y + center_y).astype(np.float32)

        # Apply the correction using cv2.remap
        corrected_image = cv2.remap(image, x_new, y_new,
                                    interpolation=cv2.INTER_LINEAR,
                                    borderMode=cv2.BORDER_CONSTANT,
                                    borderValue=(0, 0, 0))

        return corrected_image

    def get_frame_pixel_sums(self, with_rows=False):
        new_frame = np.zeros([self.frame_height, self.frame_width, 3], dtype=np.uint8)
        for index, pixel_row in enumerate(self.get_pixel_sums()):
            new_frame[index, : pixel_row] = self.white

        if with_rows:
            new_frame = self.add_line(new_frame)
            new_frame = self.add_threshold(new_frame)
        return new_frame

    def get_pixel_sums(self):
        if self.pixel_sums is not None:
            return self.pixel_sums
        self.pixel_sums = (np.sum(self.get_frame_filtered_2(), 1) / 255).astype(int)
        return self.pixel_sums

    def add_line(self, frame):
        if self.lines is None:
            return frame
        new_frame = frame.copy()
        for line in self.lines:
            new_line = np.zeros((5, self.frame_width, 3))
            new_line[:, :] = self.red
            y = line[0]
            start = max(0, y-1)
            end = min(self.frame_height, y + 1)
            new_frame[start:end] = new_line[:end - start]
        return new_frame

    def get_frame_collapsed(self):
        if self.frame_collapsed is not None:
            return self.frame_collapsed
        # array is normed to values between 0 and 100
        self.frame_collapsed = np.sum(self.get_frame_filtered_2(), 1) / 255 / self.frame_width * 100
        time_debug.print_time("got frame collapsed")
        return self.frame_collapsed

    def add_threshold(self, frame):
        new_frame = frame.copy()
        new_frame[0:self.frame_height,
        int((self.line_detection_threshold / 255) - 2): int((self.line_detection_threshold / 255) + 2)] = self.yellow
        return new_frame

    def overlay_number(self, frame):
        if self.lines is None:
            return frame

        thickness = 2
        font_scale = 1
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Colors
        red = (255, 100, 100)  # BGR format - Red for index
        white = (255, 255, 255)  # BGR format - White for value

        for index, line in enumerate(self.lines):
            # Split the text into two parts
            index_text = f'{index + 1}:'
            value_text = f'{int(line[1])}%'

            # Get the size of the index text to know where to start the value
            (index_width, _), _ = cv2.getTextSize(index_text, font, font_scale, thickness)

            # Position for the texts
            pos = [0, line[0]]

            # Draw index in red
            cv2.putText(frame, index_text, pos, font, font_scale, red, thickness, cv2.LINE_AA)

            # Draw value in white, starting after the index
            pos[0] += index_width
            cv2.putText(frame, value_text, pos, font, font_scale, white, thickness, cv2.LINE_AA)

        return frame

    @staticmethod
    def rotate_image(image, angle):
        # Get the image size
        height, width = image.shape[:2]

        # Calculate the rotation matrix
        center = (width / 2, height / 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

        # Perform the rotation
        rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

        return rotated_image


def process_chunk(args):
    chunk, filter_threshold = args
    output = np.zeros_like(chunk, dtype=np.uint8)
    for row in range(chunk.shape[0]):
        diff = np.diff(chunk[row], prepend=0, append=0)
        runs = np.where(diff != 0)[0].reshape(-1, 2)
        run_lengths = runs[:, 1] - runs[:, 0]
        valid_runs = runs[run_lengths > filter_threshold]
        for start, end in valid_runs:
            output[row, start:end] = 255
    return output
