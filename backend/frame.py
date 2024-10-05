import cv2
import numpy as np
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
        self.settings = settings
        # frame = self.rotate_image(frame, 6)
        #k1 = -settings.fisheye / 1000
        #k2 = 0.1
        #p1 = 0.0
        #p2 = 0.0
        #frame = self.remove_fisheye(frame, k1, k2, p1, p2)
        self.frame = frame[settings.frame_cutout.min:settings.frame_cutout.max, :]

        if self.resize:
            height, width, _ = self.frame.shape
            self.frame_height = 300
            self.frame_width = int(self.frame_height / height * width)
            if self.frame_width > 4096:
                self.frame_width = 4096
            self.frame = cv2.resize(self.frame, (self.frame_width, self.frame_height))
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

    @staticmethod
    def remove_fisheye(img, k1, k2, p1, p2):

        # Get image dimensions
        h, w = img.shape[:2]

        # Define camera matrix
        # Assuming the focal length is half of the image width and the center point is the image center
        focal_length = w / 2
        center = (w / 2, h / 2)
        camera_matrix = np.array(
            [[focal_length, 0, center[0]],
             [0, focal_length, center[1]],
             [0, 0, 1]], dtype=np.float32
        )
        # Define distortion coefficients
        dist_coeffs = np.array([k1, k2, p1, p2, 0], dtype=np.float32)

        # Generate new camera matrix
        new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, (w, h), 1, (w, h))

        # Undistort the image
        dst = cv2.undistort(img, camera_matrix, dist_coeffs, None, new_camera_matrix)

        # Crop the image
        x, y, w, h = roi
        dst = dst[y:y + h, x:x + w]

        return dst

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

    def get_frame_monochrom(self):
        if self.frame_monochrom is not None:
            return self.frame_monochrom
        new_frame = cv2.cvtColor(self.get_frame(), cv2.COLOR_BGR2HSV)  # filter works better when using HSV color coding
        self.frame_monochrom = cv2.inRange(new_frame, self.min_color, self.max_color)
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
        return self.frame_filtered_2

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
            start = max(0, y - 2)
            end = min(self.frame_height, y + 3)
            new_frame[start:end] = new_line[:end - start]
        return new_frame

    def get_frame_collapsed(self):
        if self.frame_collapsed is not None:
            return self.frame_collapsed
        # array is normed to values between 0 and 100
        self.frame_collapsed = np.sum(self.get_frame_filtered_2(), 1) / 255 / self.frame_width * 100
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
        color = (255, 255, 255)
        font_scale = 1
        # Convert the number to string

        # Define the font
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Put the text on the image
        for index, line in enumerate(self.lines):
            text = f'{index+1}:{int(line[1])}%'
            cv2.putText(frame, text, [0, line[0]], font, font_scale, color, thickness, cv2.LINE_AA)

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
