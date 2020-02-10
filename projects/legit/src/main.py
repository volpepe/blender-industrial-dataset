import bpy
from random import randint, choice, random
from mathutils import Vector
import os
from datetime import datetime
import sys

render_config = {
    "fps": 12
}

#objects present in the scene
objects = {
    'cubes' : {
        'cube_0' : bpy.data.objects["Cube"],
        'cube_1' : bpy.data.objects["Cube.001"],
        'cube_2' : bpy.data.objects["Cube.002"],
        'cube_3' : bpy.data.objects["Cube.003"],
        'cube_4' : bpy.data.objects["Cube.004"],
        'cube_5' : bpy.data.objects["Cube.005"],
        'cube_6' : bpy.data.objects["Cube.006"],
        'cube_7' : bpy.data.objects["Cube.007"],
    }, 
    'spheres' : {
        'sphere_0' : bpy.data.objects["Sphere"],
        'sphere_1' : bpy.data.objects["Sphere.001"],
        'sphere_2' : bpy.data.objects["Sphere.002"],
        'sphere_3' : bpy.data.objects["Sphere.003"],
        'sphere_4' : bpy.data.objects["Sphere.004"],
    },
    'cones' : {
        'cone_0' : bpy.data.objects["Cone"],
        'cone_1' : bpy.data.objects["Cone.001"],
    },
    'cylinder' : {
        'cylinder_0' : bpy.data.objects["Cylinder"],
        'cylinder_1' : bpy.data.objects["Cylinder.001"],
    },
    'lights' : {
        'light_0' : bpy.data.lights["Light"],
    },
    'cameras' : {
        'camera_0' : bpy.data.cameras["Camera"],
    },
    'robots' : {
        'arm_0' : bpy.data.objects["arm"],
    }
}

object_locations = {
    'ground' : [
        bpy.data.objects["Cube.002"],
        bpy.data.objects["Cube.004"],
        bpy.data.objects["Cube.007"],
        bpy.data.objects["Cone.001"],
        bpy.data.objects["Cylinder.001"],
    ],
    'loc_0': [
        bpy.data.objects["Sphere"],
    ],
    'loc_1': [],
    'loc_2': [
        bpy.data.objects["Sphere.001"],
    ],
    'loc_3': [
        bpy.data.objects["Cube"],
    ],
    'loc_4': [
        bpy.data.objects["Cylinder"],
        bpy.data.objects["Cube.001"],
        bpy.data.objects["Sphere.002"],
    ],
    'loc_5': [
        bpy.data.objects["Sphere.004"],
    ],
    'loc_6': [],
    'loc_7': [],
    'loc_8': [
        bpy.data.objects["Sphere.003"],
    ],
    'loc_9': [
        bpy.data.objects["Cone"],
    ],
    'loc_10': [],
    'loc_11': [
        bpy.data.objects["Cube.006"],
    ],
    'loc_12': [
        bpy.data.objects["Cube.003"],
        bpy.data.objects["Cube.005"],
    ],
    'loc_13': [],
}

#doors of the locker: they can be opened by rotating their z axis at -90°
#and closed by restoring that to 0°
doors = {
    'door_0' : bpy.data.objects["Door_0"],
    'door_1' : bpy.data.objects["Door_1"],
    'door_2' : bpy.data.objects["Door_2"],
    'door_3' : bpy.data.objects["Door_3"],
    'door_4' : bpy.data.objects["Door_4"],
    'door_5' : bpy.data.objects["Door_5"],
    'door_6' : bpy.data.objects["Door_6"],
    'door_7' : bpy.data.objects["Door_7"],
    'door_8' : bpy.data.objects["Door_8"],
    'door_9' : bpy.data.objects["Door_9"],
    'door_10' : bpy.data.objects["Door_10"],
    'door_11' : bpy.data.objects["Door_11"],
    'door_12' : bpy.data.objects["Door_12"],
    'door_13' : bpy.data.objects["Door_13"],
}

#False = closed, True = open
door_open = [False] * len(doors.keys())

brightness_levels = [x for x in range(2000, 60000, 1000)]


###################################################################

#random choices

#choose a random luminosity and print it to console
def choose_luminosity(min=2000, max=60000):
    chosen_luminosity = choice([x for x in brightness_levels if x >= min and x <= max])
    print("Chosen luminosity: " + str(chosen_luminosity))
    return chosen_luminosity

