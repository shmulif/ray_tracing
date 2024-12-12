"""
A basic (but far from simple) ray tracer.

Author: Christian Duncan
Course: CSC345/645: Computer Graphics
Term: Fall 2024

This code provides the main interface to a ray tracing project. It allows navigation of a simple
scene and then the ability to render that scene using ray tracing. The implementation is SLOW.
But making it efficient is an entirely more complex task.
"""

import sys
import math
import pygame
import copy
from OpenGL.GLU import *
from OpenGL.GL import *
from Navigator import Navigator
from Camera import Camera
from Point3 import Point3
from Vector3 import Vector3
from Window import Window
from Scene import Scene
from SphereObj import SphereObj
from BoxObj import BoxObj
from CylinderObj import CylinderObj
from Material import Material
from Light import Light
from Color import Color

# Constants
FPS = 60
FRAME_WIDTH = 500
FRAME_HEIGHT = 500
FRAME_TITLE = "Go Ray Tracer!"
# DELAY = int(1000 / FPS)

# Initialize global variables
init_eye = Point3(0, 0, 10)
init_look = Point3(0, 0, 0)
init_up = Vector3(0, 1, 0)
init_view_angle = 45.0
init_near = 0.1
init_far = 50.0

nav = Navigator(Camera(init_eye, init_look, init_up))
win = Window(FRAME_WIDTH, FRAME_HEIGHT, FRAME_TITLE)
scn = Scene()
light_angle = 0
light_speed = 1
light_distance = 5
lightB_angle = 0
lightB_speed = 1.5  # Different speed for a different motion
lightB_distance = 5

lightC_angle = 0
lightC_speed = 2  # Speed of light C motion
lightC_distance = 7

lightD_angle = 180
lightD_speed = 1  # Speed of light D motion
lightD_distance = 6

animate = True  # Animation

# Enums for rendering modes
RENDER_SOLID = 0
RENDER_RAY_SINGLE = 1
RENDER_RAY_RECORD = 2
render_mode = RENDER_SOLID
raytrace_count = 0  # How many ray traced images have been generated so far

block_size = 4

# Functions
# def set_light_positions(lightA):
#     global light_angle, light_distance
#     pos_x = light_distance * math.cos(math.radians(light_angle))
#     pos_y = light_distance * math.sin(math.radians(light_angle))
#     pos_z = 0

#     lightA.set_position(pos_x, pos_y, pos_z)
#     lightA.obj.reset()
#     lightA.obj.translate(pos_x, pos_y, pos_z)
#     lightA.obj.scale(0.2, 0.2, 0.2)

def set_light_positions(light, angle, distance):
    pos_x = distance * math.cos(math.radians(angle))
    pos_y = distance * math.sin(math.radians(angle))
    pos_z = 0

    light.set_position(pos_x, pos_y, pos_z)
    light.obj.reset()
    light.obj.translate(pos_x, pos_y, pos_z)
    light.obj.scale(0.2, 0.2, 0.2)

