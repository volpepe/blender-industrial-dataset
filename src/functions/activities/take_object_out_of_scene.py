from env_params.actions_phrases import phrase_structure
from env_params.refs import *
from functions.timeline_utilities import *
from env_params.actions_phrases import *
from functions.env_utilities import *
from functions.common_activities import *

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
    #get some height
    current_frame = advance_frame(current_frame)
    arm.location[2] += 1
    grabbed.location[2] += 1
    set_keyframe_for_objects([arm, grabbed])
    #move away
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