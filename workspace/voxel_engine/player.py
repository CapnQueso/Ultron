from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class VoxelPlayer(FirstPersonController):
    """
    Custom player controller extending the FirstPersonController prefab.
    Handles input mapping and first-person camera control.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speed = 15
        self.jumping = False

    def update(self):
        # Use the built-in jump functionality via keypress
        # The prefab handles the jumping logic internally
        pass  # Let parent class handle movement and jumping
