import sys
import ctypes
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
import math
import time


class GLBackend():
    def __init__(self, display_callback, keyboard_callback):
        self.display_callback = display_callback
        self.keyboard_callback = keyboard_callback
        self.resolution = (512, 512)
        self.init_glut()
        self.program = self.prepare_program()
        self.data = self.prepare_data()
        self.upload_data()

    def start(self):
        glut.glutMainLoop()

    def display(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, 4)
        glut.glutSwapBuffers()
        self.display_callback()

    def reshape(self, width, height):
        gl.glViewport(0, 0, width, height)
        self.resolution = (width, height)
        self.u_resolution()

    def keyboard(self, key, x, y):
        if key == b'\x1b':
            sys.exit()
        self.keyboard_callback(key, x, y)

    def u_resolution(self):
        l_resolution = gl.glGetUniformLocation(self.program, 'resolution')
        gl.glUniform2f(l_resolution, float(
            self.resolution[0]), float(self.resolution[1]))

    def u_sources(self, sources):
        l_sources = gl.glGetUniformLocation(self.program, 'sources')
        gl.glUniform3fv(l_sources, len(sources), np.array(sources))

    def u_offsets(self, offsets):
        l_offsets = gl.glGetUniformLocation(self.program, 'offsets')
        gl.glUniform1fv(l_offsets, len(offsets), np.array(offsets))

    def u_wavenumber(self, wavenumber):
        l_wavenumber = gl.glGetUniformLocation(self.program, 'wavenumber')
        gl.glUniform1f(l_wavenumber, wavenumber)

    def u_scale(self, scale):
        l_scale = gl.glGetUniformLocation(self.program, 'scale')
        gl.glUniform1f(l_scale, scale)

    def u_color_range(self, color_range):
        l_color_range = gl.glGetUniformLocation(self.program, 'color_range')
        gl.glUniform1f(l_color_range, color_range)

    def u_count(self, count):
        l_count = gl.glGetUniformLocation(self.program, 'count')
        gl.glUniform1i(l_count, count)

    def u_z(self, z):
        l_z = gl.glGetUniformLocation(self.program, 'z')
        gl.glUniform1f(l_z, z)

    def u_plane(self, plane):
        l_xy_plane = gl.glGetUniformLocation(self.program, 'xy_plane')
        l_xz_plane = gl.glGetUniformLocation(self.program, 'xz_plane')
        if plane == "XY":
            gl.glUniform1i(l_xy_plane, True)
            gl.glUniform1i(l_xz_plane, False)
        elif plane == "XZ":
            gl.glUniform1i(l_xy_plane, False)
            gl.glUniform1i(l_xz_plane, True)
        else:
            gl.glUniform1i(l_xy_plane, False)
            gl.glUniform1i(l_xz_plane, False)

    def timer(self, v):
        glut.glutPostRedisplay()
        glut.glutTimerFunc(16, self.timer, 0)

    def init_glut(self):
        glut.glutInit()
        glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
        glut.glutCreateWindow('')
        glut.glutReshapeWindow(self.resolution[0], self.resolution[1])
        glut.glutReshapeFunc(self.reshape)
        glut.glutDisplayFunc(self.display)
        glut.glutKeyboardFunc(self.keyboard)
        glut.glutTimerFunc(0, self.timer, 0)

    def prepare_data(self):
        data = np.zeros(4, [("position", np.float32, 2)])
        data['position'] = (-1, 1),   (-1, -1),   (+1, +1),   (1, -1)
        return data

    def prepare_program(self):
        vertex_code = open("s.vert.glsl").read()
        fragment_code = open("s.frag.glsl").read()

        program = gl.glCreateProgram()
        vertex = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        fragment = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

        # Set shaders source
        gl.glShaderSource(vertex, vertex_code)
        gl.glShaderSource(fragment, fragment_code)

        # Compile shaders
        gl.glCompileShader(vertex)
        if not gl.glGetShaderiv(vertex, gl.GL_COMPILE_STATUS):
            error = gl.glGetShaderInfoLog(vertex).decode()
            print(error)
            raise RuntimeError("Vertex shader compilation error")

        gl.glCompileShader(fragment)
        gl.glCompileShader(fragment)
        if not gl.glGetShaderiv(fragment, gl.GL_COMPILE_STATUS):
            error = gl.glGetShaderInfoLog(fragment).decode()
            print(error)
            raise RuntimeError("Fragment shader compilation error")

        # Attach shader objects to the program
        gl.glAttachShader(program, vertex)
        gl.glAttachShader(program, fragment)

        # Build program
        gl.glLinkProgram(program)
        if not gl.glGetProgramiv(program, gl.GL_LINK_STATUS):
            print(gl.glGetProgramInfoLog(program))
            raise RuntimeError('Linking error')

        # Get rid of shaders (no more needed)
        gl.glDetachShader(program, vertex)
        gl.glDetachShader(program, fragment)

        # Make program the default program
        gl.glUseProgram(program)

        return program

    def upload_data(self):
        buffer = gl.glGenBuffers(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)

        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.data.nbytes,
                        self.data, gl.GL_DYNAMIC_DRAW)

        stride = self.data.strides[0]
        offset = ctypes.c_void_p(0)
        loc = gl.glGetAttribLocation(self.program, "position")
        gl.glEnableVertexAttribArray(loc)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
        gl.glVertexAttribPointer(loc, 2, gl.GL_FLOAT, False, stride, offset)
