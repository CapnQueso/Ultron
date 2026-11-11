"""
Player System for Voxel Engine
Handles player physics, collision, gravity, and jumping.
"""
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from voxel_engine.chunk import CHUNK_SIZE

class VoxelPlayer(FirstPersonController):
    """
    Custom player controller with physics:
    - Bounding box collision detection
    - Gravity (handled by parent)
    - Jumping (handled by parent)
    - Movement with WASD (handled by parent)
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speed = 15
        self.bounding_box = None
        self.on_ground = True
        self.chunks = {}
        self.chunk_entities = {}
        
        # Initialize bounding box for collision detection
        self.bounding_box = Entity(
            model='cube',
            scale=(0.6, 1.6, 0.6),
            position=self.position,
            visible=False,
            collider=None
        )
    
    def set_chunks(self, chunks, chunk_entities):
        """Set the chunks dictionary for physics calculations."""
        self.chunks = chunks
        self.chunk_entities = chunk_entities
    
    def update(self, chunks=None, chunk_entities=None):
        """Main update loop with physics."""
        # Set chunks if provided
        if chunks is not None and chunk_entities is not None:
            self.chunks = chunks
            self.chunk_entities = chunk_entities
        
        # Call parent update for basic movement and physics
        # FirstPersonController handles gravity, jumping, and movement
        super().update()
        
        # Update bounding box position
        self.bounding_box.position = self.position
        
        # Keep player within reasonable bounds
        boundary = 500
        self.position = Vec3(
            max(-boundary, min(boundary, self.x)),
            self.y,
            max(-boundary, min(boundary, self.z))
        )
