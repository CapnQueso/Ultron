"""
Voxel Engine Main Entry Point
Step 1: 3D Window, Input Mapping, First-person Camera
Author: Ultron-Prime
"""
from ursina import *

# Import from the package using relative import when run as module
try:
    from voxel_engine.player import VoxelPlayer
except ImportError:
    # Fallback for direct execution
    from player import VoxelPlayer

# Initialize the app
app = Ursina()

# Set window properties
window.title = 'Voxel Engine - Ultron Prime'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = True

# Add sky (basic implementation)
Sky()

# Create the player (First-person controller)
player = VoxelPlayer(
    position=(0, 2, 0),
    speed=15,
    jump_velocity=10
)

# Basic ground plane for testing visibility (will be replaced by chunks in Step 2)
ground = Entity(
    model='plane',
    scale=(100, 1, 100),
    color=color.rgb(100, 150, 100),
    texture='grass',
    collider='box'
)

# Add some simple block for testing visibility
block_test = Entity(
    model='cube',
    scale=(1, 1, 1),
    position=(0, 0.5, 5),
    color=color.rgb(200, 100, 50),
    texture='white_cube',
    collider='box'
)

print("STEP 1 INITIALIZED: Engine running. Use WASD to move, Space to jump, Mouse to look.")

# Run the app
app.run()
