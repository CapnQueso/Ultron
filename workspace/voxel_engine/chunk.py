"""
Chunk System for Voxel Engine
Handles chunk generation, storage, and rendering.
"""
import random
from voxel_engine.block import BlockRegistry, AIR_ID, GRASS_ID, DIRT_ID, STONE_ID

CHUNK_SIZE = 16
CHUNK_HEIGHT = 64

class Chunk:
    """
    Represents a 3D chunk of voxels.
    Each chunk is a 16x64x16 grid of blocks.
    """
    
    def __init__(self, chunk_x: int, chunk_z: int, world_height: int = CHUNK_HEIGHT):
        self.chunk_x = chunk_x
        self.chunk_z = chunk_z
        self.width = CHUNK_SIZE
        self.height = world_height
        self.depth = CHUNK_SIZE
        
        # Block data: blocks[x][y][z]
        self.blocks = [[[AIR_ID for _ in range(self.depth)] for _ in range(self.height)] for _ in range(self.width)]
        
        # Mesh cache
        self.mesh = None
        self.is_dirty = True
    
    def get_block(self, x: int, y: int, z: int) -> int:
        """Get block ID at position (local chunk coordinates)."""
        if 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.depth:
            return self.blocks[x][y][z]
        return AIR_ID
    
    def set_block(self, x: int, y: int, z: int, block_id: int):
        """Set block ID at position."""
        if 0 <= x < self.width and 0 <= y < self.height and 0 <= z < self.depth:
            self.blocks[x][y][z] = block_id
            self.is_dirty = True
    
    def get_global_position(self, local_x: int, local_y: int, local_z: int) -> tuple:
        """Convert local chunk coordinates to world coordinates."""
        world_x = self.chunk_x * self.width + local_x
        world_y = local_y
        world_z = self.chunk_z * self.depth + local_z
        return (world_x, world_y, world_z)
    
    def get_local_position(self, world_x: int, world_y: int, world_z: int) -> tuple:
        """Convert world coordinates to local chunk coordinates."""
        local_x = world_x % self.width
        local_z = world_z % self.depth
        # Handle negative coordinates
        if local_x < 0:
            local_x += self.width
        if local_z < 0:
            local_z += self.depth
        return (local_x, world_y, local_z)
    
    def generate_terrain(self, height_map: dict):
        """
        Generate terrain for this chunk based on height map.
        height_map is a dictionary of (chunk_x, chunk_z) -> surface_height
        """
        # Clear chunk to air
        for x in range(self.width):
            for y in range(self.height):
                for z in range(self.depth):
                    self.blocks[x][y][z] = AIR_ID
        
        surface_height = height_map.get((self.chunk_x, self.chunk_z), 20)
        
        # Generate terrain
        for x in range(self.width):
            for z in range(self.depth):
                for y in range(self.height):
                    if y > surface_height:
                        if y == surface_height + 1:
                            self.blocks[x][y][z] = GRASS_ID
                        elif y > surface_height + 4:
                            self.blocks[x][y][z] = STONE_ID
                        else:
                            self.blocks[x][y][z] = DIRT_ID

    def create_mesh(self):
        """
        Generate a single mesh for all visible blocks in the chunk.
        Only creates mesh if chunk is dirty.
        """
        if not self.is_dirty:
            return
        
        mesh_data = Mesh()
        
        # Simple mesh generation - in production this would use vertex buffers
        # For now, we'll create individual entity models
        self.is_dirty = False
        self.mesh = mesh_data
    
    def rebuild(self):
        """Mark chunk as dirty to trigger mesh rebuild."""
        self.is_dirty = True
