import numpy as np


class LineFinder:
    line_count = None
    lines = None
    frame = None

    def update(self, frame):
        self.frame = frame

    def get_lines(self):
        if self.frame is None:
            return None
        if self.lines is None:
            self.create_default()
        self.update_line_positions()
        self.update_line_values()
        return self.lines

    def get_line_values(self):
        if self.lines is None:
            self.create_default()
        return [x[1] for x in self.lines]

    def update_line_count(self, line_count):
        self.line_count = line_count

    def update_line_values(self):
        self.lines = [[x[0], self.frame[x[0]]] for x in self.lines]

    def update_line_positions(self):
        filter_constant = 10
        detected_lines = []
        last_valley = [0, 0]
        last_hill = [0, 0]
        position = 0
        waiting_for_hill = True
        for index, value in enumerate(self.frame):
            if waiting_for_hill:
                if value > last_hill[1]:
                    last_hill = [index, value]
                if last_hill[1] > value + filter_constant:
                    detected_lines.append(last_hill[0])
                    last_valley = [index, value]
                    waiting_for_hill = False
            else:
                if value < last_valley[1]:
                    last_valley = [index, value]
                if last_valley[1] < value - filter_constant:
                    last_hill = [index, value]
                    waiting_for_hill = True

        if len(detected_lines) > self.line_count:
            print(f'detected {len(detected_lines)}. Ignoring the smallest one')
            detected_lines = sorted(detected_lines, reverse=True, key=lambda x: self.frame[x])[:self.line_count]
        detected_lines = sorted(detected_lines)
        # --------------------------------------
        # --------------------------------------
        # ab hier ist müll
        # --------------------------------------
        # --------------------------------------
        current_lines = [x[0] for x in self.lines]
        for index_detected, line in enumerate(detected_lines):
            for x in range(len(current_lines)):
                if x < index_detected:
                    continue
                index = min(range(len(current_lines) - index_detected),
                            key=lambda i: abs(current_lines[i + index_detected] - line))
                if current_lines[index] > line:
                    current_lines[index] -= 1
                else:
                    current_lines[index] += 1



        for index, value in enumerate(current_lines):
            self.lines[index][0] = value
        print(f'current line poitions{current_lines}, detected lines {len(detected_lines)}')














        return

        current_line_positions = [x[0] for x in self.lines]
        for line in detected_lines:
            index = min(range(len(current_line_positions)), key=lambda i: abs(current_line_positions[i] - line))
            if abs(current_line_positions[index] - line) < 20:
                if current_line_positions[index] > line:
                    current_line_positions[index] -= 1
                else:
                    current_line_positions[index] += 1
        for index, value in enumerate(current_line_positions):
            self.lines[index][0] = value
        print(self.lines)





    def create_default(self):
        self.line_count = 6
        positions = [int(self.frame.shape[0] / self.line_count * x
                         + (self.frame.shape[0] / self.line_count / 2))
                     for x in range(self.line_count)]
        self.lines = [[x, 0] for x in positions]
