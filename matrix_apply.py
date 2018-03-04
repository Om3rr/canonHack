#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import Xlib
import i3
import numpy as np

import colorsys
import math
import random
import sys
import time


from matplotlib import pyplot as plt

def display_rect(color, idx):
    plt.figure(str(idx))
    plt.fill([0, 0, 1, 1], [0, 1, 1, 0], color=color)

def main():
    # The color count should correspond to the output count
    color_count = 5

    # Spread color_count hues evenly in HSV space
    hues = np.linspace(0, 1, num=color_count + 1)[:-1]

    rgbs = []
    # Convert each hue to RGB
    for hue in hues:
        rgbs.append(colorsys.hsv_to_rgb(hue, 1, 1))

    rgbs = list(zip(np.arange(len(rgbs)), rgbs))

    print("indexes: %s" % [idx for idx, rgb in rgbs])

    for idx, color in rgbs:
        display_rect(color, idx)
        plt.show(False)
        i3.focus(title=str(idx))
        i3.move('workspace 10')

    input()

def apply_output_order(order=list(range(5))):

    # The length changes in the loop due to pop() so we need to save it
    iters = len(order)
    while len(order) > 0:
        idx = order.pop()
        for i in range(iters):
            i3.workspace('10')
            i3.focus(title=str(idx))
            result = i3.move('left')
            # print('move result: %s' % result)
            # print('i = %d' % i)

    # i3.focus(title='Figure 1')
    # i3.move('down')

if __name__ == '__main__':
    main()
