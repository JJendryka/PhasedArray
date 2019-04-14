import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from math import sin, cos, pi
import math

COUNT = 16
FREQUENCY = 4e3
SPACING = 0.5
SPEED = 343
SIZE = 5
RESOLUTION = 256
TIME = 1
OFFSET = 0
POWER = 1 / COUNT

length = SPEED/FREQUENCY
SOURCES = []


def update_offset(offset):
    global OFFSET
    global SOURCES
    OFFSET = offset
    for i in range(COUNT):
        SOURCES[i][2] = offset * i


def update_count(count):
    global COUNT
    global POWER
    global SOURCES
    POWER = 1 / COUNT
    COUNT = count
    SOURCES = []
    for i in range(COUNT):
        SOURCES.append([-0.1, i * length * SPACING - length *
                        SPACING * COUNT / 2, OFFSET * i])


def distance(x0, y0, x1, y1):
    return math.sqrt((x0 - x1)**2 + (y0 - y1)**2)


def phase(source, x, y):
    dist = distance(source[0], source[1], x, y)
    phase = 2 * pi / length * dist + source[2]
    return phase


def amplitute(source, x, y):
    dist = distance(source[0], source[1], x, y)
    return POWER/dist


def amplitute_sum(x, y):
    return math.sqrt(sum(sin(phase(source, x, y)) * amplitute(source, x, y) for source in SOURCES)
                     ** 2 + sum(cos(phase(source, x, y)) * amplitute(source, x, y) for source in SOURCES)**2)


# data = np.zeros(shape=(RESOLUTION, RESOLUTION))
# for x in range(RESOLUTION):
#     for y in range(RESOLUTION):
#         data[x][y] = amplitute_sum(
#             x * SIZE / RESOLUTION, y * SIZE / RESOLUTION)

# plt.imshow(data, cmap="viridis", interpolation="nearest",
#            extent=[0, SIZE, 0, SIZE], norm=matplotlib.colors.LogNorm())
# plt.show()

DISTANCE = 30
RES_INTENSITY = 2048


def calc_intensity():
    intensity = []
    angles = []
    for i in range(RES_INTENSITY):
        angle = 2 * i * pi / RES_INTENSITY
        intensity.append(amplitute_sum(
            sin(angle) * DISTANCE, cos(angle) * DISTANCE))
        angles.append(angle)

    return angles, intensity


def power_in_slice(angle, slice, intensity, angles):
    power_in = 0
    power_out = 0
    for j in range(len(angles)):
        if -SLICE/2 < angles[j] - angle < SLICE/2:
            power_in += intensity[j]
        else:
            power_out += intensity[j]
    return power_in/(power_in + power_out)


if __name__ == "__main__":
    update_count(8)

    ''' 2D Calculation '''

    # data = np.zeros(shape=(RESOLUTION, RESOLUTION))
    # for x in range(RESOLUTION):
    #     for y in range(RESOLUTION):
    #         data[x][y] = amplitute_sum(
    #             x * SIZE / RESOLUTION, y * SIZE / RESOLUTION)

    # plt.imshow(data, cmap="viridis", interpolation="nearest",
    #            extent=[0, SIZE, 0, SIZE], norm=matplotlib.colors.LogNorm())
    # plt.show()

    ''' Phase offset change animation '''
    # STEPS = 100
    # RANGE = 2 * pi
    # angles, intensity = calc_intensity()

    # plt.ion()
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection="polar")
    # line1, = ax.plot(angles, intensity)

    # for j in range(STEPS):
    #     update_offset(j * RANGE / STEPS)

    #     _, intensity = calc_intensity()

    #     line1.set_ydata(intensity)
    #     fig.canvas.draw()

    ''' Angle vs Phase offset '''

    # STEPS = 200
    # RANGE = 2 * pi
    # maximas = []
    # offsets = []
    # for i in range(STEPS):
    #     update_offset(i * RANGE / STEPS)
    #     angles, intensity = calc_intensity()
    #     angle_max = angles[max(enumerate(intensity), key=lambda x: x[1])[0]]
    #     maximas.append(angle_max)
    #     offsets.append(i * RANGE / STEPS)
    # plt.scatter(maximas, offsets)
    # plt.show()

    ''' Focusing vs source count '''
    # SLICE = pi/18
    # MAX_COUNT = 16

    # proportions = []
    # for i in range(1, MAX_COUNT):
    #     update_count(i)
    #     angles, intensity = calc_intensity()
    #     proportions.append(power_in_slice(pi/2, SLICE, intensity, angles))

    # plt.plot(proportions)
    # plt.show()

    ''' Focusing vs source count and angle '''
    # SLICE = pi/18
    # STEPS = 50
    # MAX_COUNT = 16

    # data = np.zeros(shape=(MAX_COUNT, STEPS))
    # for i in range(1, MAX_COUNT):
    #     update_count(i)
    #     for j in range(STEPS):
    #         update_offset(j * 2 * pi / STEPS)
    #         angles, intensity = calc_intensity()

    #         center = angles[max(enumerate(intensity), key=lambda x: x[1])[0]]

    #         data[i][j] = power_in_slice(center, SLICE, intensity, angles)

    # plt.imshow(data, cmap="viridis", interpolation="none",
    #            extent=[0, 2*pi, MAX_COUNT, 0])
    # plt.show()

    ''' Focusing vs spacing '''

    SLICE = pi/18
    STEPS = 200

    proportions = []
    spacings = []
    for i in range(STEPS):
        SPACING = i * 4 / STEPS
        spacings.append(i * 4 / STEPS)
        update_count(16)
        angles, intensity = calc_intensity()
        proportions.append(power_in_slice(pi/2, SLICE, intensity, angles))

    plt.plot(spacings, proportions)
    plt.show()
