import bpy
from random import randint, choice, random
from mathutils import Vector
import os
from datetime import datetime
from math import radians
import sys
from functools import partial
import csv
import argparse
import time

render_config = {
    "fps": 12
}

#objects present in the scene

objects = {
    'cubes' : {
        'cube_0' : bpy.data.objects["Cube"],
        'cube_1' : bpy.data.objects["Cube.001"],
        'cube_2' : bpy.data.objects["Cube.002"],
        'cube_3' : bpy.data.objects["Cube.003"],
        'cube_4' : bpy.data.objects["Cube.004"],
        'cube_5' : bpy.data.objects["Cube.005"],
        'cube_6' : bpy.data.objects["Cube.006"],
        'cube_7' : bpy.data.objects["Cube.007"],
        'cube_8' : bpy.data.objects["Cube.008"],
    }, 
    'spheres' : {
        'sphere_0' : bpy.data.objects["Sphere"],
        'sphere_1' : bpy.data.objects["Sphere.001"],
        'sphere_2' : bpy.data.objects["Sphere.002"],
        'sphere_3' : bpy.data.objects["Sphere.003"],
        'sphere_4' : bpy.data.objects["Sphere.004"],
        'sphere_5' : bpy.data.objects["Sphere.005"],
    },
    'cones' : {
        'cone_0' : bpy.data.objects["Cone"],
        'cone_1' : bpy.data.objects["Cone.001"],
        'cone_2' : bpy.data.objects["Cone.002"],
    },
    'cylinders' : {
        'cylinder_0' : bpy.data.objects["Cylinder"],
        'cylinder_1' : bpy.data.objects["Cylinder.001"],
    },
    'lights' : {
        'light_0' : bpy.data.lights["Light"],
    },
    'cameras' : {
        'camera_0' : bpy.data.objects["Camera"],
    },
    'robots' : {
        'arm' : bpy.data.objects["arm"],
        'arm_color' : bpy.data.objects["arm.color"],
        'arm_copy' : bpy.data.objects["arm.copy"],
    }
}

object_locations = {
    'ground_in' : [
        bpy.data.objects["Cube.002"],
        bpy.data.objects["Cube.004"],
        bpy.data.objects["Cube.007"],
        bpy.data.objects["Cone.001"],
        bpy.data.objects["Cylinder.001"],
    ],
    'ground_out' : [
        bpy.data.objects["Cone.002"],
        bpy.data.objects["Sphere.005"],
        bpy.data.objects["Cube.008"],
    ],
    'loc_0': [
        bpy.data.objects["Sphere"],
    ],
    'loc_1': [],
    'loc_2': [
        bpy.data.objects["Sphere.001"],
    ],
    'loc_3': [
        bpy.data.objects["Cube"],
    ],
    'loc_4': [
        bpy.data.objects["Cylinder"],
        bpy.data.objects["Cube.001"],
        bpy.data.objects["Sphere.002"],
    ],
    'loc_5': [
        bpy.data.objects["Sphere.004"],
    ],
    'loc_6': [],
    'loc_7': [],
    'loc_8': [
        bpy.data.objects["Sphere.003"],
    ],
    'loc_9': [
        bpy.data.objects["Cone"],
    ],
    'loc_10': [],
    'loc_11': [
        bpy.data.objects["Cube.006"],
    ],
    'loc_12': [
        bpy.data.objects["Cube.003"],
        bpy.data.objects["Cube.005"],
    ],
    'loc_13': [],
}

#doors of the locker: they can be opened by rotating their z axis at -90°
#and closed by restoring that to 0°
doors = {
    'door_0' : bpy.data.objects["Door_0"],
    'door_1' : bpy.data.objects["Door_1"],
    'door_2' : bpy.data.objects["Door_2"],
    'door_3' : bpy.data.objects["Door_3"],
    'door_4' : bpy.data.objects["Door_4"],
    'door_5' : bpy.data.objects["Door_5"],
    'door_6' : bpy.data.objects["Door_6"],
    'door_7' : bpy.data.objects["Door_7"],
    'door_8' : bpy.data.objects["Door_8"],
    'door_9' : bpy.data.objects["Door_9"],
    'door_10' : bpy.data.objects["Door_10"],
    'door_11' : bpy.data.objects["Door_11"],
    'door_12' : bpy.data.objects["Door_12"],
    'door_13' : bpy.data.objects["Door_13"],
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

#False = closed, True = open
door_open = [False] * len(doors.keys())

brightness_levels = [x for x in range(2000, 60000, 1000)]

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
    "arm_drop_object" : lambda arm, dropped, null, start, end : [arm, "dropped", dropped, "on", "the ground", "", "", start, end]
}

def action_builder(action, end, var_1=None, var_2=None, var_3=None, duration=1):
    return actions.get(action)(var_1, var_2, var_3, int(end) - int(render_config["fps"]) * int(duration), end)

###################################################################

#random choices

