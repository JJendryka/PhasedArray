import matplotlib
import matplotlib.pyplot as plt
import matplotlib.widgets as wdg
import OpenGL.GLUT as glut
import math


class UserInterface():
    def __init__(self, simulation):
        self.simulation = simulation

        self.fig = plt.figure()
        self.scale_axes = plt.axes([0.25, 0.90, 0.65, 0.03])
        self.scale_slider = wdg.Slider(
            self.scale_axes, "Scale", 0.01, 16, valinit=1)
        self.h_offset_axes = plt.axes([0.25, 0.80, 0.65, 0.03])
        self.h_offset_slider = wdg.Slider(
            self.h_offset_axes, "Horizontal offset", -math.pi, math.pi, valinit=0)
        self.v_offset_axes = plt.axes([0.25, 0.70, 0.65, 0.03])
        self.v_offset_slider = wdg.Slider(
            self.v_offset_axes, "Vertical offset", -math.pi, math.pi, valinit=0)
        self.color_range_axes = plt.axes([0.25, 0.60, 0.65, 0.03])
        self.color_range_slider = wdg.Slider(
            self.color_range_axes, "Color range", 0, 200, valinit=100)
        self.width_axes = plt.axes([0.25, 0.50, 0.65, 0.03])
        self.width_slider = wdg.Slider(
            self.width_axes, "Width", 0, 100, valinit=8, valstep=1)
        self.height_axes = plt.axes([0.25, 0.40, 0.65, 0.03])
        self.height_slider = wdg.Slider(
            self.height_axes, "Height", 0, 100, valinit=1, valstep=1)
        self.z_axes = plt.axes([0.25, 0.30, 0.65, 0.03])
        self.z_slider = wdg.Slider(
            self.z_axes, "z", -2, 2, valinit=0)
        self.plane_axes = plt.axes([0.25, 0.1, 0.15, 0.15])
        self.plane_radio = wdg.RadioButtons(
            self.plane_axes, ('XY', 'XZ', 'YZ'))

    def start(self):
        plt.ion()
        plt.show()
        while True:
            glut.glutMainLoopEvent()
            self.simulation.scale = self.scale_slider.val
            self.simulation.offset_horizontal = self.h_offset_slider.val
            self.simulation.offset_vertical = self.v_offset_slider.val
            self.simulation.color_range = self.color_range_slider.val
            self.simulation.width = int(self.width_slider.val)
            self.simulation.height = int(self.height_slider.val)
            self.simulation.z = self.z_slider.val
            self.simulation.plane = self.plane_radio.value_selected
            self.simulation.upload_all()
            self.fig.canvas.draw()
            plt.pause(0.0001)

    def display(self):
        pass

    def keyboard(self, k, x, y):
        pass
