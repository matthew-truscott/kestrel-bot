import numpy as np
import game.br_vec as vec
import math
import random

def diff(vec2_a, vec2_b):
    vec2_d = vec.vec2()
    vec2_d.x = vec2_a.x - vec2_b.x
    vec2_d.y = vec2_a.y - vec2_b.y
    return vec2_d

def random_walk(vec2_p, box_width, box_height, pull):
    speed = 1
    d_walk = 5 # change to increase or decrease movement predictability
    angle_variance = 1 # change to increase or decrease movement predictability
    dx = 0
    dy = 0
    origin = vec.vec2((box_width-1) / 2, (box_height-1) / 2)
    #print(origin)
    pull_dir = diff(origin, vec2_p)
    #print('dir', pull_dir)
    pull_angle = pull_dir.get_direction()
    #print('angle', pull_angle)
    angle = 0
    for i in np.arange(d_walk):
        if angle == 0:
            angle = random.uniform(0, 2 * math.pi)
        else:
            angle += random.uniform(-angle_variance, angle_variance)
        dx += ((speed - pull) * math.cos(angle)) / d_walk
        dy += ((speed - pull) * math.sin(angle)) / d_walk
    if pull_angle < 10:
        dx += math.cos(pull_angle) * pull
        dy += math.sin(pull_angle) * pull
        #print('px', math.cos(pull_angle) * pull, 'py', math.sin(pull_angle) * pull)
    vec2_p.move(dx, dy)

    # discretize
    vec2_p.discretize()
    if vec2_p.x < 0:
        vec2_p.x = 0
    if vec2_p.x > box_width - 1:
        vec2_p.x = box_width - 1
    if vec2_p.y < 0:
        vec2_p.y = 0
    if vec2_p.y > box_height - 1:
        vec2_p.y = box_height - 1


def main():
    p = vec.vec2(0, 0)
    print(p)
    for i in np.arange(100):
        random_walk(p, 10, 10, 0.4)
        print(p)
        #print('_______')

if __name__ == "__main__":
    main()