#choose a random luminosity and print it to console
def choose_luminosity(min=2000, max=60000):
    chosen_luminosity = choice([x for x in brightness_levels if x >= min and x <= max])
    print("Chosen luminosity: " + str(chosen_luminosity))
    return chosen_luminosity

#choose a random activity from the ones in the activity dictionary
def choose_activity():
    random_activity = choice(list(activities.keys()))
    print("Chosen activity: " + random_activity)
    return random_activity

#selects a random object from a list of choices passed as an argument
#a location can be selected as well
#example: ["cubes", "spheres"] --> select a random cube or sphere
#["cubes"] --> selects a random cube
def select_random_object(choices=["cubes", "spheres", "cylinders", "cones"], locations=None):
    list_obj = []
    for c in choices:
        list_obj.extend(objects[c].values())
    if locations is not None:
        list_obj = [x for x in list_obj for loc in locations if x in object_locations[loc]]
    return choice(list_obj)

def get_random_locker_num_and_door(exceptions=[], nonempty=False):
    while True: 
        i = randint(0, len(doors.keys()) - 1)
        if i not in exceptions:
            if not nonempty:
                print("Chosen door " + str(i))
                break
            elif len(object_locations['loc_' + str(i)]) > 0:
                print("Chosen door " + str(i))
                break
            else:
                pass
    return i, doors["door_" + str(i)]

def random_scaled(max, min):
    return min + random() * (max - min)

def get_random_x_and_y_within_locker(door):
    boundary = door.dimensions[1]
    margin = 0.2
    #scale random values with min + (value * (max - min))
    x = random_scaled(boundary - margin, margin)
    y = random_scaled(boundary - margin, margin)
    return x, y

def random_rotate_camera(camera):
    #20% chance
    if random() <= 0.2:
        print("Camera rotated")
        camera_x_max_boundary = radians(69)
        camera_x_min_boundary = radians(56) 
        camera_y_max_boundary = radians(20)
        camera_y_min_boundary = radians(-11)
        camera_z_max_boundary = radians(120)
        camera_z_min_boundary = radians(100)
        x_rot = random_scaled(camera_x_max_boundary, camera_x_min_boundary)
        y_rot = random_scaled(camera_y_max_boundary, camera_y_min_boundary)
        z_rot = random_scaled(camera_z_max_boundary, camera_z_min_boundary)
        camera.rotation_euler = Vector([x_rot, y_rot, z_rot])

def select_random_coordinates_on_visible_ground():
    x_min = 2.2875
    x_max = 4.5
    y_min = -3.6
    y_max = 5.00
    return random_scaled(x_max, x_min), random_scaled(y_max, y_min)

def random_select_rotate_arm():
    #select main arm and store its position
    arm = objects["robots"]["arm"]
    starting_position = Vector(arm.location)
    
    #select a random arm and swap the two arm locations
    random_arm = select_random_object(choices=["robots"])
    arm.location = random_arm.location
    random_arm.location = starting_position

    #randomly choose a small arm rotation
    random_arm.rotation_euler[0] = radians(random_scaled(110, 70))
    random_arm.rotation_euler[1] = radians(random_scaled(40, 20))
    random_arm.rotation_euler[2] = radians(random_scaled(-35, -40))

    return random_arm

###################################################################

#rendering utilities

#changes current frame
def set_current_frame(frame_num):
    bpy.context.scene.frame_set(frame_num)

#adds a keyframe at the current frame for a list of objects
def set_keyframe_for_objects(scene_objects, data_path="location"):
    for scene_object in scene_objects:
        scene_object.keyframe_insert(data_path=data_path, index=-1)

#last function to call: renders the scene with the set keyframes and settings
def render_and_end():
    bpy.ops.render.render(animation=True)

###################################################################

#environment utilities

#gets all object except the ones defined in the exception list
def get_all_objects(exceptions=[]):
    return [obj for key in objects.keys() for obj in objects[key].values() if key not in exceptions]

#sets a random luminosity to a light
def set_random_luminosity(light, min=200, max=8200):
    light.energy = choose_luminosity()

def enable_collisions(objs):
    for obj in objs:
        obj.rigid_body.enabled = True
        obj.rigid_body.kinematic = False

#returns a string that indicates where the object is
def get_locker_loc_for_object(obj):
    for locker in [x for x in object_locations.keys() if x != "ground_in" and x != "ground_out"]:
        if obj in object_locations[locker]:
            return locker
    return None

#gets the location of the locker's handle
def get_handle_location_for_object(obj):
    locker = get_locker_loc_for_object(obj)
    if locker is not None and locker != 'ground_in' and locker != 'ground_out':
        locker_num = locker.split('_')[1]
        door = doors['door_' + locker_num]
        return get_handle_location_for_door(door, locker_num)
    else:
        return None

