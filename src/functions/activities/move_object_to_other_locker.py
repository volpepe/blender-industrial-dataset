from env_params.actions_phrases import phrase_structure
from env_params.refs import *
from functions.timeline_utilities import *
from env_params.actions_phrases import *
from functions.env_utilities import *
from functions.common_activities import *

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