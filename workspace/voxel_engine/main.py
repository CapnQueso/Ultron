#!/usr/bin/env python3
"""
Voxel Engine - Main entry point
Step 1: Window & Camera Setup
"""

import pygame
from pygame.locals import *
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from voxel_engine.camera import Camera

def main():
    """Initialize pygame and create window"""
    pygame.init()
    
    # Set up display
    display_width = 1280
    display_height = 720
    
    pygame.display.set_mode((display_width, display_height), DOUBLEBUF | OPENGL)
    
    # Initialize OpenGL
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.5, 0.7, 1.0, 1.0)  # Sky blue background
    
    # Set up perspective
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display_width / display_height), 0.1, 500.0)
    glMatrixMode(GL_MODELVIEW)
    
    # Create camera
    camera = Camera()
    
    # Game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        clock.tick(60)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        # Update camera
        camera.update(60)
        
        # Render
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Set camera position
        glLoadIdentity()
        camera.apply()
        
        # Draw some debug cubes to verify 3D rendering
        draw_debug_scene()
        
        pygame.display.flip()
    
    pygame.quit()

def draw_debug_scene():
    """Draw a simple debug scene with cubes"""
    glPushMatrix()
    
    # Draw a cube at origin
    draw_cube(-2, -1, 0)
    
    # Draw another cube
    draw_cube(2, -1, 0)
    
    glPopMatrix()

def draw_cube(x, y, z, color=(1.0, 0.5, 0.0)):
    """Draw a simple colored cube"""
    glColor3f(*color)
    
    vertices = [
        # Front face
        (x-1, y-1, z+1), (x+1, y-1, z+1), (x+1, y+1, z+1), (x-1, y+1, z+1),
        # Back face
        (x-1, y-1, z-1), (x-1, y+1, z-1), (x+1, y+1, z-1), (x+1, y-1, z-1),
        # Top face
        (x-1, y+1, z-1), (x+1, y+1, z-1), (x+1, y+1, z+1), (x-1, y+1, z+1),
        # Bottom face
        (x-1, y-1, z-1), (x-1, y-1, z+1), (x+1, y-1, z+1), (x+1, y-1, z-1),
        # Right face
        (x+1, y-1, z-1), (x+1, y+1, z-1), (x+1, y+1, z+1), (x+1, y-1, z+1),
        # Left face
        (x-1, y-1, z-1), (x-1, y-1, z+1), (x-1, y+1, z+1), (x-1, y+1, z-1),
    ]
    
    faces = [
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (8, 9, 10, 11),
        (12, 13, 14, 15),
        (16, 17, 18, 19),
        (20, 21, 22, 23),
    ]
    
    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glVertex3f(*vertices[vertex])
    glEnd()

if __name__ == "__main__":
    main()