def get_handle_location_for_door(door, locker_num):
    #we need to copy the location in a new vector or the following changes would be made on the door location
    door_location = Vector(door.location)
    if not door_open[int(locker_num)]:
        door_location[1] += door.dimensions[1]
    else:
        door_location[0] += door.dimensions[1]
    return door_location

###################################################################

#basic actions

def advance_frame(current_frame):
    current_frame += render_config["fps"]
    set_current_frame(current_frame)
    return current_frame

def close_door(arm, door, locker_num):
    door.rotation_euler[2] = radians(0)
    door_open[int(locker_num)] = False
    arm.location = get_handle_location_for_door(door, locker_num)
    set_keyframe_for_objects([arm])
    set_keyframe_for_objects([door], data_path="rotation_euler")

def return_to_origin(arm, starting_location):
    arm.location = starting_location
    set_keyframe_for_objects([arm])

def open_locker(arm, door, locker_num):
    #radians operations are required for rotations
    door.rotation_euler[2] = radians(-90)
    door_open[int(locker_num)] = True
    arm.location = get_handle_location_for_door(door, locker_num)
    set_keyframe_for_objects([arm])
    set_keyframe_for_objects([door], data_path="rotation_euler")

def move_to_locker_and_open(arm, door, locker, format_arm, format_locker, format_door, current_frame, moves):
    #get to door 1
    current_frame = advance_frame(current_frame)
    arm.location = get_handle_location_for_door(door, locker)
    set_keyframe_for_objects([arm, door])
    set_keyframe_for_objects([door], data_path="rotation_euler")
    moves.append(action_builder("arm_to_locker", current_frame, format_arm, format_locker))
    
    #open the first locker
    current_frame = advance_frame(current_frame)
    open_locker(arm, door, locker)
    moves.append(action_builder("arm_open_door", current_frame, format_arm, format_door))
    return current_frame, moves

def setup_taking_object(moves):
    #select a random object in a locker
    grabbed = select_random_object(locations=[x for x in \
        object_locations.keys() if x not in ["ground_in", "ground_out"]])
    print("Selected " + str(grabbed))

    #enable all collisions
    enable_collisions(get_all_objects(exceptions=["lights", "cameras"]))

    #get reference to the arm
    arm = random_select_rotate_arm()
    starting_location = [x for x in arm.location]

    #let the arm be controlled by the animation
    arm.rigid_body.kinematic = True
    #temporarily disable rigid_body physics for the sphere
    grabbed.rigid_body.kinematic = True

    #set the first keyframe for the arm, the object and the locker door
    current_frame = 0
    set_current_frame(current_frame)
    set_keyframe_for_objects([arm, grabbed])

    grabbed.keyframe_insert(data_path='rigid_body.enabled', frame=current_frame)
    grabbed.keyframe_insert(data_path='rigid_body.kinematic', frame=current_frame)

    locker_num = get_locker_loc_for_object(grabbed).split("_")[1]

    door = doors['door_' + str(locker_num)]

    format_arm = format_objs(arm, 'robots')
    format_grab = format_objs(grabbed)
    format_locker = format_lockers(locker_num)
    format_door = format_doors(locker_num)

    current_frame, moves = move_to_locker_and_open(arm, door, locker_num, format_arm, \
        format_locker, format_door, current_frame, moves)

    #get in front of the object (1 sec)
    current_frame, moves = take_obj_from_locker(current_frame, moves, arm, grabbed, \
        format_arm, format_grab, format_locker)

    return arm, grabbed, locker_num, door, format_arm, format_grab, format_locker, \
        format_door, current_frame, starting_location, moves

def position_item_to_locker_then_close(arm, grabbed, door, locker_num, format_arm, format_grab, \
        format_locker, format_door, current_frame, moves):
    ##take the item to second locker
    #first move in y and z to second locker
    current_frame = advance_frame(current_frame)
    #x and y are random within the locker boundaries
    positioning_x, positioning_y = get_random_x_and_y_within_locker(door)
    correct_x = door.location[0] - positioning_x
    correct_y = door.location[1] + positioning_y
    #correct z to put the object exactly at the height of the shelf of the locker
    correct_z = door.location[2] - door.dimensions[2] / 2 + grabbed.dimensions[2] / 2
    #move in y and z
    arm.location[1] = grabbed.location[1] = correct_y
    grabbed.location[2] = correct_z
    arm.location[2] = correct_z + grabbed.dimensions[2] / 2
    set_keyframe_for_objects([arm, grabbed])
    moves.append(action_builder("arm_to_locker_w_object", current_frame, format_arm, format_locker, \
        format_grab))

    #put it in(1 sec)
    #move in x
    current_frame = advance_frame(current_frame)
    placeholder = arm.location[0]
    arm.location[0] = grabbed.location[0] = correct_x
    set_keyframe_for_objects([arm, grabbed])
    moves.append(action_builder("arm_position_object_in_locker", current_frame, format_arm, \
        format_grab, format_locker))

    #get out (1 sec)
    current_frame = advance_frame(current_frame)
    arm.location[0] = placeholder + grabbed.dimensions[0]
    set_keyframe_for_objects([arm])
    moves.append(action_builder("arm_out_locker", current_frame, format_arm, format_locker))

    #close lockers
    #get to handle
    current_frame = advance_frame(current_frame)
    arm.location = get_handle_location_for_door(door, locker_num)
    set_keyframe_for_objects([arm])
    set_keyframe_for_objects([door], data_path="rotation_euler")

    #close door
    current_frame = advance_frame(current_frame)
    close_door(arm, door, locker_num)
    moves.append(action_builder("arm_close_door", current_frame, format_arm, format_door))

    return current_frame, moves

