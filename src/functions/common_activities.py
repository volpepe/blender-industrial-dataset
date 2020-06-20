from mathutils import Vector
from math import radians

from env_params.actions_phrases import *
from functions.env_utilities import *
from functions.timeline_utilities import *
from env_params.refs import *

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

    #get in front of the object and take it
    current_frame, moves = take_obj_from_locker(current_frame, moves, arm, grabbed, \
        format_arm, format_grab, format_locker)

    return arm, grabbed, locker_num, door, format_arm, format_grab, format_locker, \
        format_door, current_frame, starting_location, moves

def position_item_to_locker_then_close(arm, grabbed, door, locker_num, format_arm, format_grab, \
        format_locker, format_door, current_frame, moves):
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
    arm.location[0] = placeholder + grabbed.dimensions[0] if placeholder < 3 else 3
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