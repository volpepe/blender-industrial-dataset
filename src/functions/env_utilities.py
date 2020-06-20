from random import randint, choice, random
from mathutils import Vector
from math import radians

from env_params.refs import *

brightness_levels = [x for x in range(2000, 60000, 1000)]

def random_scaled(max, min):
    return min + random() * (max - min)

def enable_collisions(objs):
    for obj in objs:
        obj.rigid_body.enabled = True
        obj.rigid_body.kinematic = False

# Gets the location of the locker's handle
def get_handle_location_for_object(obj):
    locker = get_locker_loc_for_object(obj)
    if locker is not None and locker != 'ground_in' and locker != 'ground_out':
        locker_num = locker.split('_')[1]
        door = doors['door_' + locker_num]
        return get_handle_location_for_door(door, locker_num)
    else:
        return None

def get_random_locker_num_and_door(exceptions=[], nonempty=False):
    while True: 
        i = randint(0, len(doors.keys()) - 1)
        if i not in exceptions:
            if not nonempty:
                print("Chosen door " + str(i))
                break
            elif len(object_locations['loc_' + str(i)]) > 0:
                print("Chosen door " + str(i))
                break
            else:
                pass
    return i, doors["door_" + str(i)]

# Returns a string that indicates where the object is
def get_locker_loc_for_object(obj):
    for locker in [x for x in object_locations.keys() if x != "ground_in" and x != "ground_out"]:
        if obj in object_locations[locker]:
            return locker
    return None

def get_random_x_and_y_within_locker(door):
    boundary = door.dimensions[1]
    margin = 0.2
    #scale random values with min + (value * (max - min))
    x = random_scaled(boundary - margin, margin)
    y = random_scaled(boundary - margin, margin)
    return x, y

# Choose a random brightness level, print it to console and return it
def choose_brightness(min=2000, max=60000):
    chosen_brightness = choice([x for x in brightness_levels if x >= min and x <= max])
    print("Chosen brightness: " + str(chosen_brightness))
    return chosen_brightness

# Sets a random brightness to a light
def set_random_brightness(light, min=200, max=8200):
    light.energy = choose_brightness()

def random_rotate_camera(camera):
    #20% chance
    if random() <= 0.2:
        print("Camera rotated")
        camera_x_max_boundary = radians(69)
        camera_x_min_boundary = radians(56) 
        camera_y_max_boundary = radians(20)
        camera_y_min_boundary = radians(-11)
        camera_z_max_boundary = radians(120)
        camera_z_min_boundary = radians(100)
        x_rot = random_scaled(camera_x_max_boundary, camera_x_min_boundary)
        y_rot = random_scaled(camera_y_max_boundary, camera_y_min_boundary)
        z_rot = random_scaled(camera_z_max_boundary, camera_z_min_boundary)
        camera.rotation_euler = Vector([x_rot, y_rot, z_rot])

def select_random_coordinates_on_visible_ground():
    x_min = 2.2875
    x_max = 3.3
    y_min = -3.6
    y_max = 5.00
    return random_scaled(x_max, x_min), random_scaled(y_max, y_min)

def random_select_rotate_arm():
    #select main arm and store its position
    arm = objects["robots"]["arm"]
    starting_position = Vector(arm.location)
    
    #select a random arm and swap the two arm locations
    random_arm = select_random_object(choices=["robots"])
    arm.location = random_arm.location
    random_arm.location = starting_position

    #randomly choose a small arm rotation
    random_arm.rotation_euler[0] = radians(random_scaled(110, 70))
    random_arm.rotation_euler[1] = radians(random_scaled(40, 20))
    random_arm.rotation_euler[2] = radians(random_scaled(-35, -40))

    return random_arm

def get_random_location_on_locker():
    max_x = physical_locker.location[0] + physical_locker.dimensions[0] / 2 - 1
    min_x = physical_locker.location[0] - physical_locker.dimensions[0] / 2 + 1
    max_y = physical_locker.location[1] + physical_locker.dimensions[1] / 2 - 0.5
    min_y = physical_locker.location[1] - physical_locker.dimensions[1] / 2 + 0.5
    return random_scaled(max_x, min_x), random_scaled(max_y, min_y)

def get_handle_location_for_door(door, locker_num):
    # We need to copy the location in a new vector or the following changes would be made on the door location
    door_location = Vector(door.location)
    if not door_open[int(locker_num)]:
        door_location[1] += door.dimensions[1]
    else:
        door_location[0] += door.dimensions[1]
    return door_location