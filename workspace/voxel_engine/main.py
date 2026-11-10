"""
Voxel Engine Main Entry Point
Step 2: Block creation/destruction grid and chunk generation pipeline
Author: Ultron-Prime
"""
from ursina import *
import math
from voxel_engine.player import VoxelPlayer
from voxel_engine.chunk import Chunk, CHUNK_SIZE, CHUNK_HEIGHT
from voxel_engine.block import BlockRegistry, GRASS_ID, DIRT_ID, STONE_ID, AIR_ID

# Initialize the app
app = Ursina()

# Set window properties
window.title = 'Voxel Engine - Ultron Prime'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = True
window.fog_start = 10
window.fog_end = 80

# Add sky
Sky()

# Create the player
player = VoxelPlayer(
    position=(0, 5, 0),
    speed=15,
    jump_velocity=10
)

# Chunk management
chunks = {}
chunk_entities = {}
global_height_map = None

def generate_height_map():
    """Generate a simple height map for terrain."""
    height_map = {}
    # Create a grid of chunks and generate heights
    for cx in range(-5, 6):
        for cz in range(-5, 6):
            # Simple noise using sine waves
            base_height = 20
            noise1 = math.sin(cx * 0.5) * 5 + math.sin(cz * 0.5) * 5
            noise2 = math.cos(cx * 0.3 + cz * 0.3) * 3
            height = base_height + noise1 + noise2
            height_map[(cx, cz)] = int(height)
    return height_map

