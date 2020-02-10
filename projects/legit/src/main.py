import bpy
from random import randint, choice, random
from mathutils import Vector
import os
from datetime import datetime
import sys

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
    'ground' : {
        'cube_2' : bpy.data.objects["Cube.002"],
        'cube_4' : bpy.data.objects["Cube.004"],
        'cube_7' : bpy.data.objects["Cube.007"],
        'cone_1' : bpy.data.objects["Cone.001"],
        'cylinder_1' : bpy.data.objects["Cylinder.001"],
    },
    'loc_0': {
        bpy.data.objects["Sphere"],
    },
    'loc_1': {},
    'loc_2': {
        bpy.data.objects["Sphere.001"],
    },
    'loc_3': {
        bpy.data.objects["Cube"],
    },
    'loc_4': {
        bpy.data.objects["Cylinder"],
        bpy.data.objects["Cube.001"],
        bpy.data.objects["Sphere.002"],
    },
    'loc_5': {
        bpy.data.objects["Sphere.004"],
    },
    'loc_6': {},
    'loc_7': {},
    'loc_8': {
        bpy.data.objects["Sphere.003"],
    },
    'loc_9': {
        bpy.data.objects["Cone"],
    },
    'loc_10': {},
    'loc_11': {
        bpy.data.objects["Cube.006"],
    },
    'loc_12': {
        bpy.data.objects["Cube.003"],
        bpy.data.objects["Cube.005"],
    },
    'loc_13': {},
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

brightness_levels = [x for x in range(2000, 60000, 1000)]


###################################################################

#random choices

def choose_luminosity(min=2000, max=60000):
    chosen_luminosity = choice([x for x in brightness_levels if x >= min and x <= max])
    print("Chosen luminosity: " + str(chosen_luminosity))
    return chosen_luminosity

def choose_activity():
    random_activity = choice(list(activities.keys()))
    print("Chosen activity: " + random_activity)
    return random_activity

###################################################################

#sets a random luminosity to a light
def set_random_luminosity(light, min=200, max=8200):
    light.energy = choose_luminosity()

#last function to call: renders the scene with the set keyframes and settings
def render_and_end():
    bpy.ops.render.render(animation=True)

def get_all_objects(exceptions=[]):
    return [obj for key in objects.keys() for obj in objects[key].values() if key not in exceptions]


###################################################################

def test():
    print("test!")
    print("loaded objects: " + str(objects))
    print("loaded locations: " + str(object_locations))
    print("loaded doors: " + str(doors))

def test_2():
    print("test 2: I dunno man")

###################################################################

activities = {
    'test_1' : test,
    'test_2' : test_2,
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