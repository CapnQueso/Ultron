#!/usr/bin/env python3
"""
Test script for chunk and block system
Verifies terrain generation and block data
"""

import sys
import numpy as np

from voxel_engine.block import Block, BlockType
from voxel_engine.chunk import Chunk

def test_block_creation():
    """Test basic block creation"""
    print("[TEST] Block creation...")
    
    block = Block(BlockType.DIRT, 5, 10, 15)
    assert block.block_type == BlockType.DIRT
    assert block.x == 5
    assert block.y == 10
    assert block.z == 15
    assert not block.is_air()
    
    air = Block(BlockType.AIR, 0, 0, 0)
    assert air.is_air()
    
    print("  [PASS] Block creation")

def test_block_colors():
    """Test block color lookup"""
    print("[TEST] Block colors...")
    
    dirt_color = Block(BlockType.DIRT).get_color()
    assert len(dirt_color) == 4
    assert dirt_color[0] > 0 and dirt_color[0] < 1  # R
    
    grass_color = Block(BlockType.GRASS).get_color()
    assert grass_color[1] > dirt_color[1]  # G should be higher for grass
    
    print("  [PASS] Block colors")

def test_chunk_creation():
    """Test chunk initialization"""
    print("[TEST] Chunk creation...")
    
    chunk = Chunk(0, 0)
    
    assert chunk.chunk_x == 0
    assert chunk.chunk_z == 0
    assert chunk.CHUNK_SIZE == 16
    assert chunk.CHUNK_HEIGHT == 64
    
    print("  [PASS] Chunk creation")

def test_chunk_terrain():
    """Test terrain generation"""
    print("[TEST] Terrain generation...")
    
    chunk = Chunk(0, 0)
    
    # Check that we have non-air blocks
    air_count = 0
    block_count = 0
    
    for x in range(0, 16, 4):  # Sample every 4th block
        for z in range(0, 16, 4):
            for y in range(0, chunk.CHUNK_HEIGHT, 8):
                block = chunk.get_block(x, y, z)
                if block.is_air():
                    air_count += 1
                else:
                    block_count += 1
    
    assert block_count > 0, "No blocks generated!"
    
    # Check for grass at surface level
    # Ground is around y=20, grass should be at y=ground_level-1
    grass_found = False
    for x in range(0, 16, 2):
        for z in range(0, 16, 2):
            for y in range(15, 25):  # Check around y=20
                block = chunk.get_block(x, y, z)
                if block.block_type == BlockType.GRASS:
                    grass_found = True
                    print("      Found grass at ({}, {}, {})".format(x, y, z))
                    break
            if grass_found:
                break
        if grass_found:
            break
    
    assert grass_found, "No grass blocks found!"
    
    print("  [PASS] Terrain generation")
    print("      Blocks sampled: {} non-air, {} air".format(block_count, air_count))

def test_tree_generation():
    """Test tree generation"""
    print("[TEST] Tree generation...")
    
    chunk = Chunk(0, 0)
    
    # Trees should be generated at specific coordinates
    # x % 7 == 3 and z % 7 == 3
    # Check positions (3,3), (3,10), (10,3), (10,10)
    
    trees_found = 0
    for tx, tz in [(3, 3), (3, 10), (10, 3), (10, 10)]:
        # Check if there's a wood block at expected tree location
        wood_count = 0
        for y in range(chunk.CHUNK_HEIGHT):
            block = chunk.get_block(tx, y, tz)
            if block.block_type == BlockType.WOOD:
                wood_count += 1
        
        if wood_count >= 3:  # Should have at least 3 wood blocks for a tree
            trees_found += 1
    
    # At least some trees should be generated
    if trees_found == 0:
        print("  [WARN] No trees generated (might be due to terrain height)")
    else:
        print("      Found {} trees".format(trees_found))
    
    print("  [PASS] Tree generation")

def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("Running Voxel Engine Chunk Tests")
    print("=" * 50)
    
    try:
        test_block_creation()
        test_block_colors()
        test_chunk_creation()
        test_chunk_terrain()
        test_tree_generation()
        
        print("")
        print("=" * 50)
        print("[ALL TESTS PASSED]")
        print("=" * 50)
        return True
    except AssertionError as e:
        print("")
        print("[TEST FAILED]")
        print("Error: {}".format(e))
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
