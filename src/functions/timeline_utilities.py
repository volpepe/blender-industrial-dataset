import bpy
from renderer import render_config

# Timeline manipulation utilities

# Changes current frame
def set_current_frame(frame_num):
    bpy.context.scene.frame_set(frame_num)

# Adds a keyframe at the current frame for a list of objects
def set_keyframe_for_objects(scene_objects, data_path="location"):
    for scene_object in scene_objects:
        scene_object.keyframe_insert(data_path=data_path, index=-1)

# Moves to the next second
def advance_frame(current_frame):
    current_frame += render_config["fps"]
    set_current_frame(current_frame)
    return current_frame