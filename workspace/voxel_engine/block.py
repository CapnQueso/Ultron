#!/usr/bin/env python3
"""
Block module for the voxel engine
Defines block types and basic block rendering
"""

from enum import Enum
from dataclasses import dataclass
from typing import Tuple, Optional

class BlockType(Enum):
    """Enum of available block types"""
    AIR = 0
    DIRT = 1
    GRASS = 2
    STONE = 3
    WOOD = 4
    LEAVES = 5
    SAND = 6
    WATER = 7

@dataclass
class Block:
    """Represents a single block in the world"""
    block_type: BlockType
    x: int = 0
    y: int = 0
    z: int = 0
    
    @property
    def id(self) -> int:
        return self.block_type.value
    
    def is_air(self) -> bool:
        return self.block_type == BlockType.AIR
    
    def get_color(self) -> Tuple[float, float, float, float]:
        """Return RGBA color for this block"""
        colors = {
            BlockType.AIR: (0.0, 0.0, 0.0, 0.0),
            BlockType.DIRT: (0.5, 0.3, 0.1, 1.0),
            BlockType.GRASS: (0.2, 0.8, 0.2, 1.0),
            BlockType.STONE: (0.5, 0.5, 0.5, 1.0),
            BlockType.WOOD: (0.4, 0.3, 0.2, 1.0),
            BlockType.LEAVES: (0.1, 0.5, 0.1, 1.0),
            BlockType.SAND: (0.8, 0.8, 0.5, 1.0),
            BlockType.WATER: (0.0, 0.3, 0.8, 0.5),
        }
        return colors.get(self.block_type, (1.0, 1.0, 1.0, 1.0))
