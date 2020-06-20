from env_params.actions_phrases import phrase_structure
from env_params.refs import *
from functions.timeline_utilities import *
from env_params.actions_phrases import *
from functions.env_utilities import *
from functions.common_activities import *

def take_object_drop_and_replace():
    moves = [phrase_structure]

    #take a random object from a locker
    arm, grabbed, locker_num, door, format_arm, format_grab, format_locker, \
        format_door, current_frame, starting_location, moves = setup_taking_object(moves)

    #select another random object from the ground to put in the open locker
    grabbed_2 = select_random_object(choices=['cubes','spheres','cones'], locations=["ground_in", "ground_out"])
    print("Selected " + str(grabbed))
    #set a keyframe for its physics
    grabbed_2.rigid_body.kinematic = False
    grabbed_2.keyframe_insert(data_path='rigid_body.kinematic', frame=current_frame)
    format_grab_2 = format_objs(grabbed_2)

    #position arm and object in a random location in the scene
    current_frame = advance_frame(current_frame)
    x, y = select_random_coordinates_on_visible_ground()
    arm.location[0] = grabbed.location[0] = x
    arm.location[1] = grabbed.location[1] = y
    set_keyframe_for_objects([arm, grabbed])
    moves.append(action_builder("arm_to_unidentified_w_object", current_frame, format_arm, format_grab))

    #drop object on the ground by enabling its physics again
    grabbed.rigid_body.enabled = True
    grabbed.rigid_body.kinematic = False
    grabbed.keyframe_insert(data_path='rigid_body.enabled', frame=current_frame)
    grabbed.keyframe_insert(data_path='rigid_body.kinematic', frame=current_frame)
    moves.append(action_builder("arm_drop_object", current_frame, format_arm, format_grab))

    #rest for a random amount of time while object falls to the ground
    current_frame = advance_frame(current_frame - random_scaled(9, 0))
    set_keyframe_for_objects([arm])

    #make other object kinematic
    grabbed_2.rigid_body.kinematic = True
    grabbed_2.keyframe_insert(data_path='rigid_body.kinematic', frame=current_frame)

    #move to selected object
    current_frame = advance_frame(current_frame)
    arm.location[0] = grabbed_2.location[0]
    arm.location[1] = grabbed_2.location[1]
    #apply correction for z axis to get on top of the object
    arm.location[2] = grabbed_2.location[2] + (grabbed_2.dimensions[2] / 2)
    set_keyframe_for_objects([arm, grabbed_2])
    moves.append(action_builder("arm_to_object", current_frame, format_arm, format_grab))
    moves.append(action_builder("arm_grab_object", current_frame, format_arm, format_grab, duration=0))

    #rest for a while
    current_frame = advance_frame(current_frame - 3)
    set_keyframe_for_objects([arm, grabbed_2])

    #put object in locker and close the door
    current_frame, moves = position_item_to_locker_then_close(arm, \
            grabbed_2, door, locker_num, format_arm, format_grab_2, format_locker, format_door, current_frame, moves)

    #return to origin
    current_frame = advance_frame(current_frame)
    return_to_origin(arm, starting_location)
    moves.append(action_builder("arm_to_origin", current_frame, format_arm))

    return moves