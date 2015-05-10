#!/usr/bin/env python
"""
This draws a radial optical test pattern image.
"""

import SVG # A little SVG Library for drawing simple stuff.

# Dimensions for an 8.5" x 11" paper.
sceneHeight = 1100
sceneWidth = 850
margin = 10  # How wide the margin around the image border and between patterns is.
scene = SVG.Scene('radialPattern', sceneHeight, sceneWidth) # Make the scene we will be drawing in.
r = min( (sceneHeight - 3*margin)/4.0, (sceneWidth - 2*margin)/2.0) # The radius of the test pattern.

origin1 = (sceneWidth/2.0, r+margin) # The center of the first pattern
origin2 = (sceneWidth/2.0, 3*r+2*margin) # The center of the second pattern
black = (0,0,0) # The color black

scene.add(SVG.RadialPattern(30, r, origin1))
scene.add(SVG.RadialPattern(45, r, origin2))
    
scene.write_svg()
scene.display()
