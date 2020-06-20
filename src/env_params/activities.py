from functools import partial
from random import choice

from functions.activities import *

activities = {
    'move_sphere_to_other_locker' : partial(move_obj_to_other_locker, obj_type='spheres'),
    'move_cube_to_other_locker' : partial(move_obj_to_other_locker, obj_type='cubes'),
    'get_new_object' : partial(put_object_in_scene, must_put_in_locker=False),
    'put_new_object_in_locker' : partial(put_object_in_scene, must_put_in_locker=True),
    'take_object_out_of_scene' : take_object_out_of_scene,
    'take_object_drop_and_replace' : take_object_drop_and_replace,
    'open_three_doors' : open_three_doors,
    'swap_from_ground' : swap_from_ground,
    'put_two_objects_on_ground': put_two_objects_on_ground,
    'put_on_top': put_on_top
}

# Choose a random activity from the ones in the activity dictionary
def choose_activity():
    random_activity = choice(list(activities.keys()))
    print("Chosen activity: " + random_activity)
    return random_activity