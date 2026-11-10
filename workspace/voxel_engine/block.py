"""
Block System for Voxel Engine
Defines block types, textures, and properties.
"""
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
import colorsys

@dataclass
class BlockDefinition:
    """Definition of a block type."""
    id: int
    name: str
    color: Tuple[int, int, int]
    solid: bool = True
    transparent: bool = False
    hard: int = 1
    
    def get_color(self):
        return self.color

class BlockRegistry:
    """Registry for all block types."""
    
    BLOCKS: Dict[int, BlockDefinition] = {}
    
    @classmethod
    def register(cls, block: BlockDefinition):
        cls.BLOCKS[block.id] = block
    
    @classmethod
    def get(cls, block_id: int) -> Optional[BlockDefinition]:
        return cls.BLOCKS.get(block_id)
    
    @classmethod
    def get_all(cls):
        return cls.BLOCKS.values()

# Define block colors (RGB)
AIR_COLOR = (0, 0, 0, 0)  # Transparent
GRASS_COLOR = (34, 139, 34)
DIRT_COLOR = (139, 90, 43)
STONE_COLOR = (128, 128, 128)
WOOD_COLOR = (139, 90, 43)
LEAVES_COLOR = (34, 139, 34)
SAND_COLOR = (245, 245, 220)
WATER_COLOR = (65, 105, 225)

# Register standard block types
AIR_ID = 0
GRASS_ID = 1
DIRT_ID = 2
STONE_ID = 3
WOOD_ID = 4
LEAVES_ID = 5
SAND_ID = 6
WATER_ID = 7

BlockRegistry.register(BlockDefinition(
    id=AIR_ID, name='Air', color=AIR_COLOR, solid=False, transparent=True
))
BlockRegistry.register(BlockDefinition(
    id=GRASS_ID, name='Grass', color=GRASS_COLOR
))
BlockRegistry.register(BlockDefinition(
    id=DIRT_ID, name='Dirt', color=DIRT_COLOR
))
BlockRegistry.register(BlockDefinition(
    id=STONE_ID, name='Stone', color=STONE_COLOR
))
BlockRegistry.register(BlockDefinition(
    id=WOOD_ID, name='Wood', color=WOOD_COLOR
))
BlockRegistry.register(BlockDefinition(
    id=LEAVES_ID, name='Leaves', color=LEAVES_COLOR, transparent=True
))
BlockRegistry.register(BlockDefinition(
    id=SAND_ID, name='Sand', color=SAND_COLOR
))
BlockRegistry.register(BlockDefinition(
    id=WATER_ID, name='Water', color=WATER_COLOR, solid=False, transparent=True
))
