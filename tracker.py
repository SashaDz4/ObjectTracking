import cv2
import numpy as np


class Tracker:
    def __init__(self, name, frame, shape=(640, 480)):
        self.name = name
        self.track = None
        self.trajectory = []
        self.img_size = shape
        self.last_update = 0
        self.color = tuple(np.random.randint(0, 255, (3,)).tolist())
        self.build(frame)

    def build(self, frame):
        self.track = cv2.legacy.TrackerMOSSE_create()
        frame = cv2.resize(frame, self.img_size)
        bbox = cv2.selectROI(f"tracker {self.name}", frame, False)
        self.trajectory.append((int(bbox[0] + bbox[2] / 2), int(bbox[1] + bbox[3] / 2)))
        self.track.init(frame, bbox)
        cv2.destroyWindow(f"tracker {self.name}")

    def __str__(self):
        return self.name

    def step(self, frame, count):
        bbox = self.update(frame)
        if bbox:
            self.last_update = count
            return self.draw_bbox(frame, bbox)
        else:
            return frame

    def update(self, frame):
        success, bbox = self.track.update(frame)
        success = self.check_valid_bbox(bbox)
        if success:
            self.trajectory.append((int(bbox[0] + bbox[2] / 2), int(bbox[1] + bbox[3] / 2)))
            return bbox
        else:
            return None

    def draw_bbox(self, frame, bbox):
        x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), self.color, 2)
        # add name to the bbox Object name
        cv2.putText(frame, f"object: {self.name}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)
        for i in range(1, len(self.trajectory)):
            if self.trajectory[i] == (0, 0):
                continue
            cv2.line(frame, self.trajectory[i - 1], self.trajectory[i], self.color, 1)
        return frame

    def check_valid_bbox(self, bbox):
        if bbox is None:
            return False
        x, y, w, h = bbox
        if x < 0 or y < 0 or x + w > self.img_size[0] or y + h > self.img_size[1]:
            return False
        return True

