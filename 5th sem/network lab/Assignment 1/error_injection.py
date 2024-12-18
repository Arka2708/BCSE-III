import random

def injectRandomError(frames):
    for i in range(len(frames)):
        pos = random.randint(0, len(frames[i]) - 1)
        frames[i] = frames[i][:pos] + '1' + frames[i][pos + 1:]
    return frames

def injectSpecificError(frames, zeropos, onepos):
    for i in range(len(zeropos)):
        for j in range(len(zeropos[i])):
            pos = zeropos[i][j]
            frames[i] = frames[i][:pos] + '0' + frames[i][pos + 1:]
    for i in range(len(onepos)):
        for j in range(len(onepos[i])):
            pos = onepos[i][j]
            frames[i] = frames[i][:pos] + '1' + frames[i][pos + 1:]
    return frames