def put_item_in_visible_position(current_frame, arm, grabbed, format_arm, format_grab, moves):
    #put the object on the ground, in a random visible position
    current_frame = advance_frame(current_frame)
    x, y = select_random_coordinates_on_visible_ground()
    arm.location[0] = grabbed.location[0] = x
    arm.location[1] = grabbed.location[1] = y
    grabbed.location[2] = grabbed.dimensions[2] / 2
    arm.location[2] = grabbed.location[2] + grabbed.dimensions[2] / 2
    set_keyframe_for_objects([arm, grabbed])
    moves.append(action_builder("arm_to_ground", current_frame, format_arm, format_grab))
    return current_frame, moves

def take_obj_from_locker(current_frame, moves, arm, grabbed, format_arm, format_grab, format_locker):
    #move in y and z
    current_frame = advance_frame(current_frame)
    arm.location[1] = grabbed.location[1]
    #apply correction for z axis to get on top of the object
    arm.location[2] = grabbed.location[2] + (grabbed.dimensions[2] / 2)
    set_keyframe_for_objects([arm])
    moves.append(action_builder("arm_to_locker", current_frame, format_arm, format_locker))
    moves.append(action_builder("arm_to_object", current_frame, format_arm, format_grab))

    #get item (1 sec)
    #move in x
    current_frame = advance_frame(current_frame)
    placeholder = arm.location[0]
    arm.location[0] = grabbed.location[0]
    set_keyframe_for_objects([arm, grabbed])
    moves.append(action_builder("arm_into_locker", current_frame, format_arm, format_locker))
    moves.append(action_builder("arm_grab_object", current_frame, format_arm, format_grab, duration=0))

    #get out with item (1 sec)
    current_frame = advance_frame(current_frame)
    arm.location[0] = grabbed.location[0] = placeholder + grabbed.dimensions[0]
    set_keyframe_for_objects([arm, grabbed])
    moves.append(action_builder("arm_out_locker_w_object", current_frame, format_arm, format_locker, format_grab))

    return current_frame, moves

########### ACTIVITIES ################

def move_obj_to_other_locker(obj_type):

    moves = [phrase_structure]

    #select a random obj in a locker
    obj = select_random_object(choices=[obj_type], locations=[x for x in object_locations.keys() \
        if x not in ["ground_in", "ground_out"]])
    print("Selected " + str(obj))

    #enable all collisions
    enable_collisions(get_all_objects(exceptions=["lights", "cameras"]))

    #get reference to the arm
    arm = random_select_rotate_arm()
    starting_location = [x for x in arm.location]

    #let the arm be controlled by the animation
    arm.rigid_body.kinematic = True
    #temporarily disable rigid_body physics for the obj
    obj.rigid_body.kinematic = True

    #set the first keyframe for the arm, the obj and the locker door
    current_frame = 0
    set_current_frame(current_frame)
    set_keyframe_for_objects([arm, obj])

    locker_num = get_locker_loc_for_object(obj).split("_")[1]

    door = doors['door_' + str(locker_num)]

    format_arm = format_objs(arm, 'robots')
    format_obj = format_objs(obj)
    format_locker = format_lockers(locker_num)
    format_door = format_doors(locker_num)

    current_frame, moves = move_to_locker_and_open(arm, door, locker_num, format_arm, \
        format_locker, format_door, current_frame, moves)

    #select a random object in another locker
    locker_num_2, door_2 = get_random_locker_num_and_door(exceptions=[int(locker_num)], nonempty=False)
    format_locker_2 = format_lockers(locker_num_2)
    format_door_2 = format_doors(locker_num_2)

    #approach and open the second locker (1 sec)
    current_frame, moves = move_to_locker_and_open(arm, door_2, locker_num_2, format_arm, \
        format_locker_2, format_door_2, current_frame, moves)

    #get in front of the object of the first locker (1 sec)
    current_frame, moves = take_obj_from_locker(current_frame, moves, arm, obj, format_arm, format_obj, format_locker)

    #bring it to second locker, put it in and close door
    current_frame, moves = position_item_to_locker_then_close(arm, \
            obj, door_2, locker_num_2, format_arm, format_obj, format_locker_2, format_door_2, current_frame, moves)

    #get to first handle
    current_frame = advance_frame(current_frame)
    arm.location = get_handle_location_for_door(door, locker_num)
    set_keyframe_for_objects([arm])
    set_keyframe_for_objects([door], data_path="rotation_euler")
    moves.append(action_builder("arm_to_locker", current_frame, format_arm, format_locker))

    #close door
    current_frame = advance_frame(current_frame)
    close_door(arm, door, locker_num)
    moves.append(action_builder("arm_close_door", current_frame, format_arm, format_door))

    ###14 SECONDS: get back to original position in 1 second
    current_frame = advance_frame(current_frame)
    return_to_origin(arm, starting_location)
    moves.append(action_builder("arm_to_origin", current_frame, format_arm))

    return moves

