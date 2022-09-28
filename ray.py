from code import interact
from lib import *
import random
from material import Material
from sphere import Sphere
from math import *
from light import Light

class RayTracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.clear_color = color(0, 0, 0)
        self.current_color = color(255,255, 255)
        self.background_color = color(0, 0, 0)
        self.dense = 1
        self.scene = []
        self.light = None
        self.clear()

    def clear(self):
        self.framebuffer = [
            [self.clear_color for x in range(self.width)] 
            for y in range(self.height)
            ]

    def point(self, x, y, c = None):
        if y > 0 and y < self.height and x > 0 and x < self.width:
            if c is None:
                c = self.current_color
            self.framebuffer[y][x] = c
    
    def write(self, filename):
        writebmp(filename, self.width, self.height, self.framebuffer)

    def color(self, r, g, b):
        self.current_color = color(r, g, b)    

    def cast_ray(self, origin, direction):
        material, intersect = self.scene_intersect(origin, direction)

        if material is None:
            return self.background_color
        
        l_dir = norm(sub(self.light.position, intersect.point))
        intensity = dot( l_dir, intersect.normal)
        print(material.diffuse[2], intensity)
        if intensity < 0:
            return self.background_color
        else:
            diffuse = color(
                int(material.diffuse[2] * intensity), 
                int(material.diffuse[1] * intensity), 
                int(material.diffuse[0] * intensity) 
            )
            return diffuse

        #return material.diffuse
        #
        #for s in self.scene:
        #    i = s.ray_intersect(origin, direction)
        #    if i:
        #        return s.color
        #return self.background_color


    def render(self):
        fov = int(pi / 2)
        aspect_ratio = self.width / self.height
        #angle = tan(fov / 2)
        angle = tan(fov / 2)
        for y in range(self.height):
            for x in range(self.width):
                rand = random.uniform(0, 1)
                if rand < self.dense:
                    i = ((2 * (x + 0.5) / self.width) - 1) * angle * aspect_ratio
                    j = (1 - 2 * (y + 0.5) / self.height) * angle 
                    
                    direction = V3(i, j, -1).norm()
                    origin = V3(0, 0, 0)
                    
                    c = self.cast_ray(origin, direction)
                    #c = color(255,0,0)
                    self.point(x, y, c)
                
        self.write('ray.bmp')
    
    
    def scene_intersect(self, origin, direction):
        zbuffer = 999999
        material = None
        intersect = None
    

        for o in self.scene:
            hit = o.ray_intersect(origin, direction)
            if hit:
                if hit.distance < zbuffer:
                    zbuffer = hit.distance
                    material = o.material
                    intersect = hit
        return material, intersect
        #zbuffer = float('inf')
        #material = None
        #intersect = None
        #
        #for obj in self.scene:
        #    hit = obj.ray_intersect(origin, direction)
        #    if hit is not None:
        #        if hit.distance < zbuffer:
        #            zbuffer = hit.distance
        #            material = obj.material
        #            intersect = hit
        #return material, intersect
    #def raytrace(self, x, y):
    #    return (0, 0, 0)

#r = RayTracer(500, 500)
#r.point(10, 10)
#r.dense = 0.1
#r.render()
#
red = Material(diffuse=color(255, 0, 0))
white = Material(diffuse=color(255, 255, 255))

r = RayTracer(500, 500)
r.light = Light(position=V3(-3, 0, 0), intensity=1.5)
r.dense = 1
r.scene = [
    Sphere(V3(-3, 0, -16), 2, white),
    Sphere(V3(-3, 0, -10), 2, red)
]
r.render()