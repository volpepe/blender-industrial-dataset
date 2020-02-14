import bpy
from random import randint, choice, random
from mathutils import Vector
import os
from datetime import datetime
from math import radians
import sys
from functools import partial
import csv

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
        'sphere_4' : bpy.data.objects["Sphere.005"],
    },
    'cones' : {
        'cone_0' : bpy.data.objects["Cone"],
        'cone_1' : bpy.data.objects["Cone.001"],
        'cone_1' : bpy.data.objects["Cone.002"],
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

def format_objs(obj, typ):
    for key, val in objects.get(typ).items():
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

phrase_structure = ["who", "doesWhat", "toWhom", "whereAdverb", "where", "whileDoingWhat", "whileToWhom"]

actions = {
    'arm_to_locker': lambda arm, locker, null : [arm, "moved", "itself", "to", locker, "", ""],
    'arm_to_object': lambda arm, obj, null : [arm, "moved", "itself", "in front of", obj, "", ""],
    'arm_open_door': lambda arm, door, null : [arm, "opened", door, "", "", "", ""],
    'arm_close_door': lambda arm, door, null : [arm, "closed", door, "", "", "", ""],
    'arm_into_locker': lambda arm, locker, null: [arm, "moved", "itself", "into", locker, "", ""],
    'arm_out_locker': lambda arm, locker, null: [arm, "moved", "itself", "out of", locker, "", ""],
    'arm_grab_object': lambda arm, obj, null: [arm, "grabbed", obj, "", "", "", ""],
    'arm_out_locker_w_object': lambda arm, locker, obj: [arm, "moved", "itself", "out of", locker, "holding", obj],
    'arm_to_locker_w_object': lambda arm, locker, obj: [arm, "moved", "itself", "in front of", locker, "holding", obj],
    'arm_to_object_w_object': lambda arm, obj_1, obj_2: [arm, "moved", "itself", "in front of", obj_1, "holding", obj_2],
    'arm_position_object_in_locker': lambda arm, obj, locker: [arm, "positioned", obj, "into", locker, "", ""],
    'arm_to_origin': lambda arm, null, null_2: [arm, "moved", "itself", "to", "original position", "", ""],
    'arm_exit_scene' : lambda arm, null, null_2: [arm, "moved", "itself", "out of", "scene", "", ""],
    "arm_in_scene" : lambda arm, null, null_2: [arm, "moved", "itself", "into", "scene", "", ""],
    "arm_in_scene_w_object" : lambda arm, obj, null: [arm, "moved", "itself", "into", "scene", "holding", obj],
    "arm_to_ground" : lambda arm, obj, null: [arm, "put", obj, "on", "the ground", "", ""],
    "arm_exit_scene_w_object" : lambda arm, obj, null: [arm, "moved", "itself", "out of", "scene", "holding", obj],
}

def action_builder(action, var_1=None, var_2=None, var_3=None):
    return actions.get(action)(var_1, var_2, var_3)

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
                break
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
    x_min = 1.12
    x_max = 2.25
    y_min = -6.6
    y_max = 5.55
    return random_scaled(x_max, x_min), random_scaled(y_max, y_min)

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


def move_sphere_to_locker():

    moves = [phrase_structure]

    #select a random sphere in a locker
    sphere = select_random_object(choices=["spheres"], locations=[x for x in object_locations.keys() if x not in ["ground_in", "ground_out"]])
    print("Selected " + str(sphere))

    #enable all collisions
    enable_collisions(get_all_objects(exceptions=["lights", "cameras"]))

    #get reference to the arm
    arm = objects["robots"]["arm"]
    starting_location = [x for x in arm.location]

    #let the arm be controlled by the animation
    arm.rigid_body.kinematic = True
    #temporarily disable rigid_body physics for the sphere
    sphere.rigid_body.kinematic = True

    #set the first keyframe for the arm, the sphere and the locker door
    current_frame = 0
    set_current_frame(current_frame)
    set_keyframe_for_objects([arm, sphere])

    locker_num = get_locker_loc_for_object(sphere).split("_")[1]

    door = doors['door_' + str(locker_num)]

    format_arm = format_objs(arm, 'robots')
    format_sphere = format_objs(sphere, 'spheres')
    format_locker = format_lockers(locker_num)
    format_door = format_doors(locker_num)

    #approach its locker (1 sec)
    #get the locker location
    handle_0 = get_handle_location_for_object(sphere)
    if handle_0 is None:
        return None #nothing happens
    #move arm to locker
    current_frame = advance_frame(current_frame)
    arm.location = handle_0
    set_keyframe_for_objects([arm, door, sphere])
    set_keyframe_for_objects([door], data_path="rotation_euler")
    moves.append(action_builder("arm_to_locker", format_arm, format_locker))
    
    #open the locker (1 secs)
    current_frame = advance_frame(current_frame)
    open_locker(arm, door, locker_num)
    moves.append(action_builder("arm_open_door", format_arm, format_door))

    #select a random object in another locker
    locker_num_2, door_2 = get_random_locker_num_and_door(exceptions=[int(locker_num)], nonempty=False)
    format_locker_2 = format_lockers(locker_num_2)
    format_door_2 = format_doors(locker_num_2)

    #approach the second locker (1 sec)
    current_frame = advance_frame(current_frame)
    arm.location = get_handle_location_for_door(door_2, locker_num_2)
    set_keyframe_for_objects([arm])
    set_keyframe_for_objects([door_2], data_path="rotation_euler")
    moves.append(action_builder("arm_to_locker", format_arm, format_locker_2))

    #open the second locker (1 sec)
    current_frame = advance_frame(current_frame)
    open_locker(arm, door_2, locker_num_2)
    moves.append(action_builder("arm_open_door", format_arm, format_door_2))

    #get in front of the object of the first locker (1 sec)
    #move in y and z
    current_frame = advance_frame(current_frame)
    arm.location[1] = sphere.location[1]
    #apply correction for z axis to get on top of the object
    arm.location[2] = sphere.location[2] + (sphere.dimensions[2] / 2)
    set_keyframe_for_objects([arm])
    moves.append(action_builder("arm_to_locker", format_arm, format_locker))
    moves.append(action_builder("arm_to_object", format_arm, format_sphere))

    #get item (1 sec)
    #move in x
    current_frame = advance_frame(current_frame)
    placeholder = arm.location[0]
    arm.location[0] = sphere.location[0]
    set_keyframe_for_objects([arm, sphere])
    moves.append(action_builder("arm_into_locker", format_arm, format_locker))
    moves.append(action_builder("arm_grab_object", format_arm, format_sphere))

    #get out with item (1 sec)
    current_frame = advance_frame(current_frame)
    arm.location[0] = sphere.location[0] = placeholder
    set_keyframe_for_objects([arm, sphere])
    moves.append(action_builder("arm_out_locker_w_object", format_arm, format_locker, format_sphere))

    #take the item to second locker (1 sec)
    #first move in y and z to second locker
    current_frame = advance_frame(current_frame)
    #x and y are random within the locker boundaries
    positioning_x, positioning_y = get_random_x_and_y_within_locker(door_2)
    correct_x = door_2.location[0] - positioning_x
    correct_y = door_2.location[1] + positioning_y
    #correct z to put the object exactly at the height of the shelf of the locker
    correct_z = door_2.location[2] - door_2.dimensions[2] / 2 + sphere.dimensions[2] / 2
    #move in y and z
    arm.location[1] = sphere.location[1] = correct_y
    sphere.location[2] = correct_z
    arm.location[2] = correct_z + sphere.dimensions[2] / 2
    set_keyframe_for_objects([arm, sphere])
    moves.append(action_builder("arm_to_locker_w_object", format_arm, format_locker_2, format_sphere))

    #put it in(1 sec)
    #move in x
    current_frame = advance_frame(current_frame)
    placeholder = arm.location[0]
    arm.location[0] = sphere.location[0] = correct_x
    set_keyframe_for_objects([arm, sphere])
    moves.append(action_builder("arm_position_object_in_locker", format_arm, format_sphere, format_locker_2))

    #get out (1 sec)
    current_frame = advance_frame(current_frame)
    arm.location[0] = placeholder
    set_keyframe_for_objects([arm])
    moves.append(action_builder("arm_out_locker", format_arm, format_locker_2))

    #close lockers (4 secs)
    #get to handle
    current_frame = advance_frame(current_frame)
    arm.location = get_handle_location_for_door(door_2, locker_num_2)
    set_keyframe_for_objects([arm])
    set_keyframe_for_objects([door_2], data_path="rotation_euler")

    #close door
    current_frame = advance_frame(current_frame)
    close_door(arm, door_2, locker_num_2)
    moves.append(action_builder("arm_close_door", format_arm, format_door_2))

    #get to handle
    current_frame = advance_frame(current_frame)
    arm.location = get_handle_location_for_door(door, locker_num)
    set_keyframe_for_objects([arm])
    set_keyframe_for_objects([door], data_path="rotation_euler")
    moves.append(action_builder("arm_to_locker", format_arm, format_locker))

    #close door
    current_frame = advance_frame(current_frame)
    close_door(arm, door, locker_num)
    moves.append(action_builder("arm_close_door", format_arm, format_door))

    ###14 SECONDS: get back to original position in 1 second
    current_frame = advance_frame(current_frame)
    return_to_origin(arm, starting_location)
    moves.append(action_builder("arm_to_origin", format_arm))
    
    return moves

def put_object_in_scene(must_put_in_locker=False):
    moves = []
    #go get an object out of scene
    ##choose a random out_of_scene object
    grabbed = select_random_object(locations=["ground_out"])
    print("Selected " + str(grabbed))

    #enable all collisions
    enable_collisions(get_all_objects(exceptions=["lights", "cameras"]))

    #get reference to the arm
    arm = objects["robots"]["arm"]
    starting_location = [x for x in arm.location]

    #let the arm be controlled by the animation
    arm.rigid_body.kinematic = True
    #temporarily disable rigid_body physics for the grabbed object
    grabbed.rigid_body.kinematic = True

    #set the first keyframe for the arm and the grabbed object
    current_frame = 0
    set_current_frame(current_frame)
    set_keyframe_for_objects([arm, grabbed])

    #go take the grabbed object (1 sec)
    current_frame = advance_frame(current_frame)
    arm.location[0] = grabbed.location[0]
    arm.location[1] = grabbed.location[1]
    #apply correction for z axis to get on top of the object
    arm.location[2] = grabbed.location[2] + (grabbed.dimensions[2] / 2)
    moves.append(actions["arm_exit_scene"].format(str(grabbed)))
    moves.append(actions["arm_to_object"].format(str(grabbed)))
    moves.append(actions["arm_grab_object"].format(str(grabbed)))
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
    moves.append(actions["arm_in_scene_w_object"].format(str(grabbed)))

    #rest for a second 
    current_frame = advance_frame(current_frame)
    set_keyframe_for_objects([arm, grabbed])

    if must_put_in_locker:
        #choose random locker
        locker_num, door = get_random_locker_num_and_door()

        #move arm to the handle
        current_frame = advance_frame(current_frame)
        arm.location = get_handle_location_for_door(door, locker_num)
        set_keyframe_for_objects([arm])
        moves.append(actions["arm_to_closed_locker"].format(str(locker_num)))

        #set keyframe for door rotation
        set_keyframe_for_objects([door], data_path="rotation_euler")

        #open locker
        current_frame = advance_frame(current_frame)
        open_locker(arm, door, locker_num)
        moves.append(actions["arm_open_door"].format(str(locker_num)))

        #get back to object
        current_frame = advance_frame(current_frame)
        arm.location[0] = grabbed.location[0]
        arm.location[1] = grabbed.location[1]
        #apply correction for z axis to get on top of the object
        arm.location[2] = grabbed.location[2] + grabbed.dimensions[2] / 2
        moves.append(actions["arm_to_object"].format(str(grabbed)))
        moves.append(actions["arm_grab_object"].format(str(grabbed)))
        set_keyframe_for_objects([arm, grabbed])

        #put object in locker
        #first move in y and z to locker
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
        moves.append(actions["arm_to_open_locker_w_object"].format(str(locker_num), str(grabbed)))

        #put it in(1 sec)
        #move in x
        current_frame = advance_frame(current_frame)
        placeholder = arm.location[0]
        arm.location[0] = grabbed.location[0] = correct_x
        set_keyframe_for_objects([arm, grabbed])
        moves.append(actions["arm_position_object_in_locker"].format(str(grabbed), str(locker_num)))

        #get out (1 sec)
        current_frame = advance_frame(current_frame)
        arm.location[0] = placeholder
        set_keyframe_for_objects([arm])
        moves.append(actions["arm_out_locker"].format(str(locker_num)))

        #close lockers
        #get to handle
        current_frame = advance_frame(current_frame)
        arm.location = get_handle_location_for_door(door, locker_num)
        set_keyframe_for_objects([arm])
        set_keyframe_for_objects([door], data_path="rotation_euler")

        #close door
        current_frame = advance_frame(current_frame)
        close_door(arm, door, locker_num)
        moves.append(actions["arm_close_door"].format(str(locker_num)))

    #return to origin
    current_frame = advance_frame(current_frame)
    return_to_origin(arm, starting_location)
    moves.append(actions["arm_to_origin"])

    return moves

def take_object_out_of_scene():
    moves = []

    #select a random object in a locker
    grabbed = select_random_object(locations=[x for x in object_locations.keys() if x not in ["ground_in", "ground_out"]])
    print("Selected " + str(grabbed))

    #enable all collisions
    enable_collisions(get_all_objects(exceptions=["lights", "cameras"]))

    #get reference to the arm
    arm = objects["robots"]["arm"]
    starting_location = [x for x in arm.location]

    #let the arm be controlled by the animation
    arm.rigid_body.kinematic = True
    #temporarily disable rigid_body physics for the sphere
    grabbed.rigid_body.kinematic = True

    #set the first keyframe for the arm, the object and the locker door
    current_frame = 0
    set_current_frame(current_frame)
    set_keyframe_for_objects([arm, grabbed])

    locker_num = get_locker_loc_for_object(grabbed).split("_")[1]

    door = doors['door_' + str(locker_num)]

    #approach its locker (1 sec)
    #get the locker location
    handle_0 = get_handle_location_for_object(grabbed)
    if handle_0 is None:
        return None #nothing happens
    #move arm to locker
    current_frame = advance_frame(current_frame)
    arm.location = handle_0
    set_keyframe_for_objects([arm, door, grabbed])
    set_keyframe_for_objects([door], data_path="rotation_euler")
    moves.append(actions["arm_to_closed_locker"].format(str(locker_num)))
    
    #open the locker (1 secs)
    current_frame = advance_frame(current_frame)
    open_locker(arm, door, locker_num)
    moves.append(actions["arm_open_door"].format(str(locker_num)))

    #get in front of the object (1 sec)
    #move in y and z
    current_frame = advance_frame(current_frame)
    arm.location[1] = grabbed.location[1]
    #apply correction for z axis to get on top of the object
    arm.location[2] = grabbed.location[2] + grabbed.dimensions[2] / 2
    set_keyframe_for_objects([arm])
    moves.append(actions["arm_to_object"].format(str(grabbed)))

    #get item (1 sec)
    #move in x
    current_frame = advance_frame(current_frame)
    placeholder = arm.location[0]
    arm.location[0] = grabbed.location[0]
    set_keyframe_for_objects([arm, grabbed])
    moves.append(actions["arm_into_locker"].format(str(locker_num)))
    moves.append(actions["arm_grab_object"].format(str(grabbed)))

    #get out with item (1 sec)
    current_frame = advance_frame(current_frame)
    arm.location[0] = grabbed.location[0] = placeholder
    set_keyframe_for_objects([arm, grabbed])
    moves.append(actions["arm_out_locker_w_object"].format(str(locker_num), str(grabbed)))

    #put item on ground
    current_frame = advance_frame(current_frame)
    x, y = select_random_coordinates_on_visible_ground()
    arm.location[0] = grabbed.location[0] = x
    arm.location[1] = grabbed.location[1] = y
    grabbed.location[2] = grabbed.dimensions[2] / 2
    arm.location[2] = grabbed.location[2] + grabbed.dimensions[2] / 2
    set_keyframe_for_objects([arm, grabbed])
    moves.append(actions["arm_to_ground"].format(str(grabbed)))

    #come back and close door
    current_frame = advance_frame(current_frame)
    arm.location = get_handle_location_for_door(door, locker_num)
    set_keyframe_for_objects([arm])
    set_keyframe_for_objects([door], data_path="rotation_euler")
    moves.append(actions["arm_to_open_locker"].format(str(locker_num)))

    #close door
    current_frame = advance_frame(current_frame)
    close_door(arm, door, locker_num)
    moves.append(actions["arm_close_door"].format(str(locker_num)))

    #get back to the object
    current_frame = advance_frame(current_frame)
    arm.location[0] = grabbed.location[0]
    arm.location[1] = grabbed.location[1]
    #apply correction for z axis to get on top of the object
    arm.location[2] = grabbed.location[2] + (grabbed.dimensions[2] / 2)
    moves.append(actions["arm_to_object"].format(str(grabbed)))
    moves.append(actions["arm_grab_object"].format(str(grabbed)))
    set_keyframe_for_objects([arm, grabbed])

    #rest for a second
    current_frame = advance_frame(current_frame)
    set_keyframe_for_objects([arm, grabbed])

    #randomly choose where to put the object
    x, y = select_random_coordinates_on_visible_ground()
    x += 7 #move to invisible ground
    current_frame = advance_frame(current_frame)
    arm.location[0] = grabbed.location[0] = x
    arm.location[1] = grabbed.location[1] = y
    set_keyframe_for_objects([arm, grabbed])
    moves.append(actions["arm_exit_scene_w_object"].format(str(grabbed)))

    #return to origin
    current_frame = advance_frame(current_frame)
    return_to_origin(arm, starting_location)
    moves.append(actions["arm_to_origin"])

    return moves

###################################################################

activities = {
    'move_sphere_to_other_locker' : move_sphere_to_locker,
    #'get_new_object' : partial(put_object_in_scene, must_put_in_locker=False),
    #'put_new_object_in_locker' : partial(put_object_in_scene, must_put_in_locker=True),
    #'take_object_out_of_scene' : take_object_out_of_scene,
}

#get the path for saving the files
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"
out_path = argv[0]

#set a random luminosity for the scene
set_random_luminosity(objects["lights"]["light_0"])

#set a random camera rotation (within boundaries) on a 20% chance
random_rotate_camera(objects["cameras"]["camera_0"]) 

#choose an activity and execute it
random_activity = choose_activity()
moves = activities[random_activity]()

#set filepath
folder = os.path.join(out_path, random_activity, datetime.now().strftime("%d%m%Y_%H%M%S"))
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