from ray import RayTracer
from material import Material
from sphere import Sphere
from color import Color
from light import Light
from lib import V3

#red_rubber = Material(diffuse=Color(255, 0, 0), albedo = [0.9, 0.1], spec = 10 )
red_metal = Material(diffuse=Color(255, 0, 0), albedo = [0.8, 0.2], spec = 70)
ivory = Material(diffuse=Color(255, 255, 255), albedo = [0.7, 0.3], spec = 50)
white_cotton = Material(diffuse=Color(255, 255, 255), albedo = [0.9, 0.1], spec = 0)
dark_brown_cotton = Material(diffuse=Color(181, 101, 29), albedo = [0.9, 0.1], spec = 0)
light_brown_cotton = Material(diffuse=Color(200, 157, 124), albedo = [0.9, 0.1], spec = 0)
black_metal = Material(diffuse=Color(0, 0, 0), albedo = [0.8, 0.2], spec = 70)

r = RayTracer(500, 500)
r.light = Light(position=V3(0, 0, 0), intensity=1.4, color= Color(255, 255, 255))
r.scene = [
    Sphere(V3(-2, 0, -10), 1, red_metal),
    Sphere(V3(-3, 1, -10), 0.5, dark_brown_cotton),
    Sphere(V3(-1, 1, -10), 0.5, dark_brown_cotton),
    Sphere(V3(-3.25, -0.5, -10), 0.5, dark_brown_cotton),
    Sphere(V3(-0.75, -0.5, -10), 0.5, dark_brown_cotton),

    Sphere(V3(-2, -1.5, -10), 0.75, dark_brown_cotton),
    Sphere(V3(-2.625, -2.125, -10), 0.375, dark_brown_cotton),
    Sphere(V3(-1.375, -2.125, -10), 0.375, dark_brown_cotton),
    Sphere(V3(-1.6, -1.2, -8), 0.25, light_brown_cotton),

    Sphere(V3(-1.4, -1.1, -7), 0.05, black_metal),
    Sphere(V3(-1.65, -1.2, -7), 0.05, black_metal),
    Sphere(V3(-1.15, -1.2, -7), 0.05, black_metal),



    Sphere(V3(2, 0, -10), 1, ivory),
    Sphere(V3(3, 1, -10), 0.5, white_cotton),
    Sphere(V3(1, 1, -10), 0.5, white_cotton),
    Sphere(V3(3.25, -0.5, -10), 0.5, white_cotton),
    Sphere(V3(0.75, -0.5, -10), 0.5, white_cotton),
    Sphere(V3(2, -1.5, -10), 0.75, white_cotton),
    Sphere(V3(2.625, -2.125, -10), 0.375, white_cotton),
    Sphere(V3(1.375, -2.125, -10), 0.375, white_cotton),
    Sphere(V3(1.6, -1.2, -8), 0.25, white_cotton),
    Sphere(V3(1.4, -1.1, -7), 0.05, black_metal),
    Sphere(V3(1.65, -1.2, -7), 0.05, black_metal),
    Sphere(V3(1.15, -1.2, -7), 0.05, black_metal),
    #prueba de material
]
r.dense = 1
r.render()