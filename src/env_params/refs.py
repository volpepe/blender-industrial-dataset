import bpy
from random import choice

"""
This file contains references to all the relevant objects in the scene.
"""

# Dictionary of objects present in the scene that can be manipulated.
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
        'cube_8' : bpy.data.objects["Cube.008"],
    }, 
    'spheres' : {
        'sphere_0' : bpy.data.objects["Sphere"],
        'sphere_1' : bpy.data.objects["Sphere.001"],
        'sphere_2' : bpy.data.objects["Sphere.002"],
        'sphere_3' : bpy.data.objects["Sphere.003"],
        'sphere_4' : bpy.data.objects["Sphere.004"],
        'sphere_5' : bpy.data.objects["Sphere.005"],
    },
    'cones' : {
        'cone_0' : bpy.data.objects["Cone"],
        'cone_1' : bpy.data.objects["Cone.001"],
        'cone_2' : bpy.data.objects["Cone.002"],
    },
    'cylinders' : {
        'cylinder_0' : bpy.data.objects["Cylinder"],
        'cylinder_1' : bpy.data.objects["Cylinder.001"],
    },
    'lights' : {
        'light_0' : bpy.data.lights["Light"],
    },
    'cameras' : {
        'camera_0' : bpy.data.objects["Camera"],
    },
    'robots' : {
        'arm' : bpy.data.objects["arm"],
        'arm_color' : bpy.data.objects["arm.color"],
        'arm_copy' : bpy.data.objects["arm.copy"],
    }
}

# Dictionary of the same set of objects, but ordered by their position in the scene.
# Having such a dictionary in a project might be important in order to express more complicated activities.
object_locations = {
    'ground_in' : [
        bpy.data.objects["Cube.002"],
        bpy.data.objects["Cube.004"],
        bpy.data.objects["Cube.007"],
        bpy.data.objects["Cone.001"],
        bpy.data.objects["Cylinder.001"],
    ],
    'ground_out' : [
        bpy.data.objects["Cone.002"],
        bpy.data.objects["Sphere.005"],
        bpy.data.objects["Cube.008"],
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

# A reference to the locker object
physical_locker = bpy.data.objects["Locker"]

# References to the doors of the locker.
# In our case, doors can be opened by rotating their Z axis to -90°
# and closed by restoring that parameter to 0°
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

# Gets all objects except the ones defined in the exception list
def get_all_objects(exceptions=[]):
    return [obj for key in objects.keys() for obj in objects[key].values() if key not in exceptions]

# Selects a random object from a list of choices passed as an argument.
# A location can be selected as well.
# Example: ["cubes", "spheres"] --> select a random cube or sphere
# ["cubes"] --> selects a random cube
def select_random_object(choices=["cubes", "spheres", "cylinders", "cones"], locations=None):
    list_obj = []
    for c in choices:
        list_obj.extend(objects[c].values())
    if locations is not None:
        list_obj = [x for x in list_obj for loc in locations if x in object_locations[loc]]
    return choice(list_obj)