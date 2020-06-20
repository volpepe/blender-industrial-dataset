from env_params.actions_phrases import phrase_structure
from env_params.refs import *
from functions.timeline_utilities import *
from env_params.actions_phrases import *
from functions.env_utilities import *
from functions.common_activities import *

def put_on_top():
    moves = [phrase_structure]

    #take an object from a locker
    arm, grabbed, locker_num, door, format_arm, format_grab, format_locker, \
        format_door, current_frame, starting_location, moves = setup_taking_object(moves)

    #put it on top of the locker
    #move in z first
    current_frame = advance_frame(current_frame)
    arm.location[2] = physical_locker.location[2] + physical_locker.dimensions[2] / 2 + grabbed.dimensions[2]
    grabbed.location[2] = arm.location[2] - grabbed.dimensions[2] / 2
    set_keyframe_for_objects([arm, grabbed])
    moves.append(action_builder("arm_to_unidentified_w_object", current_frame, format_arm, format_grab))

    #move in x and y at random location on locker
    current_frame = advance_frame(current_frame)
    placeholder = Vector(arm.location)
    x, y = get_random_location_on_locker()
    arm.location[0] = grabbed.location[0] = x
    arm.location[1] = grabbed.location[1] = y
    set_keyframe_for_objects([arm, grabbed])
    moves.append(action_builder("arm_on_top_w_object", current_frame, format_arm, format_grab))

    #get down and close door
    current_frame = advance_frame(current_frame)
    arm.location = placeholder
    set_keyframe_for_objects([arm])

    current_frame = advance_frame(current_frame)
    arm.location = get_handle_location_for_door(door, locker_num)
    set_keyframe_for_objects([door], data_path='rotation_euler')
    set_keyframe_for_objects([arm])
    moves.append(action_builder("arm_to_locker", current_frame, format_arm, format_locker))

    current_frame = advance_frame(current_frame)
    close_door(arm, door, locker_num)
    set_keyframe_for_objects([door], data_path='rotation_euler')
    moves.append(action_builder("arm_close_door", current_frame, format_arm, format_door))

    #return to origin
    current_frame = advance_frame(current_frame)
    return_to_origin(arm, starting_location)
    moves.append(action_builder("arm_to_origin", current_frame, format_arm))

    return moves