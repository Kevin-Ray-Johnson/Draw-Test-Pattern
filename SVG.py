#!/usr/bin/env python
"""\
SVG.py - Construct/display SVG scenes.

The following code is a lightweight wrapper around SVG files. The metaphor
is to construct a scene, add objects to it, and then write it to a file
to display it.

This program uses ImageMagick to display the SVG files. ImageMagick also 
does a remarkable job of converting SVG files into other formats.
"""

import os
import math
display_prog = 'display' # Command to execute to display images.
      
class Scene:
    def __init__(self,name="svg",height=400,width=400):
        self.name = name
        self.items = []
        self.height = height
        self.width = width
        return

    def add(self,item): self.items.append(item)

    def strarray(self):
        var = ["<?xml version=\"1.0\"?>\n",
               "<svg height=\"%d\" width=\"%d\" >\n" % (self.height,self.width),
               " <g style=\"fill-opacity:1.0; stroke:black;\n",
               "  stroke-width:1;\">\n"]
        for item in self.items: var += item.strarray()            
        var += [" </g>\n</svg>\n"]
        return var

    def write_svg(self,filename=None):
        if filename:
            self.svgname = filename
        else:
            self.svgname = self.name + ".svg"
        file = open(self.svgname,'w')
        file.writelines(self.strarray())
        file.close()
        return

    def display(self,prog=display_prog):
        os.system("%s %s" % (prog,self.svgname))
        return        

class Text:
    def __init__(self,origin,text,size=24):
        self.origin = origin
        self.text = text
        self.size = size
        return

    def strarray(self):
        return ["  <text x=\"%d\" y=\"%d\" font-size=\"%d\">\n" %\
                (self.origin[0],self.origin[1],self.size),
                "   %s\n" % self.text,
                "  </text>\n"]        

class Line:
    def __init__(self,start,end):
        self.start = start #xy tuple
        self.end = end     #xy tuple
        return

    def strarray(self):
        return ["  <line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" />\n" %\
                (self.start[0],self.start[1],self.end[0],self.end[1])]


class Circle:
    def __init__(self,center,radius,color):
        self.center = center #xy tuple
        self.radius = radius #xy tuple
        self.color = color   #rgb tuple in range(0,256)
        return

    def strarray(self):
        return ["  <circle cx=\"%d\" cy=\"%d\" r=\"%d\"\n" %\
                (self.center[0],self.center[1],self.radius),
                "    style=\"fill:%s;\"  />\n" % colorstr(self.color)]

class Rectangle:
    def __init__(self,origin,height,width,color):
        self.origin = origin
        self.height = height
        self.width = width
        self.color = color
        return

    def strarray(self):
        return ["  <rect x=\"%d\" y=\"%d\" height=\"%d\"\n" %\
                (self.origin[0],self.origin[1],self.height),
                "    width=\"%d\" style=\"fill:%s;\" />\n" %\
                (self.width,colorstr(self.color))]

class Triangle:
    def __init__(self,corner1,corner2,corner3,color):
        self.corner1 = corner1
        self.corner2 = corner2
        self.corner3 = corner3
        self.color = color
        return
    
    def strarray(self):
        return ["  <polygon points=\"%d,%d %d,%d %d,%d\" fill=\"%s\" />\n" %\
               (self.corner1[0], self.corner1[1], 
                self.corner2[0], self.corner2[1], 
                self.corner3[0], self.corner3[1],
                colorstr(self.color))]

class RadialPattern:
    def __init__(self, spokes, radius, origin, color=(0,0,0), size=12):
        self.spokes = spokes
        self.r = radius
        self.origin = origin
        self.color = color
        self.size = size
        return

    def strarray(self):
        pattern = "\n  <text x=\"%d\" y=\"%d\" font-size=\"%d\">\n   %s\n  </text>\n" %\
                  (self.origin[0]-self.r,self.origin[1]-self.r+1.25*self.size,self.size,str(self.spokes)+' Spokes')
        w = math.pi / self.spokes # Angular width of a spoke.
        for i in range(self.spokes):
            pt1X = self.origin[0] - self.r*math.cos(2*i*w)
            pt1Y = self.origin[1] + self.r*math.sin(2*i*w)
            pt2X = self.origin[0] - self.r*math.cos((2*i+1)*w)
            pt2Y = self.origin[1] + self.r*math.sin((2*i+1)*w)
            pattern = pattern + "\n  <polygon points=\"%d,%d %d,%d %d,%d\" fill=\"%s\" stroke-width=\"0\" />\n" %\
                         (self.origin[0], self.origin[1], pt1X, pt1Y, pt2X, pt2Y, colorstr(self.color))
        return [pattern]
        
        

class ThreeBar:
    def __init__(self, pitch, origin, color=(0,0,0)):
        self.pitch = pitch
        self.origin = origin
        self.color = color
        self.height = 0.5 * pitch
        self.width = 2.5 * pitch
        return
    
    def strarray(self):
        return[
        "  <rect x=\"%d\" y=\"%d\" height=\"%d\" width=\"%d\" style=\"fill:%s;\" stroke-width=\"0\" />\n" %\
            (self.origin[0],self.origin[1],self.height,self.width,colorstr(self.color)) +
        "  <rect x=\"%d\" y=\"%d\" height=\"%d\" width=\"%d\" style=\"fill:%s;\" stroke-width=\"0\" />\n" %\
            (self.origin[0],self.origin[1]+self.pitch,self.height, self.width,colorstr(self.color)) +
        "  <rect x=\"%d\" y=\"%d\" height=\"%d\" width=\"%d\" style=\"fill:%s;\" stroke-width=\"0\" />\n" %\
            (self.origin[0],self.origin[1]+2.0*self.pitch,self.height, self.width,colorstr(self.color)) + "\n"
        ]

def colorstr(rgb): return "#%x%x%x" % (rgb[0]/16,rgb[1]/16,rgb[2]/16)

def test():
    scene = Scene('test')
    scene.add(Rectangle((100,100),200,200,(0,255,255)))
    scene.add(Line((200,200),(200,300)))
    scene.add(Line((200,200),(300,200)))
    scene.add(Line((200,200),(100,200)))
    scene.add(Line((200,200),(200,100)))
    scene.add(Circle((200,200),30,(0,0,255)))
    scene.add(Circle((200,300),30,(0,255,0)))
    scene.add(Circle((300,200),30,(255,0,0)))
    scene.add(Circle((100,200),30,(255,255,0)))
    scene.add(Circle((200,100),30,(255,0,255)))
    scene.add(Text((50,50),"Testing SVG"))
    scene.add(Triangle((350,350),(350,395),(395,350),(0,0,0)))
    scene.write_svg()
    #scene.display()
    return

def testRadial():
    scene = Scene('testRadial')
    scene.add(RadialPattern(25, 200, (200,200)))
    scene.write_svg()
    scene.display()
    return
    
def testThreeBar():
    scene = Scene('testThreeBar', 1100, 850)
    pitch = 1
    y = 20
    for i in range(1,10):
        scene.add(ThreeBar(pitch, (20, y)))
        y = y + 3.0*pitch
        pitch = pitch*i*1.1

        
        
    scene.write_svg()
    scene.display()
    return

if __name__ == '__main__': 
    #test()
    testRadial()
    testThreeBar()
