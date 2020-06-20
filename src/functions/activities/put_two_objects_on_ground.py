from env_params.actions_phrases import phrase_structure
from env_params.refs import *
from functions.timeline_utilities import *
from env_params.actions_phrases import *
from functions.env_utilities import *
from functions.common_activities import *

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