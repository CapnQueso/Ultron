#!/usr/bin/env python3
"""
Chunk module for the voxel engine
Handles chunk generation and rendering
"""

from typing import Tuple
import numpy as np
from voxel_engine.block import Block, BlockType

class Chunk:
    """Represents a chunk of voxels in the world"""
    
    CHUNK_SIZE = 16
    CHUNK_HEIGHT = 64
    
    def __init__(self, chunk_x: int, chunk_z: int):
        self.chunk_x = chunk_x
        self.chunk_z = chunk_z
        
        # Create empty voxel array (chunk_x, chunk_y, height)
        # Each chunk covers a 16x64x16 area
        self.blocks = np.full(
            (self.CHUNK_SIZE, self.CHUNK_HEIGHT, self.CHUNK_SIZE),
            Block(BlockType.AIR),
            dtype=object
        )
        
        # Generate initial terrain
        self.generate_terrain()
    
    def generate_terrain(self):
        """Generate simple terrain with some variation"""
        import math
        
        for x in range(self.CHUNK_SIZE):
            for z in range(self.CHUNK_SIZE):
                # World coordinates
                world_x = self.chunk_x * self.CHUNK_SIZE + x
                world_z = self.chunk_z * self.CHUNK_SIZE + z
                
                # Simple terrain height using sine waves
                base_height = 20
                height_variation = int(
                    5 * math.sin(world_x * 0.1) * math.cos(world_z * 0.1)
                )
                ground_level = base_height + height_variation
                
                # Fill blocks from bottom to ground
                for y in range(ground_level):
                    if y == ground_level - 1:
                        self.blocks[x, y, z] = Block(BlockType.GRASS, x, y, z)
                    elif y > ground_level - 4:
                        self.blocks[x, y, z] = Block(BlockType.DIRT, x, y, z)
                    else:
                        self.blocks[x, y, z] = Block(BlockType.STONE, x, y, z)
                
                # Add some trees occasionally
                if x % 7 == 3 and z % 7 == 3 and ground_level > 15:
                    self.generate_tree(x, ground_level, z)
    
    def generate_tree(self, x: int, y: int, z: int):
        """Generate a simple tree"""
        # Trunk
        for h in range(4):
            if y + h < self.CHUNK_HEIGHT:
                self.blocks[x, y + h, z] = Block(BlockType.WOOD, x, y + h, z)
        
        # Leaves
        for lx in range(-2, 3):
            for ly in range(3, 6):
                for lz in range(-2, 3):
                    if abs(lx) + abs(lz) <= 3:  # Round shape
                        tx, ty, tz = x + lx, y + ly, z + lz
                        if (0 <= tx < self.CHUNK_SIZE and 
                            0 <= ty < self.CHUNK_HEIGHT and 
                            0 <= tz < self.CHUNK_SIZE):
                            if not self.blocks[tx, ty, tz].is_air():
                                self.blocks[tx, ty, tz] = Block(BlockType.LEAVES, tx, ty, tz)
    
    def get_block(self, x: int, y: int, z: int) -> Block:
        """Get block at local chunk coordinates"""
        if (0 <= x < self.CHUNK_SIZE and 
            0 <= y < self.CHUNK_HEIGHT and 
            0 <= z < self.CHUNK_SIZE):
            return self.blocks[x, y, z]
        return Block(BlockType.AIR)
    
    def set_block(self, x: int, y: int, z: int, block: Block):
        """Set block at local chunk coordinates"""
        if (0 <= x < self.CHUNK_SIZE and 
            0 <= y < self.CHUNK_HEIGHT and 
            0 <= z < self.CHUNK_SIZE):
            self.blocks[x, y, z] = block
    
    def get_chunk_position(self) -> Tuple[int, int]:
        """Get chunk's world position in chunk coordinates"""
        return (self.chunk_x, self.chunk_z)
