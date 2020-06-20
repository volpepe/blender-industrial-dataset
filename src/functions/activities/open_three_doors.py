from env_params.actions_phrases import phrase_structure
from env_params.refs import *
from functions.timeline_utilities import *
from env_params.actions_phrases import *
from functions.env_utilities import *
from functions.common_activities import *

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