def init_scene():
    global scn, nav, lightA, lightB, lightC, lightD

    # Setup camera
    cam = nav.get_camera()
    cam.look_at(init_eye, init_look, init_up)
    cam.set_lens_shape(init_view_angle, FRAME_WIDTH / FRAME_HEIGHT, init_near, init_far)

    # Create objects and add them to the scene
     # Setup camera
    cam = nav.get_camera()
    cam.look_at(Point3(0, 5, 30), Point3(0, 5, 0), Vector3(0, 1, 0))
    cam.set_lens_shape(init_view_angle, FRAME_WIDTH / FRAME_HEIGHT, init_near, init_far)


    # Back Wall
    mat = Material()
    mat.set_diffuse([1.0, 0.0, 0.0])  # Red
    back_wall = BoxObj()
    back_wall.name = "Back Wall"
    back_wall.set_material(mat)
    back_wall.scale(20, 14, 0.1)
    back_wall.translate(0, 1.5, -200)
    scn.add_object(back_wall)

    #front wall
    mat = Material()
    mat.set_diffuse([1.0, 1.0, 0.8])  # Yellow
    frontwall = BoxObj()
    frontwall.name = "frontwall"
    frontwall.set_material(mat)
    frontwall.scale(20, 14, 0.1)
    frontwall.translate(0, 1, 200)
    scn.add_object(frontwall)

    # Left Wall
    mat = Material()
    mat.set_diffuse([0.3, 0.7, 0.3])  # Green
    left_wall = BoxObj()
    left_wall.name = "Left Wall"
    left_wall.set_material(mat)
    left_wall.scale(0.1, 14, 20)
    left_wall.translate(200, 1.0, 0)
    #left_wall.rotate(90,Vector3(0,0,0))
    scn.add_object(left_wall)

    # Right Wall
    mat = Material()
    mat.set_diffuse([0.3, 0.3, 0.7])  # Blue
    right_wall = BoxObj()
    right_wall.name = "Right Wall"
    right_wall.set_material(mat)
    right_wall.scale(0.1, 14, 20)
    right_wall.translate(-200, 1.0, 0)
    scn.add_object(right_wall)

    # Ceiling
    mat = Material()
    mat.set_diffuse([1.0, 1.0, 0.8])  # Yellow
    ceiling = BoxObj()
    ceiling.name = "Ceiling"
    ceiling.set_material(mat)
    ceiling.scale(20, 0.1, 20)
    ceiling.translate(0, 200, 0)
    scn.add_object(ceiling)

    # Create and add a sphere
    # mat = Material()
    # mat.set_copper()
    # mat.set_reflectivity(0.1)
    # ball = SphereObj()
    # ball.set_material(mat)
    # ball.translate(0,1,0)
    # ball.scale(1, 2, 1)
    # ball.name = "Ball 1"
    # scn.add_object(ball)

    # Create and add a cylinder
    # mat = Material()
    # mat.set_copper()
    # mat.set_reflectivity(0.1)
    # cyl = CylinderObj()
    # cyl.set_material(mat)
    # cyl.translate(0,1,0)
    # cyl.rotate(90,Vector3(1,0,0))
    # cyl.scale(1, 2, 1)
    # cyl.name = "Cylinder 1"
    # scn.add_object(cyl)

    # mat = Material()
    # mat.set_silver()
    # mat.set_reflectivity(0.8)
    # floor = BoxObj()
    # floor.name = "Floor"
    # floor.set_material(mat)
    # floor.translate(0, -2, 0)
    # floor.scale(10, 0.1, 10)
    # scn.add_object(floor)

    # Create and add a cylinder
    # mat = Material()
    # mat.set_copper()
    # mat.set_reflectivity(0.1)
    # cyl = CylinderObj()
    # cyl.set_material(mat)
    # cyl.translate(0, 1, 0)
    # cyl.rotate(90, Vector3(1, 0, 0))
    # cyl.scale(1, 2, 1)
    # cyl.name = "Cylinder 1"
    # scn.add_object(cyl)

    # Create and add a cube
    # mat = Material()
    # mat.set_gold()
    # mat.set_reflectivity(0.5)
    # cube = BoxObj()
    # cube.name = "Minecraft"
    # cube.set_material(mat)
    # cube.translate(1, 0, 0)  # Position the cube
    # cube.scale(1, 1, 1)      # Standard unit cube
    # scn.add_object(cube)

    # Light setup
    lightA = Light()
    scn.add_light(lightA)
    mat = Material()
    mat.set_emissive_only(lightA.get_diffuse())
    mat.set_translucent(True)

    # Create a visible component of the light
    # It will be associated both with the light and with the Scene
    lightA.obj = SphereObj()
    lightA.obj.name = "Light Source"
    lightA.obj.set_material(mat)
    scn.add_object(lightA.obj)

    set_light_positions(lightA, light_angle, light_distance)
   
    # Add second light to the scene
    lightB = Light()
    scn.add_light(lightB)

    # Set material for the second light
    mat = Material()
    mat.set_emissive_only(lightB.get_diffuse())
    mat.set_translucent(True)

    # Create a visible component for the second light
    lightB.obj = SphereObj()
    lightB.obj.name = "Second Light Source"
    lightB.obj.set_material(mat)
    scn.add_object(lightB.obj)

    # Set initial position for the second light
    set_light_positions(lightB, lightB_angle, lightB_distance)

    # Light C setup
    lightC = Light()
    scn.add_light(lightC)
    mat = Material()
    mat.set_emissive_only(lightC.get_diffuse())
    mat.set_translucent(True)

    lightC.obj = SphereObj()
    lightC.obj.name = "Light Source C"
    lightC.obj.set_material(mat)
    scn.add_object(lightC.obj)

    set_light_positions(lightC, lightC_angle, lightC_distance)

    # Light D setup
    lightD = Light()
    scn.add_light(lightD)
    mat = Material()
    mat.set_emissive_only(lightD.get_diffuse())
    mat.set_translucent(True)

    lightD.obj = SphereObj()
    lightD.obj.name = "Light Source D"
    lightD.obj.set_material(mat)
    scn.add_object(lightD.obj)

    set_light_positions(lightD, lightD_angle, lightD_distance)
     

