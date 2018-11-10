#!/usr/bin/env python3

"""planets.py: This is a program coded for depicting the path of solar system.

__author__ = "Hejiawei"
__pkuid__  = "1800011753"
__email__  = "Leo.h@pku.edu.cn"
"""

import turtle as t
import math
import random


# classifying a planet class
class Planet(t.Turtle):

    def __init__(self, name, color, omega, size):
        self.name = name
        self.name = t.Turtle()
        self.color = color
        self.length = 1.3
        self.omega = omega
        if self.omega !=0:
            self.orbit = self.length/2/math.tan(0.5*0.1*self.omega/2/math.pi)
        else:
            self.orbit = 0
        self.count = 0
        self.name.speed(0)
        self.size = size
        self.name.shapesize(stretch_wid=self.size, stretch_len=self.size)
        self.name.color(self.color)
        self.name.shape(name='circle')
        self.name.up()

    # define initialize position
    def initialize(self):
        self.name.goto(0,-self.orbit)
        angle = random.randint(1,360)
        self.name.circle(self.orbit, angle)
        self.name.down()

    # define orbiting code
    def go_turn(self, countangle):
        countnumber = countangle // (self.omega * 10)
        if self.count == 0 or self.count != countnumber:
            self.name.left(self.omega)
            self.name.forward(self.length)
            self.count = countnumber
        if countangle > 3600 / min(omegas):
            self.name.up()

    # define staying code
    def stay(self, x, y):
        self.name.goto(0,0)
        self.name.down()


def main():
    # creating a screen instance
    wdn = t.Screen()
    wdn.bgcolor('black')
    # creating list containing properties of planets
    global omegas, planets, colors, sizes
    planets = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn']
    colors = ['grey', 'purple', 'blue', 'red', 'white', 'yellow']
    omegas = [1.2, 0.85, 0.6, 0.42, 0.32, 0.22]
    sizes = [0.8, 1, 1.2, 0.8, 2.1, 3]
    names = locals()
    # creating instances of planet turtles:
    for num in range(0, 6):
        names['%s' % planets[num]] = Planet(planets[num], colors[num], omegas[num], sizes[num])
    # initialize the position of all planet:
    for num in range(0, 6):
        names['%s' % planets[num]].initialize()

    sun = Planet('sun', 'yellow', 0, 1)

    # main loop of planet orbiting:
    i = 1
    sun.stay(0, 0)
    while True:
        for num in range(0, 6):
            names['%s' % planets[num]].go_turn(float(i))
        i += 1


if __name__ == '__main__':
    main()