def put_object_in_scene(must_put_in_locker=False):
    moves = [phrase_structure]
    #go get an object out of scene
    ##choose a random out_of_scene object
    grabbed = select_random_object(locations=["ground_out"])
    print("Selected " + str(grabbed))

    #enable all collisions
    enable_collisions(get_all_objects(exceptions=["lights", "cameras"]))

    #get reference to the arm
    arm = random_select_rotate_arm()
    starting_location = [x for x in arm.location]

    #let the arm be controlled by the animation
    arm.rigid_body.kinematic = True
    #temporarily disable rigid_body physics for the grabbed object
    grabbed.rigid_body.kinematic = True

    #set the first keyframe for the arm and the grabbed object
    current_frame = 0
    set_current_frame(current_frame)
    set_keyframe_for_objects([arm, grabbed])

    format_arm = format_objs(arm, 'robots')
    format_grab = format_objs(grabbed)

    #go take the grabbed object (1 sec)
    current_frame = advance_frame(current_frame)
    arm.location[0] = grabbed.location[0]
    arm.location[1] = grabbed.location[1]
    #apply correction for z axis to get on top of the object
    arm.location[2] = grabbed.location[2] + (grabbed.dimensions[2] / 2)
    moves.append(action_builder("arm_exit_scene", current_frame, format_arm))
    #not seen by camera
    #moves.append(action_builder("arm_to_object", current_frame, format_arm, format_grab))
    #moves.append(action_builder("arm_grab_object", current_frame, format_arm, format_grab))
    set_keyframe_for_objects([arm, grabbed])

    #bring it in scene --> random choice
    ##put in on the ground and stay still?
    ##put it in a locker
    #until decision is made, leave object on the ground
    current_frame = advance_frame(current_frame)
    x, y = select_random_coordinates_on_visible_ground()
    arm.location[0] = grabbed.location[0] = x
    arm.location[1] = grabbed.location[1] = y
    set_keyframe_for_objects([arm, grabbed])
    moves.append(action_builder("arm_in_scene_w_object", current_frame, format_arm, format_grab))

    #rest for a random amount of time between 3 and 12 frames 
    current_frame = advance_frame(current_frame - random_scaled(9, 0))
    set_keyframe_for_objects([arm, grabbed])

    if must_put_in_locker:
        #choose random locker
        locker_num, door = get_random_locker_num_and_door()

        format_door = format_doors(locker_num)
        format_locker = format_lockers(locker_num)

        current_frame, moves = move_to_locker_and_open(arm, door, locker_num, format_arm, \
            format_locker, format_door, current_frame, moves)

        #get back to object
        current_frame = advance_frame(current_frame)
        arm.location[0] = grabbed.location[0]
        arm.location[1] = grabbed.location[1]
        #apply correction for z axis to get on top of the object
        arm.location[2] = grabbed.location[2] + grabbed.dimensions[2] / 2
        moves.append(action_builder("arm_to_object", current_frame, format_arm, format_grab))
        moves.append(action_builder("arm_grab_object", current_frame, format_arm, format_grab, duration=0))
        set_keyframe_for_objects([arm, grabbed])

        #get some distance from the locker
        if (grabbed.location[0] - grabbed.dimensions[0] / 2 < door.location[0] + door.dimensions[1]):
            current_frame = advance_frame(current_frame)
            arm.location[0] = grabbed.location[0] = door.location[0] + door.dimensions[1] + random_scaled(0.5, 2)
            set_keyframe_for_objects([arm, grabbed])

        #put object in locker and close door
        current_frame, moves = position_item_to_locker_then_close(arm, \
            grabbed, door, locker_num, format_arm, format_grab, format_locker, format_door, \
                current_frame, moves)

    #return to origin
    current_frame = advance_frame(current_frame)
    return_to_origin(arm, starting_location)
    moves.append(action_builder("arm_to_origin", current_frame, format_arm))

    return moves