# Return a copy of all the things in scene that could have changed!
def get_copy_state():
    return (copy.deepcopy(nav.camera), light_angle)

# Reset the state back to the given state
def restore_state(state):
    global nav, light_angle, lightA
    nav.camera = copy.deepcopy(state[0])
    light_angle = state[1]
    set_light_positions(lightA)

def display():
    global render_mode, raytrace_count, animate, record
    if render_mode == RENDER_SOLID:
        scn.render_solid(nav.get_camera(), win)
        pygame.display.flip()
    elif render_mode == RENDER_RAY_SINGLE:
        scn.render_solid(nav.get_camera(), win)   # Render solid first so user can see it
        pygame.display.flip()
        scn.render_ray_traced(nav.get_camera(), win, block_size)
        win.save_pixmap('image{0}.png'.format(raytrace_count))
        raytrace_count+=1
        animate = False
        render_mode = RENDER_SOLID # So doesn't try to render it again!
        pygame.event.clear() # Takes so long to render, need to clear events that happened while rendering!
    elif render_mode == RENDER_RAY_RECORD:
        scn.render_solid(nav.get_camera(), win)   # Render solid first so user can see it
        pygame.display.flip()
        if len(record) < 60: # Capped so we don't go crazy ray tracing here!
            # Save a copy of the things that could change from scene to scene
            record.append(get_copy_state())

# Ray trace a sequence of frames - each step recorded to recreate
def raytrace_records(record):
    # Save the current state
    save_state = get_copy_state()

    record_count = 1
    for s in record:
        print("Recording frame {0} of {1}".format(record_count, len(record)))
        # Restore state back to this saved record
        restore_state(s)
        scn.render_solid(nav.get_camera(), win)   # Render solid first so user can see it
        pygame.display.flip()
        scn.render_ray_traced(nav.get_camera(), win, block_size)
        win.save_pixmap('frame{0}.png'.format(record_count))
        record_count+=1

    pygame.event.clear() # Takes so long to render, need to clear events that happened while rendering!

    # Restore it back
    restore_state(save_state)

def handle_events():
    global render_mode, block_size, light_speed, animate, record
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_1:
                block_size = 1
            elif event.key == pygame.K_2:
                block_size = 2
            elif event.key == pygame.K_3:
                block_size = 4
            elif event.key == pygame.K_BACKQUOTE:
                render_mode = RENDER_RAY_SINGLE
            elif event.key == pygame.K_BACKSLASH:
                if render_mode != RENDER_RAY_RECORD:
                    # Start the recording!
                    record = []
                    render_mode = RENDER_RAY_RECORD
                else:
                    # End it and begin ray tracing each image
                    raytrace_records(record)
                    render_mode = RENDER_SOLID
                    animate = False
                    render_mode = RENDER_SOLID # So doesn't try to render it again!
            elif event.key == pygame.K_SPACE:
                animate = not animate
            elif event.key == pygame.K_PERIOD:
                light_speed = 0
            else:
                nav.keyboard(event.key)
    return True

