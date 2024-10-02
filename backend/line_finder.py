class LineFinder:
    line_count = None
    lines = None
    frame = None

    def update(self, frame, lines):
        if self.line_count != lines:
            self.line_count = lines
            self.create_default()
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

    def update_line_values(self):
        self.lines = [[x[0], self.frame[x[0]]] for x in self.lines]

    def update_line_positions(self):
        filter_constant = 3 # in %
        detected_lines = []
        last_valley = [0, 0]
        last_hill = [0, 0]
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
            # print(f'detected {len(detected_lines)}. Ignoring the smallest one')
            detected_lines = sorted(detected_lines, reverse=True, key=lambda x: self.frame[x])[:self.line_count]
        else:
            # print(f'detected {len(detected_lines)} from {self.line_count} lines')
            pass
        detected_lines = sorted(detected_lines)

        mapped = self.map_lists([[x, y] for x, y in enumerate([x[0] for x in self.lines])],
                                [[x, y] for x, y in enumerate(detected_lines)])
        mapped = [[x['orig_index_old'], x['orig_index_new']] for x in mapped]

        for line in mapped:
            if self.lines[line[0]][0] > detected_lines[line[1]]:
                self.lines[line[0]][0] -= 1
            elif self.lines[line[0]][0] < detected_lines[line[1]]:
                self.lines[line[0]][0] += 1
        return self.lines

    def map_lists(self, old_list, new_list):
        if len(old_list) == 0 or len(new_list) == 0:
            return []

        new_lines = [{'position': position,
                      'min': index,
                      'max': len(old_list) - len(new_list) + index}
                     for index, position in enumerate(new_list)]

        best_fits = []
        for index, line in enumerate(new_lines):
            best_fit = min(range(line['min'], line['max'] + 1),
                           key=lambda i: abs(old_list[i][1] - new_list[index][1]))
            best_fits.append({'index_new': index,
                              'index_old': best_fit,
                              'orig_index_new': new_list[index][0],
                              'orig_index_old': old_list[best_fit][0],
                              'diff': abs(old_list[best_fit][1] - new_list[index][1])})

        best_fits = sorted(best_fits, key=lambda x: x['diff'])
        defined_item = best_fits[0]
        upper_old = old_list[:defined_item['index_old']]
        upper_new = new_list[:defined_item['index_new']]
        lower_old = old_list[defined_item['index_old'] + 1:]
        lower_new = new_list[defined_item['index_new'] + 1:]
        return_value = self.map_lists(upper_old, upper_new) + [defined_item] + self.map_lists(lower_old, lower_new)
        return return_value

    def create_default(self):
        if self.frame is None:
            return
        if self.line_count is None:
            self.line_count = 6
        positions = [int(self.frame.shape[0] / self.line_count * x
                         + (self.frame.shape[0] / self.line_count / 2))
                     for x in range(self.line_count)]
        self.lines = [[x, 0] for x in positions]
