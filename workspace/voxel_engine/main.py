#!/usr/bin/env python3
"""
Voxel Engine - Main entry point
Step 2: Window, Camera, and Basic Block Rendering
"""

import pygame
from pygame.locals import *
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from voxel_engine.camera import Camera
from voxel_engine.chunk import Chunk

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
    
    # Initialize chunks
    chunks = {}
    for cx in range(-2, 3):
        for cz in range(-2, 3):
            chunks[(cx, cz)] = Chunk(cx, cz)
    
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
                elif event.key == K_f:
                    # Toggle fullscreen
                    pygame.display.toggle_fullscreen()
            elif event.type == MOUSEMOTION:
                camera.handle_input(event)
        
        # Update camera
        camera.update(60)
        
        # Render
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Set camera position
        glLoadIdentity()
        camera.apply()
        
        # Draw visible chunks
        draw_chunks(chunks, camera.position)
        
        # Draw debug info
        draw_debug_info(camera.position, clock.get_fps())
        
        pygame.display.flip()
    
    pygame.quit()

def draw_chunks(chunks, camera_pos):
    """Draw all visible chunks"""
    # Simple visibility culling: draw all chunks within range
    render_distance = 3
    
    for (cx, cz), chunk in chunks.items():
        # Calculate chunk center position
        chunk_x = cx * Chunk.CHUNK_SIZE + Chunk.CHUNK_SIZE / 2
        chunk_z = cz * Chunk.CHUNK_SIZE + Chunk.CHUNK_SIZE / 2
        
        # Distance check
        dist = ((chunk_x - camera_pos.x) ** 2 + (chunk_z - camera_pos.z) ** 2) ** 0.5
        if dist > render_distance * Chunk.CHUNK_SIZE:
            continue
        
        # Draw chunk blocks
        draw_chunk(chunk, cx * Chunk.CHUNK_SIZE, cz * Chunk.CHUNK_SIZE)

def draw_chunk(chunk, world_x: int, world_z: int):
    """Draw all blocks in a chunk"""
    for x in range(chunk.CHUNK_SIZE):
        for y in range(chunk.CHUNK_HEIGHT):
            for z in range(chunk.CHUNK_SIZE):
                block = chunk.get_block(x, y, z)
                if not block.is_air():
                    draw_block(block, world_x + x, world_y := y, world_z + z)

def draw_block(block, x: int, y: int, z: int):
    """Draw a single block at world coordinates"""
    glColor4f(*block.get_color())
    
    # Define cube vertices (1x1x1 cube centered at x,y,z)
    vertices = [
        # Front face
        (x-0.5, y-0.5, z+0.5), (x+0.5, y-0.5, z+0.5), 
        (x+0.5, y+0.5, z+0.5), (x-0.5, y+0.5, z+0.5),
        # Back face
        (x-0.5, y-0.5, z-0.5), (x-0.5, y+0.5, z-0.5), 
        (x+0.5, y+0.5, z-0.5), (x+0.5, y-0.5, z-0.5),
        # Top face
        (x-0.5, y+0.5, z-0.5), (x+0.5, y+0.5, z-0.5), 
        (x+0.5, y+0.5, z+0.5), (x-0.5, y+0.5, z+0.5),
        # Bottom face
        (x-0.5, y-0.5, z-0.5), (x-0.5, y-0.5, z+0.5), 
        (x+0.5, y-0.5, z+0.5), (x+0.5, y-0.5, z-0.5),
        # Right face
        (x+0.5, y-0.5, z-0.5), (x+0.5, y+0.5, z-0.5), 
        (x+0.5, y+0.5, z+0.5), (x+0.5, y-0.5, z+0.5),
        # Left face
        (x-0.5, y-0.5, z-0.5), (x-0.5, y-0.5, z+0.5), 
        (x-0.5, y+0.5, z+0.5), (x-0.5, y+0.5, z-0.5),
    ]
    
    faces = [
        (0, 1, 2, 3),   # Front
        (4, 5, 6, 7),   # Back
        (8, 9, 10, 11), # Top
        (12, 13, 14, 15), # Bottom
        (16, 17, 18, 19), # Right
        (20, 21, 22, 23), # Left
    ]
    
    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glVertex3f(*vertices[vertex])
    glEnd()

def draw_debug_info(pos, fps):
    """Draw debug information"""
    # Could add text rendering here in later steps
    pass

if __name__ == "__main__":
    main()
