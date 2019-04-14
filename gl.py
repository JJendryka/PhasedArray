import sys
import ctypes
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
import math
import time

RESOLUTION = (512, 512)
FREQUENCY = 4000
SPEED = 343
SIZE = 1
COUNT = 8
OFFSET = math.pi / 3
SPACING = 0.5

length = SPEED/FREQUENCY

frames = 0
time_start = 0


def position_sources():
    s = []
    for i in range(COUNT):
        s.append([0.0, float(i)*length*SPACING - length*SPACING*COUNT/2])
    return np.array(s, np.float32)


def prepare_program():
    vertex_code = open("s.vert.glsl").read()
    fragment_code = open("s.frag.glsl").read()
    fragment_code = fragment_code.replace("666", str(COUNT))

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


def display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, 4)
    glut.glutSwapBuffers()
    global frames
    if frames == 0:
        global time_start
        time_start = time.clock()
    frames += 1
    print(frames/(time.clock() - time_start))


def reshape(width, height):
    gl.glViewport(0, 0, width, height)
    global RESOLUTION
    RESOLUTION = (width, height)
    l_resolution = gl.glGetUniformLocation(program, 'resolution')
    gl.glUniform2f(l_resolution, float(RESOLUTION[0]), float(RESOLUTION[1]))


def keyboard(key, x, y):
    if key == b'\x1b':
        sys.exit()


def timer(v):
    glut.glutPostRedisplay()
    glut.glutTimerFunc(16, timer, 0)


def init_glut():
    glut.glutInit()
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
    glut.glutCreateWindow('')
    glut.glutReshapeWindow(RESOLUTION[0], RESOLUTION[1])
    glut.glutReshapeFunc(reshape)
    glut.glutDisplayFunc(display)
    glut.glutKeyboardFunc(keyboard)
    glut.glutTimerFunc(0, timer, 0)


def prepare_data():
    data = np.zeros(4, [("position", np.float32, 2)])
    data['position'] = (-1, 1),   (-1, -1),   (+1, +1),   (1, -1)
    return data


init_glut()
program = prepare_program()
data = prepare_data()


# Build buffer
# --------------------------------------

# Request a buffer slot from GPU
buffer = gl.glGenBuffers(1)

# Make this buffer the default one
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)

# Upload data
gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_DYNAMIC_DRAW)


# Bind attributes
# --------------------------------------
stride = data.strides[0]
offset = ctypes.c_void_p(0)
loc = gl.glGetAttribLocation(program, "position")
gl.glEnableVertexAttribArray(loc)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
gl.glVertexAttribPointer(loc, 2, gl.GL_FLOAT, False, stride, offset)


sources = position_sources()

# Bind uniforms
print(sources)

l_resolution = gl.glGetUniformLocation(program, 'resolution')
gl.glUniform2f(l_resolution, float(RESOLUTION[0]), float(RESOLUTION[1]))
l_sources = gl.glGetUniformLocation(program, 'sources')
gl.glUniform2fv(l_sources, COUNT, sources)
l_offsets = gl.glGetUniformLocation(program, 'offsets')
gl.glUniform1fv(l_offsets, COUNT, np.zeros(COUNT))
l_wavenumber = gl.glGetUniformLocation(program, 'wavenumber')
gl.glUniform1f(l_wavenumber, 2 * math.pi/length)
l_scale = gl.glGetUniformLocation(program, 'scale')
gl.glUniform1f(l_scale, SIZE)


# Enter mainloop
# --------------------------------------
glut.glutMainLoop()
