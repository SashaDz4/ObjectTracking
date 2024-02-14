import cv2
import tkinter as tk
from PIL import Image, ImageTk

from tracker import Tracker


class VideoTracker:
    def __init__(self, video_source=0, shape=(640, 480)):
        self.photo = None
        self.shape = shape
        self.root = tk.Tk()
        self.root.title("Video Tracker")

        self.video_source = video_source
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(self.root, width=shape[0], height=shape[1])
        self.canvas.pack()

        self.btn_start = tk.Button(self.root, text="Start", width=10, command=self.start_video)
        self.btn_pause = tk.Button(self.root, text="Pause", width=10, command=self.pause_video)
        self.btn_add_object = tk.Button(self.root, text="Add Object", width=10, command=self.add_object)

        self.btn_start.pack(side=tk.RIGHT, padx=5, pady=5)
        self.btn_pause.pack(side=tk.RIGHT, padx=5, pady=5)
        self.btn_add_object.pack(side=tk.RIGHT, padx=5, pady=5)

        self.delay = 10
        self.paused = False
        self.trackers = []
        self.count = 0
        self.update()

        self.root.mainloop()

    def start_video(self):
        if not self.vid.isOpened():
            self.vid = cv2.VideoCapture(self.video_source)
            self.paused = False

    def pause_video(self):
        self.paused = not self.paused

    def add_object(self):
        self.paused = True
        # last tracker name + 1
        tracker_name = str(int(self.trackers[-1].name) + 1) if self.trackers else "0"
        self.trackers.append(Tracker(tracker_name, self.vid.read()[1], self.shape))
        self.paused = False

    def update(self):
        if not self.paused:
            ret, frame = self.vid.read()
            remove_trackers = []
            for tracker in self.trackers:
                frame = tracker.step(frame, self.count)
                if self.count - tracker.last_update > 10:
                    remove_trackers.append(tracker)

            for tracker in remove_trackers:
                self.trackers.remove(tracker)
            if ret:
                frame = cv2.resize(frame, self.shape)
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
                self.count += 1
        self.root.after(self.delay, self.update)


if __name__ == "__main__":
    app = VideoTracker("output.avi")
