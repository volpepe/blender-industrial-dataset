from env_params.actions_phrases import phrase_structure
from env_params.refs import *
from functions.timeline_utilities import *
from env_params.actions_phrases import *
from functions.env_utilities import *
from functions.common_activities import *

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