def take_object_out_of_scene():
    moves = [phrase_structure]

    arm, grabbed, locker_num, door, format_arm, format_grab, \
        format_locker, format_door, current_frame, starting_location, moves = setup_taking_object(moves)

    #put item on ground
    current_frame = advance_frame(current_frame)
    x, y = select_random_coordinates_on_visible_ground()
    arm.location[0] = grabbed.location[0] = x
    arm.location[1] = grabbed.location[1] = y
    grabbed.location[2] = grabbed.dimensions[2] / 2
    arm.location[2] = grabbed.location[2] + grabbed.dimensions[2] / 2
    set_keyframe_for_objects([arm, grabbed])
    moves.append(action_builder("arm_to_ground", current_frame, format_arm, format_grab))

    #come back and close door
    current_frame = advance_frame(current_frame)
    arm.location = get_handle_location_for_door(door, locker_num)
    set_keyframe_for_objects([arm])
    set_keyframe_for_objects([door], data_path="rotation_euler")
    moves.append(action_builder("arm_to_locker", current_frame, format_arm, format_locker))

    #close door
    current_frame = advance_frame(current_frame)
    close_door(arm, door, locker_num)
    moves.append(action_builder("arm_close_door", current_frame, format_arm, format_locker))

    #get back to the object
    current_frame = advance_frame(current_frame)
    arm.location[0] = grabbed.location[0]
    arm.location[1] = grabbed.location[1]
    #apply correction for z axis to get on top of the object
    arm.location[2] = grabbed.location[2] + (grabbed.dimensions[2] / 2)
    moves.append(action_builder("arm_to_object", current_frame, format_arm, format_grab))
    moves.append(action_builder("arm_grab_object", current_frame, format_arm, format_grab, duration=0))
    set_keyframe_for_objects([arm, grabbed])

    #rest for a random amount of time between 3 and 12 frames
    current_frame = advance_frame(current_frame - random_scaled(9, 0))
    set_keyframe_for_objects([arm, grabbed])

    #randomly choose where to put the object
    x, y = select_random_coordinates_on_visible_ground()
    x += 7 #move to invisible ground
    current_frame = advance_frame(current_frame)
    arm.location[0] = grabbed.location[0] = x
    arm.location[1] = grabbed.location[1] = y
    set_keyframe_for_objects([arm, grabbed])
    moves.append(action_builder("arm_exit_scene_w_object", current_frame, format_arm, format_grab))

    #return to origin
    current_frame = advance_frame(current_frame)
    return_to_origin(arm, starting_location)
    moves.append(action_builder("arm_to_origin", current_frame, format_arm))

    return moves

def take_object_drop_and_replace():
    moves = [phrase_structure]

    #take a random object from a locker
    arm, grabbed, locker_num, door, format_arm, format_grab, format_locker, \
        format_door, current_frame, starting_location, moves = setup_taking_object(moves)

    #position arm and object in a random location in the scene
    current_frame = advance_frame(current_frame)
    x, y = select_random_coordinates_on_visible_ground()
    arm.location[0] = grabbed.location[0] = x
    arm.location[1] = grabbed.location[1] = y
    set_keyframe_for_objects([arm, grabbed])
    moves.append(action_builder("arm_to_unidentified_w_object", current_frame, format_arm, format_grab))

    #drop object on the ground by enabling its physics again
    current_frame = advance_frame(current_frame)
    grabbed.rigid_body.enabled = True
    grabbed.rigid_body.kinematic = False
    grabbed.keyframe_insert(data_path='rigid_body.enabled', frame=current_frame)
    grabbed.keyframe_insert(data_path='rigid_body.kinematic', frame=current_frame)
    set_keyframe_for_objects([arm])
    moves.append(action_builder("arm_drop_object", current_frame, format_arm, format_grab))

    #get another random object from the ground and put it in the open locker
    grabbed_2 = select_random_object(choices=['cubes','spheres','cones'], locations=["ground_in", "ground_out"])
    print("Selected " + str(grabbed))

    #disable its physics so that it can be controlled by the animation system
    grabbed_2.rigid_body.kinematic = True

    format_grab_2 = format_objs(grabbed_2)

    #move to selected object
    current_frame = advance_frame(current_frame)
    arm.location[0] = grabbed_2.location[0]
    arm.location[1] = grabbed_2.location[1]
    #apply correction for z axis to get on top of the object
    arm.location[2] = grabbed_2.location[2] + (grabbed_2.dimensions[2] / 2)
    set_keyframe_for_objects([arm, grabbed_2])
    moves.append(action_builder("arm_to_object", current_frame, format_arm, format_grab))
    moves.append(action_builder("arm_grab_object", current_frame, format_arm, format_grab, duration=0))

    #rest for half a second 
    current_frame = advance_frame(current_frame - 6)
    set_keyframe_for_objects([arm, grabbed_2])

    #put object in locker and close the door
    current_frame, moves = position_item_to_locker_then_close(arm, \
            grabbed_2, door, locker_num, format_arm, format_grab_2, format_locker, format_door, current_frame, moves)

    #rest for half a second 
    current_frame = advance_frame(current_frame - 6)
    set_keyframe_for_objects([arm, grabbed_2])

    #return to origin
    current_frame = advance_frame(current_frame)
    return_to_origin(arm, starting_location)
    moves.append(action_builder("arm_to_origin", current_frame, format_arm))

    return moves

