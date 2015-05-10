#!/usr/bin/env python
"""
This draws a radial optical test pattern image.
"""

import SVG # A little SVG Library for drawing simple stuff.

# Dimensions for an 8.5" x 11" paper.
sceneHeight = 1100
sceneWidth = 850
margin = 10 # How wide the margin around the image border and between patterns is.
pitch = 150
scene = SVG.Scene('3-bar-pattern-test', sceneHeight, sceneWidth) # Make the scene we will be drawing in.

pitch = 1
y = 20
for i in range(1,10):
    scene.add(SVG.ThreeBar(pitch, (20, y)))
    y = y + 4.0*pitch
    pitch = pitch + 2*i

scene.write_svg()

#scene.display()