def create_chunk(chunk_x: int, chunk_z: int):
    """Create a new chunk at the given coordinates."""
    if (chunk_x, chunk_z) in chunks:
        return
    
    # Generate terrain height map if needed
    global global_height_map
    if global_height_map is None:
        global_height_map = generate_height_map()
    
    chunk = Chunk(chunk_x, chunk_z, CHUNK_HEIGHT)
    chunk.generate_terrain(global_height_map)
    
    # Create visual representation
    chunk_entity = Entity(
        model='cube',
        scale=(CHUNK_SIZE, CHUNK_HEIGHT, CHUNK_SIZE),
        position=(chunk_x * CHUNK_SIZE, CHUNK_HEIGHT // 2, chunk_z * CHUNK_SIZE),
        texture='white_cube',
        color=color.rgb(100, 150, 100),
        texture_scale=(CHUNK_SIZE, CHUNK_HEIGHT),
        collider='box'
    )
    
    chunks[(chunk_x, chunk_z)] = chunk
    chunk_entities[(chunk_x, chunk_z)] = chunk_entity

def update_chunks():
    """Update visible chunks based on player position."""
    player_chunk_x = int(player.x // CHUNK_SIZE)
    player_chunk_z = int(player.z // CHUNK_SIZE)
    
    # Load chunks around player
    render_distance = 2
    for dx in range(-render_distance, render_distance + 1):
        for dz in range(-render_distance, render_distance + 1):
            chunk_x = player_chunk_x + dx
            chunk_z = player_chunk_z + dz
            if (chunk_x, chunk_z) not in chunks:
                create_chunk(chunk_x, chunk_z)
    
    # Unload distant chunks
    unloaded = []
    for (cx, cz) in chunks:
        if abs(cx - player_chunk_x) > render_distance + 1 or abs(cz - player_chunk_z) > render_distance + 1:
            unloaded.append((cx, cz))
    
    for (cx, cz) in unloaded:
        if (cx, cz) in chunk_entities:
            chunk_entities[(cx, cz)].destroy()
        del chunks[(cx, cz)]
        del chunk_entities[(cx, cz)]

# Initial chunk loading
update_chunks()

# Block interaction logic
selected_block = GRASS_ID

def update_block_interaction():
    """Handle block selection and placement/destruction."""
    global selected_block
    
    # Raycast to find the target block
    ray = Ray(
        origin=player.position,
        direction=player.forward,
        distance=6
    )
    
    if ray.intersects():
        intersect_point = ray.hit.position
        collider_entity = ray.hit.hit_info.entity if hasattr(ray.hit, 'hit_info') else None
        
        if collider_entity:
            # Convert world position to chunk coordinates
            world_x, world_y, world_z = intersect_point
            chunk_x = int(world_x // CHUNK_SIZE)
            chunk_z = int(world_z // CHUNK_SIZE)
            
            if (chunk_x, chunk_z) in chunks:
                chunk = chunks[(chunk_x, chunk_z)]
                local_x = int(world_x % CHUNK_SIZE)
                local_z = int(world_z % CHUNK_SIZE)
                
                # Handle left click (break block)
                if mouse.left_down:
                    # Get the block before the intersection point
                    if ray.normal:
                        break_x = world_x - ray.normal.x * 0.5
                        break_y = world_y - ray.normal.y * 0.5
                        break_z = world_z - ray.normal.z * 0.5
                        
                        break_chunk_x = int(break_x // CHUNK_SIZE)
                        break_chunk_z = int(break_z // CHUNK_SIZE)
                        
                        if (break_chunk_x, break_chunk_z) in chunks:
                            break_chunk = chunks[(break_chunk_x, break_chunk_z)]
                            local_break_x = int(break_x % CHUNK_SIZE)
                            local_break_z = int(break_z % CHUNK_SIZE)
                            
                            if 0 <= local_break_x < CHUNK_SIZE:
                                local_break_x = local_break_x % CHUNK_SIZE
                            if 0 <= local_break_z < CHUNK_SIZE:
                                local_break_z = local_break_z % CHUNK_SIZE
                            
                            # Set block to air (remove it)
                            break_chunk.set_block(local_break_x, int(break_y), local_break_z, AIR_ID)
                            break_chunk.is_dirty = True
                
                # Handle right click (place block)
                if mouse.right_down:
                    # Place block adjacent to the hit face
                    place_x = world_x + ray.normal.x * 0.5
                    place_y = world_y + ray.normal.y * 0.5
                    place_z = world_z + ray.normal.z * 0.5
                    
                    place_chunk_x = int(place_x // CHUNK_SIZE)
                    place_chunk_z = int(place_z // CHUNK_SIZE)
                    
                    if (place_chunk_x, place_chunk_z) in chunks:
                        place_chunk = chunks[(place_chunk_x, place_chunk_z)]
                        local_place_x = int(place_x % CHUNK_SIZE)
                        local_place_z = int(place_z % CHUNK_SIZE)
                        
                        if 0 <= local_place_x < CHUNK_SIZE:
                            local_place_x = local_place_x % CHUNK_SIZE
                        if 0 <= local_place_z < CHUNK_SIZE:
                            local_place_z = local_place_z % CHUNK_SIZE
                        
                        # Set block to selected type
                        place_chunk.set_block(local_place_x, int(place_y), local_place_z, selected_block)
                        place_chunk.is_dirty = True
    
    # Update block selection with number keys
    if held_keys['1']: selected_block = GRASS_ID
    if held_keys['2']: selected_block = DIRT_ID
    if held_keys['3']: selected_block = STONE_ID

# UI for block selection
block_ui = Text(
    text='Selected Block: Grass (1)',
    position=(-0.9, 0.45),
    scale=2,
    origin=(0, 0)
)

def update_ui():
    """Update the UI text based on selected block."""
    block_names = {
        GRASS_ID: 'Grass',
        DIRT_ID: 'Dirt',
        STONE_ID: 'Stone'
    }
    block_ui.text = f'Selected Block: {block_names.get(selected_block, "Unknown")} ({selected_block})'

# Spawn a test block for visibility
test_block = Entity(
    model='cube',
    scale=(1, 1, 1),
    position=(0, 1, -5),
    color=color.rgb(200, 100, 50),
    collider='box'
)

# Add update functions to Ursina
def update():
    """Main update loop."""
    update_chunks()
    update_block_interaction()
    update_ui()

print("STEP 2 INITIALIZED: Engine running with chunk generation and block interaction. WASD to move, Space to jump, Mouse to look, Left-click to break, Right-click to place, 1-3 to select block.")

# Run the app
app.run()
