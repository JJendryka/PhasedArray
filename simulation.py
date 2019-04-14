import math
from gl_backend import GLBackend
from user_interface import UserInterface


class Simulation:
    def __init__(self):
        self.frequency = 4e3
        self.speed = 343
        self.scale = 1
        self.spacing = 0.5
        self.width = 8
        self.height = 1
        self.offset_horizontal = math.pi / 3
        self.offset_vertical = 0
        self.color_range = 100
        self.z = 0
        self.plane = 'XY'

        self.user_interface = UserInterface(self)
        self.backend = GLBackend(
            self.user_interface.display, self.user_interface.keyboard)

        self.sources = []
        self.offsets = []
        self.generate_array()
        self.generate_offsets()

        self.upload_all()
        self.user_interface.start()

    def length(self):
        return self.speed / self.frequency

    def wavenumber(self):
        return 2*math.pi/self.length()

    def generate_array(self):
        self.sources = []
        for i in range(self.width):
            for j in range(self.height):
                self.sources.append(
                    [self.spacing*self.length()*(i-self.width/2), self.spacing*self.length()*(j-self.height/2), 0.0])

    def generate_offsets(self):
        self.offsets = []
        for i in range(self.width):
            for j in range(self.height):
                self.offsets.append(
                    [i*self.offset_vertical + j*self.offset_horizontal])

    def upload_all(self):
        self.generate_array()
        self.generate_offsets()

        self.backend.u_z(self.z)
        self.backend.u_sources(self.sources)
        self.backend.u_offsets(self.offsets)
        self.backend.u_scale(self.scale)
        self.backend.u_wavenumber(self.wavenumber())
        self.backend.u_color_range(self.color_range)
        self.backend.u_count(self.width * self.height)
        self.backend.u_plane(self.plane)


if __name__ == "__main__":
    s = Simulation()
