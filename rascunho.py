import cv2
import tkinter as tk
from customtkinter import CTkImage

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.camera_on = False

        self.frame_left = tk.Frame(self.root)
        self.frame_left.pack()

        self.ctk_image = CTkImage(master=self.frame_left)
        self.ctk_image.pack()

        self.button = tk.Button(
            master=self.frame_left,
            text="Câmera",
            command=self.open_camera
        )
        self.button.pack()

    def open_camera(self):
        if not self.camera_on:
            self.camera_on = True
            self.vid = cv2.VideoCapture(0)  # Open the camera

            self.show_next_frame()
        else:
            self.camera_on = False
            self.ctk_image.clear_image()
            self.vid.release()

    def show_next_frame(self):
        if self.camera_on:
            ret, frame = self.vid.read()
            if ret:
                opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                self.ctk_image.set_image(opencv_image)
                self.root.after(10, self.show_next_frame)

root = tk.Tk()
app = CameraApp(root)
root.mainloop()