def open_three_doors():
    moves = [phrase_structure]

    #randomly select and rotate arm
    arm = random_select_rotate_arm()

    #select three random different lockers
    locker_1, door_1 = get_random_locker_num_and_door()
    locker_2, door_2 = get_random_locker_num_and_door(exceptions=[int(locker_1)])
    locker_3, door_3 = get_random_locker_num_and_door(exceptions=[int(locker_1), int(locker_2)])

    print("Chosen doors: {}, {} and {}".format(locker_1, locker_2, locker_3))

    #enable all collisions
    enable_collisions(get_all_objects(exceptions=["lights", "cameras"]))

    #get arm starting location
    starting_location = [x for x in arm.location]

    #let the arm be controlled by the animation
    arm.rigid_body.kinematic = True

    current_frame = 0
    set_current_frame(current_frame)
    set_keyframe_for_objects([arm])

    format_arm = format_objs(arm, 'robots')
    format_door_1 = format_doors(locker_1)
    format_locker_1 = format_lockers(locker_1)
    format_door_2 = format_doors(locker_2)
    format_locker_2 = format_lockers(locker_2)
    format_door_3 = format_doors(locker_3)
    format_locker_3 = format_lockers(locker_3)

    doors = [door_1, door_2, door_3]
    lockers = [locker_1, locker_2, locker_3]
    arr_format_lockers = [format_locker_1, format_locker_2, format_locker_3]
    arr_format_doors = [format_door_1, format_door_2, format_door_3]

    for i in range(0, 3):
        #move to locker and open it
        current_frame, moves = move_to_locker_and_open(arm, doors[i], lockers[i], format_arm, \
            arr_format_lockers[i], arr_format_doors[i], current_frame, moves)
        
        #rest for a random amount of time between 3 and 12 frames
        current_frame = advance_frame(current_frame - random_scaled(9, 0))
        set_keyframe_for_objects([arm])

    #return to original position
    current_frame = advance_frame(current_frame)
    return_to_origin(arm, starting_location)
    moves.append(action_builder("arm_to_origin", current_frame, format_arm))

    return moves

def swap_from_ground():
    moves = [phrase_structure]

    #take an object from a locker
    arm, grabbed, locker_num, door, format_arm, format_grab, format_locker, \
        format_door, current_frame, starting_location, moves = setup_taking_object(moves)

    #put the object on the ground, in a random visible position
    current_frame = advance_frame(current_frame)
    x, y = select_random_coordinates_on_visible_ground()
    arm.location[0] = grabbed.location[0] = x
    arm.location[1] = grabbed.location[1] = y
    grabbed.location[2] = grabbed.dimensions[2] / 2
    arm.location[2] = grabbed.location[2] + grabbed.dimensions[2] / 2
    set_keyframe_for_objects([arm, grabbed])
    moves.append(action_builder("arm_to_ground", current_frame, format_arm, format_grab))

    #choose a random locker and open it
    locker_num_2, door_2 = get_random_locker_num_and_door(exceptions=[int(locker_num)])
    format_locker_2 = format_lockers(locker_num_2)
    format_door_2 = format_doors(locker_num_2)

    current_frame, moves = move_to_locker_and_open(arm, door_2, locker_num_2, format_arm, \
        format_locker_2, format_door_2, current_frame, moves)

    #take the first object on the ground
    current_frame = advance_frame(current_frame)
    arm.location[0] = grabbed.location[0]
    arm.location[1] = grabbed.location[1]
    arm.location[2] = grabbed.location[2] + grabbed.dimensions[2] / 2
    set_keyframe_for_objects([arm, grabbed])
    moves.append(action_builder("arm_to_object", current_frame, format_arm, format_grab))

    #put it in the locker
    current_frame, moves = position_item_to_locker_then_close(arm, grabbed, door_2, \
        locker_num_2, format_arm, format_grab, format_locker_2, format_door_2, current_frame, moves)

    #return to origin
    current_frame = advance_frame(current_frame)
    return_to_origin(arm, starting_location)
    moves.append(action_builder("arm_to_origin", current_frame, format_arm))

    return moves