def add_menorah_to_scene():
    # Base of the Menorah (vertical stand)
    mat = Material()
    mat.set_copper()
    mat.set_reflectivity(0.1)
    base = CylinderObj()
    base.set_material(mat)
    base.translate(0, 1, 0)  # Center position
    base.scale(0.5, 2, 0.5)  # Thinner, taller cylinder for the base
    base.name = "Menorah Base"
    scn.add_object(base)

    # Horizontal bar of the Menorah
    mat = Material()
    mat.set_gold()
    mat.set_reflectivity(0.3)
    horizontal_bar = BoxObj()
    horizontal_bar.set_material(mat)
    horizontal_bar.translate(0, 3, 0)  # Positioned above the base
    horizontal_bar.scale(4.5, 0.2, 0.5)  # Long, thin bar
    horizontal_bar.name = "Menorah Horizontal Bar"
    scn.add_object(horizontal_bar)

    # Candles and flames on the Menorah
    for i in range(9):  # Nine candles
        # Candle material
        mat = Material()
        mat.set_copper()
        mat.set_reflectivity(0.1)

        # Candle stick (Cylinder)
        candle = CylinderObj()
        candle.set_material(mat)
        candle_height = 1.5 if i != 4 else 2  # Center candle is taller
        x_offset = -2 + i * 0.5  # Space candles evenly across the bar
        candle.translate(x_offset, 3.5, 0)  # Position on the horizontal bar
        candle.scale(0.2, candle_height, 0.2)  # Thin, tall cylinders
        candle.name = f"Menorah Candle {i+1}"
        scn.add_object(candle)

        # Flame material
        mat = Material()
        mat.set_gold()
        mat.set_reflectivity(0.2)

        # Flame (Sphere)
        flame = SphereObj()
        flame.set_material(mat)
        flame.translate(x_offset, 3.5 + candle_height, 0)  # Above the candle
        flame.scale(0.3, 0.3, 0.3)  # Small flame spheres
        flame.name = f"Menorah Flame {i+1}"
        scn.add_object(flame)

def add_reflect_cube_to_scene():
    # Create a reflective material
    mat = Material()
    mat.set_pewter()
    mat.set_reflectivity(0.9)

    # Create a cube
    reflect_cube = BoxObj()
    reflect_cube.set_material(mat)
    reflect_cube.translate(-5, 3, 0)
    reflect_cube.scale(1, 3, 1)
    reflect_cube.name = "Reflective Minecraft"
    scn.add_object(reflect_cube)

def add_refractive_cube_to_scene():
    # Create a reflective material
    mat = Material()
    mat.set_silver()
    # Replace below with set_refractivity()
    # mat.set_reflectivity(0.9)

    # Create a cube
    reflect_cube = BoxObj()
    reflect_cube.set_material(mat)
    reflect_cube.translate(5, 3, 0)
    reflect_cube.scale(1, 3, 1)
    reflect_cube.name = "Refractive Minecraft"
    scn.add_object(reflect_cube)

def add_filler_cube_to_scene():
    # Create a reflective material
    mat = Material()
    mat.set_pewter()
    mat.set_reflectivity(0.9)

    # Create a cube
    reflect_cube = BoxObj()
    reflect_cube.set_material(mat)
    reflect_cube.translate(-5, 10, 0)
    reflect_cube.scale(1, 3, 1)
    reflect_cube.name = "Reflective Minecraft"
    scn.add_object(reflect_cube)

def add_fillerer_cube_to_scene():
    # Create a reflective material
    mat = Material()
    mat.set_silver()
    mat.set_reflectivity(0.9)

    # Create a cube
    reflect_cube = BoxObj()
    reflect_cube.set_material(mat)
    reflect_cube.translate(5, 10, 0)
    reflect_cube.scale(1, 3, 1)
    reflect_cube.name = "Reflective Minecraft"
    scn.add_object(reflect_cube)
    
def main():
    global light_angle, light_distance, lightA, lightB, lightB_angle, lightC, lightC_angle, lightD, lightD_angle, light_distance, render_mode, animate
    win.initialize()
    init_scene()

    clock = pygame.time.Clock()
    running = True

    add_menorah_to_scene()
    add_reflect_cube_to_scene()
    # add_refractive_cube_to_scene()
    add_filler_cube_to_scene()
    # add_fillerer_cube_to_scene()

    # Set up lighting and depth-test
    glEnable(GL_LIGHTING)
    glEnable(GL_NORMALIZE)    # Inefficient...
    glEnable(GL_DEPTH_TEST)   # For z-buffering!

    while running:
        running = handle_events()

        if animate:
            # Advance the navigator
            nav.advance()
   
             # Animate light A
            light_angle += light_speed
            light_angle %= 360
            set_light_positions(lightA, light_angle, light_distance)

            # Animate light B
            lightB_angle += lightB_speed
            lightB_angle %= 360
            set_light_positions(lightB, lightB_angle, lightB_distance)

            # Animate light C
            lightC_angle += lightC_speed
            lightC_angle %= 360
            set_light_positions(lightC, lightC_angle, lightC_distance)

            # Animate light D
            lightD_angle += lightD_speed
            lightD_angle %= 360
            set_light_positions(lightD, lightD_angle, lightD_distance)

        display()
        
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
