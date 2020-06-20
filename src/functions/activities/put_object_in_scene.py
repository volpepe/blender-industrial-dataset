from env_params.actions_phrases import phrase_structure
from env_params.refs import *
from functions.timeline_utilities import *
from env_params.actions_phrases import *
from functions.env_utilities import *
from functions.common_activities import *

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