from renderer import render_config
from env_params.refs import objects
import os
import csv

phrase_structure = ["who", "doesWhat", "toWhom", "whereAdverb", "where", "whileDoingWhat", "whileToWhom", "frameInit", "frameEnd"]

actions = {
    'arm_to_locker': lambda arm, locker, null, start, end : [arm, "moved", "itself", "to", locker, "", "", start, end],
    'arm_to_object': lambda arm, obj, null, start, end : [arm, "moved", "itself", "in front of", obj, "", "", start, end],
    'arm_open_door': lambda arm, door, null, start, end : [arm, "opened", door, "", "", "", "", start, end],
    'arm_close_door': lambda arm, door, null, start, end : [arm, "closed", door, "", "", "", "", start, end],
    'arm_into_locker': lambda arm, locker, null, start, end: [arm, "moved", "itself", "into", locker, "", "", start, end],
    'arm_out_locker': lambda arm, locker, null, start, end: [arm, "moved", "itself", "out of", locker, "", "", start, end],
    'arm_grab_object': lambda arm, obj, null, start, end: [arm, "grabbed", obj, "", "", "", "", start, end],
    'arm_out_locker_w_object': lambda arm, locker, obj, start, end: [arm, "moved", "itself", "out of", locker, "holding", obj, start, end],
    'arm_to_locker_w_object': lambda arm, locker, obj, start, end: [arm, "moved", "itself", "in front of", locker, "holding", obj, start, end],
    'arm_position_object_in_locker': lambda arm, obj, locker, start, end: [arm, "positioned", obj, "into", locker, "", "", start, end],
    'arm_to_origin': lambda arm, null, null_2, start, end: [arm, "moved", "itself", "to", "original position", "", "", start, end],
    'arm_exit_scene' : lambda arm, null, null_2, start, end: [arm, "moved", "itself", "out of", "scene", "", "", start, end],
    "arm_in_scene" : lambda arm, null, null_2, start, end: [arm, "moved", "itself", "into", "scene", "", "", start, end],
    "arm_in_scene_w_object" : lambda arm, obj, null, start, end: [arm, "moved", "itself", "into", "scene", "holding", obj, start, end],
    "arm_to_ground" : lambda arm, obj, null, start, end: [arm, "put", obj, "on", "the ground", "", "", start, end],
    "arm_exit_scene_w_object" : lambda arm, obj, null, start, end: [arm, "moved", "itself", "out of", "scene", "holding", obj, start, end],
    "arm_to_unidentified_w_object" : lambda arm, obj, null, start, end : [arm, "moved", "itself", "to", "unidentified position", "holding", obj, start, end],
    "arm_drop_object" : lambda arm, dropped, null, start, end : [arm, "dropped", dropped, "on", "the ground", "", "", start, end],
    "arm_on_top_w_object" : lambda arm, obj, null, start, end : [arm, "moved", "itself", "on", "top of the locker", "holding", obj, start, end],
}

def format_objs(obj, typ=None):
    if typ is not None:
        for key, val in objects.get(typ).items():
            if obj == val:
                return key
    else:
        for diction in objects.values():
            for key, val in diction.items(): 
                if obj == val:
                    return key
    return None

def format_lockers(locker_num):
    return "locker_" + str(locker_num)

def format_doors(locker_num):
    return "door_" + str(locker_num)

def action_builder(action, end, var_1=None, var_2=None, var_3=None, duration=1):
    return actions.get(action)(var_1, var_2, var_3, int(end) - int(render_config["fps"]) * int(duration), end)

def write_csv(moves, folder):
    #create actions file
    with open(os.path.join(folder, 'actions.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(moves)
    print("Written actions file!")