#choose a random activity from the ones in the activity dictionary
def choose_activity():
    random_activity = choice(list(activities.keys()))
    print("Chosen activity: " + random_activity)
    return random_activity

#selects a random object from a list of choices passed as an argument
#a location can be selected as well
#example: ["cubes", "spheres"] --> select a random cube or sphere
#["cubes"] --> selects a random cube
def select_random_object(choices=["cubes", "spheres"], location=None):
    list_obj = []
    for c in choices:
        list_obj.extend(objects[c].values())
    if location is not None:
        list_obj = [x for x in list_obj if x in object_locations[location]]
    return choice(list_obj)

###################################################################

#rendering utilities

#changes current frame
def set_current_frame(frame_num):
    bpy.context.scene.frame_set(frame_num)

#adds a keyframe at the current frame for a list of objects
def set_keyframe_for_objects(scene_objects, data_path="location"):
    for scene_object in scene_objects:
        scene_object.keyframe_insert(data_path=data_path, index=-1)

#last function to call: renders the scene with the set keyframes and settings
def render_and_end():
    bpy.ops.render.render(animation=True)

###################################################################

#environment utilities

#gets all object except the ones defined in the exception list
def get_all_objects(exceptions=[]):
    return [obj for key in objects.keys() for obj in objects[key].values() if key not in exceptions]

#sets a random luminosity to a light
def set_random_luminosity(light, min=200, max=8200):
    light.energy = choose_luminosity()

def enable_collisions(objs):
    for obj in objs:
        obj.rigid_body.enabled = True
        obj.rigid_body.kinematic = False

#returns a string that indicates where the object is
def get_locker_num_for_object(obj):
    for locker in object_locations.keys():
        if obj in object_locations[locker]:
            return locker
    return None

#gets the location of the locker's handle
def get_handle_location_for_object(obj):
    locker = get_locker_num_for_object(obj)
    if locker is not None and locker != 'ground':
        locker_num = locker.split('_')[1]
        door = doors['door_' + locker_num]
        door_location = door.location
        if not door_open[int(locker_num)]:
            door_location[1] += door.dimensions[1]
        else:
            door_location[0] += door.dimensions[1]
        return door_location
    else:
        return None

###################################################################

def move_sphere_to_empty():
    #select a random sphere
    sphere = select_random_object(choices=["spheres"])
    print("Selected " + str(sphere))

    #enable all collisions
    enable_collisions(get_all_objects(exceptions=["lights", "cameras"]))

    #get reference to the arm
    arm = objects["robots"]["arm_0"]
    starting_location = [x for x in arm.location]

    #let the arm be controlled by the animation
    arm.rigid_body.kinematic = True
    #temporarily disable rigid_body physics for the sphere
    sphere.rigid_body.kinematic = True

    #set the first keyframe for the arm and the sphere
    current_frame = 0
    set_current_frame(current_frame)
    set_keyframe_for_objects([arm, sphere])

    #approach its locker (1 sec)

    #get the locker location
    handle_0 = get_handle_location_for_object(sphere)
    if handle_0 is None:
        return None #nothing happens

    #move arm to locker
    current_frame += render_config["fps"]
    set_current_frame(current_frame)
    arm.location = handle_0
    set_keyframe_for_objects([arm])
    
    #open the locker (2 secs)
    current_frame += render_config["fps"]
    set_current_frame(current_frame)

    #select a random locker
    #approach the second locker (1 sec)
    #open the second locker (1 sec)
    #get back to first locker (2 secs)
    #get item (1 sec)
    #get out with item (1 sec)
    #take the item to second locker (2 secs)
    #put it in(1 sec)
    #get out (1 sec)
    #move to second locker and close it (3 sec)

###################################################################

activities = {
    'move_sphere_to_empty' : move_sphere_to_empty,
}

#get the path for saving the files
argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"
out_path = argv[0]

#set a random luminosity for the scene
set_random_luminosity(objects["lights"]["light_0"])

#choose an activity and execute it
random_activity = choose_activity()
activities[random_activity]()

#set filepath
bpy.context.scene.render.filepath = (os.path.join(out_path, random_activity, datetime.now().strftime("%d%m%Y_%H%M%S"), "frame"))

#bake physics
for obj in get_all_objects(exceptions=["lights", "cameras"]):
    obj.select_set(True)
    bpy.ops.ptcache.bake_all(bake=True)

#end activity
render_and_end()