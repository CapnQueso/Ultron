#!/usr/bin/env python3
"""
Camera module for the voxel engine
Handles 3D camera with mouse look and keyboard movement
"""

import pygame
from OpenGL.GL import *
from pygame.locals import *

class Camera:
    def __init__(self):
        self.position = pygame.Vector3(0.0, 2.0, 0.0)
        self.rotation = pygame.Vector2(0.0, 0.0)
        self.speed = 5.0
        self.sensitivity = 0.1
        
        # Movement keys
        self.keys = {
            'forward': False,
            'backward': False,
            'left': False,
            'right': False,
            'up': False,
            'down': False,
        }
    
    def update(self, delta_time):
        """Update camera based on input"""
        # Movement direction
        direction = pygame.Vector3(0.0, 0.0, 0.0)
        
        # Calculate forward and right vectors based on rotation
        rad_x = self.rotation.x
        rad_y = self.rotation.y
        
        # Forward vector (pointing where we look)
        forward_x = -pygame.math.Vector2(rad_y).xnormalized().x if rad_y != 0 else 0.0
        forward_z = -pygame.math.Vector2(rad_y).xnormalized().y if rad_y != 0 else -1.0
        
        # Actually, let's compute this properly
        forward_x = -pygame.sin(rad_y)
        forward_z = -pygame.cos(rad_y)
        
        # Right vector (perpendicular to forward)
        right_x = pygame.cos(rad_y)
        right_z = -pygame.sin(rad_y)
        
        # Apply keyboard input
        if self.keys['forward']:
            direction.x += forward_x
            direction.z += forward_z
        if self.keys['backward']:
            direction.x -= forward_x
            direction.z -= forward_z
        if self.keys['left']:
            direction.x -= right_x
            direction.z -= right_z
        if self.keys['right']:
            direction.x += right_x
            direction.z += right_z
        
        # Normalize and apply speed
        if direction.length() > 0:
            direction = direction.normalized() * self.speed * delta_time * 0.016  # Assume ~60fps
        
        # Apply movement (only horizontal for now)
        self.position.x += direction.x
        self.position.z += direction.z
    
    def apply(self):
        """Apply camera transformation to OpenGL"""
        glTranslatef(-self.position.x, -self.position.y, -self.position.z)
        glRotatef(self.rotation.x * 57.2958, 1, 0, 0)  # Convert to degrees
        glRotatef(self.rotation.y * 57.2958, 0, 1, 0)
    
    def handle_input(self, event):
        """Handle pygame events for camera control"""
        if event.type == KEYDOWN:
            if event.key == K_w:
                self.keys['forward'] = True
            elif event.key == K_s:
                self.keys['backward'] = True
            elif event.key == K_a:
                self.keys['left'] = True
            elif event.key == K_d:
                self.keys['right'] = True
            elif event.key == K_SPACE:
                self.keys['up'] = True
            elif event.key == K_LSHIFT:
                self.keys['down'] = True
        
        elif event.type == KEYUP:
            if event.key == K_w:
                self.keys['forward'] = False
            elif event.key == K_s:
                self.keys['backward'] = False
            elif event.key == K_a:
                self.keys['left'] = False
            elif event.key == K_d:
                self.keys['right'] = False
            elif event.key == K_SPACE:
                self.keys['up'] = False
            elif event.key == K_LSHIFT:
                self.keys['down'] = False
        
        elif event.type == MOUSEMOTION:
            # Update rotation based on mouse movement
            if pygame.mouse.get_focused():
                dx = event.rel[0] * self.sensitivity
                dy = event.rel[1] * self.sensitivity
                
                # Limit vertical rotation
                self.rotation.y += dx
                self.rotation.x = max(-89, min(89, self.rotation.x + dy))
    
    def setup_mouse_capture(self, window_surface):
        """Setup mouse capture for camera control"""
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
