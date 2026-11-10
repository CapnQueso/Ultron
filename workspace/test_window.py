#!/usr/bin/env python3
"""
Test script to verify window and camera setup
Runs in headless mode or with display
"""

import sys
import os

# Check for required dependencies
try:
    import pygame
    import numpy
    from OpenGL.GL import *
    print("[OK] All dependencies available")
except ImportError as e:
    print(f"[FAIL] Missing dependency: {e}")
    print("Please run: pip install pygame numpy PyOpenGL")
    sys.exit(1)

# Test imports
try:
    from voxel_engine.camera import Camera
    print("[OK] Voxel engine modules imported successfully")
except ImportError as e:
    print(f"[FAIL] Import error: {e}")
    sys.exit(1)

# Test camera instantiation
try:
    camera = Camera()
    print("[OK] Camera created: position={}, rotation={}".format(camera.position, camera.rotation))
except Exception as e:
    print(f"[FAIL] Camera initialization failed: {e}")
    sys.exit(1)

print("")
print("[OK] All basic tests passed!")
print("Next step: Run main.py to see the window")
