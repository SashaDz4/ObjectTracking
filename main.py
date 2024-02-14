from video import VideoTracker

source = "output.avi" # 0 for webcam, or path to video file
app = VideoTracker(source, shape=(1280, 720))
app.root.mainloop()