def put_two_objects_on_ground():
    moves = [phrase_structure]

    #take an object from a locker
    arm, grabbed, locker_num, door, format_arm, format_grab, format_locker, \
        format_door, current_frame, starting_location, moves = setup_taking_object(moves)

    #put the item on the ground
    current_frame, moves = put_item_in_visible_position(current_frame, arm, grabbed, format_arm, format_grab, moves)

    #give physics back to the object
    grabbed.rigid_body.kinematic = False
    grabbed.keyframe_insert(data_path='rigid_body.kinematic', frame=current_frame)

    #choose another nonempty random locker and open it
    locker_num_2, door_2 = get_random_locker_num_and_door(exceptions=[int(locker_num)], nonempty=True)
    format_locker_2 = format_lockers(locker_num_2)
    format_door_2 = format_doors(locker_num_2)

    current_frame, moves = move_to_locker_and_open(arm, door_2, locker_num_2, format_arm, \
        format_locker_2, format_door_2, current_frame, moves)

    #take a random object in that locker and put it on the ground
    grabbed_2 = select_random_object(locations=['loc_' + str(locker_num_2)])
    format_grab_2 = format_objs(grabbed_2)
    #disable physics for second object
    grabbed_2.rigid_body.kinematic = True

    current_frame, moves = take_obj_from_locker(current_frame, moves, arm, grabbed_2, format_arm, \
        format_grab_2, format_locker_2)

    #put it on the ground at visibile position
    current_frame, moves = put_item_in_visible_position(current_frame, arm, grabbed_2, format_arm, \
        format_grab_2, moves)

    #close one of the two doors (or none)
    current_frame = advance_frame(current_frame)
    choice = random()
    door_to_close = 'none' if choice < 0.2 else 'first' if choice < 0.6 else 'second'
    if door_to_close == 'first':
        #move to and close first door
        arm.location = get_handle_location_for_door(door, locker_num)
        set_keyframe_for_objects([arm])
        set_keyframe_for_objects([door], data_path='rotation_euler')
        moves.append(action_builder("arm_to_locker", current_frame, format_arm, format_locker))
        
        current_frame = advance_frame(current_frame)
        close_door(arm, door, locker_num)
        set_keyframe_for_objects([door], data_path='rotation_euler')
        moves.append(action_builder("arm_close_door", current_frame, format_arm, format_door))
        
    elif door_to_close == 'second':
        #move to and close second door
        arm.location = get_handle_location_for_door(door_2, locker_num_2)
        set_keyframe_for_objects([door_2], data_path='rotation_euler')
        set_keyframe_for_objects([arm])
        moves.append(action_builder("arm_to_locker", current_frame, format_arm, format_locker_2))

        current_frame = advance_frame(current_frame)
        close_door(arm, door_2, locker_num_2)
        set_keyframe_for_objects([door_2], data_path='rotation_euler')
        moves.append(action_builder("arm_close_door", current_frame, format_arm, format_door_2))
        
    else:
        #do nothing
        pass

    set_keyframe_for_objects([arm])

    #return to origin
    current_frame = advance_frame(current_frame)
    return_to_origin(arm, starting_location)
    moves.append(action_builder("arm_to_origin", current_frame, format_arm))

    return moves

###################################################################

activities = {
    'move_sphere_to_other_locker' : partial(move_obj_to_other_locker, obj_type='spheres'),
    'move_cube_to_other_locker' : partial(move_obj_to_other_locker, obj_type='cubes'),
    'get_new_object' : partial(put_object_in_scene, must_put_in_locker=False),
    'put_new_object_in_locker' : partial(put_object_in_scene, must_put_in_locker=True),
    'take_object_out_of_scene' : take_object_out_of_scene,
    'take_object_drop_and_replace' : take_object_drop_and_replace,
    'open_three_doors' : open_three_doors,
    'swap_from_ground' : swap_from_ground,
    'put_two_objects_on_ground': put_two_objects_on_ground,
}

#get the path for saving the files
argv = sys.argv[sys.argv.index("--") + 1:]  # get all args after "--"
out_path = argv[0]

#get additional optional arguments
parser = argparse.ArgumentParser(
    description = 'Run blender in background mode',
    prog = "blender -b dataset_stem.blend -P "+__file__+" -- out_path",
)
parser.add_argument('--activity', '-a', type=str)
args = parser.parse_args(argv[1:])

#set a random luminosity for the scene
set_random_luminosity(objects["lights"]["light_0"])

#set a random camera rotation (within boundaries) on a 20% chance
random_rotate_camera(objects["cameras"]["camera_0"])

#choose an activity and execute it
if args.activity:
    try:
        random_activity = args.activity
        print("Chosen " + str(args.activity) + " activity")
    except:
        print(str(args.activity) + " is not a correct activity")
else:
    random_activity = choose_activity()
moves = activities[random_activity]()

folder = ''
#set filepath
while True:
    folder = os.path.join(out_path, random_activity, datetime.now().strftime("%d%m%Y_%H%M%S"))
    #if folder doesn't exist, create it and start rendering, else retry in a second to avoid problems
    if not os.path.exists(folder):
        os.mkdir(folder)
        break
    else:
        time.sleep(1)
bpy.context.scene.render.filepath = os.path.join(folder, "frame")

#bake physics
for obj in get_all_objects(exceptions=["lights", "cameras"]):
    obj.select_set(True)
    bpy.ops.ptcache.bake_all(bake=True)

#render activity
render_and_end()

#create actions file
with open(os.path.join(folder, 'actions.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(moves)

print("Written actions file!")