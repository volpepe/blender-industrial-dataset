import bpy
from random import randint, choice, random
from mathutils import Vector
import os
from datetime import datetime
import sys

# Run this script with blender using:
# .\blender.exe -b path\to\project.blend -P path\to\this\script -- root\folder\for\output

################################################# DATA ##################################################

#dictionary of objects
objects = {
    'cubes' : {
        'cube_0' : bpy.data.objects["Cube"],
        'cube_1' : bpy.data.objects["Cube.001"],
        'cube_2' : bpy.data.objects["Cube.002"],
        'cube_3' : bpy.data.objects["Cube.003"],
        'cube_4' : bpy.data.objects["Cube.004"],
        'cube_5' : bpy.data.objects["Cube.005"],
        'cube_6' : bpy.data.objects["Cube.006"],
    }, 
    'lights' : {
        'light_0' : bpy.data.lights["Light"],
    },
    'spheres' : {
        'sphere_0' : bpy.data.objects["Sphere"],
        'sphere_1' : bpy.data.objects["Sphere.001"],
        'sphere_2' : bpy.data.objects["Sphere.002"],
        'sphere_3' : bpy.data.objects["Sphere.003"],
    },
    'cameras' : {
        'camera_0' : bpy.data.cameras["Camera"],
    },
    'robots' : {
        'arm_0' : bpy.data.objects["arm"],
    }
}

levels = {
    "ground" : [
        bpy.data.objects["Cube"], 
        bpy.data.objects["Cube.001"],
        bpy.data.objects["Cube.002"],
        bpy.data.objects["Cube.004"],
        bpy.data.objects["Sphere.003"],
    ],
    "first" : [
        bpy.data.objects["Cube.005"],
        bpy.data.objects["Cube.006"],
        bpy.data.objects["Sphere"],
        bpy.data.objects["Sphere.002"],
    ],
    "second" : [
        bpy.data.objects["Cube.003"], 
        bpy.data.objects["Sphere.001"],
    ],
}

brightness_levels = [x for x in range(200, 8200, 400)]
 
######################################################## UTILS ################################################################

def get_all_objects(exceptions=[]):
    return [obj for key in objects.keys() for obj in objects[key].values() if key not in exceptions]

def get_shelf_safe_range():
    plane = bpy.data.objects["plane_1"]
    x_l = plane.location[0] + plane.dimensions[0] / 2 - 0.5 #margin
    x_L = plane.location[0] - plane.dimensions[0] / 2 + 0.5
    y_l = plane.location[1] + plane.dimensions[1] / 2 - 0.5
    y_L = plane.location[1] - plane.dimensions[1] / 2 + 0.5
    return ([x_l, x_L], [y_l, y_L])

#changes current frame
def set_current_frame(frame_num):
    bpy.context.scene.frame_set(frame_num)

#adds a keyframe at the current frame for a list of objects
def set_keyframe_for_objects(scene_objects):
    for scene_object in scene_objects:
        scene_object.keyframe_insert(data_path="location", index=-1)

#sets a random luminosity to a light
def set_random_luminosity(light, min=200, max=8200):
    light.energy = choice([x for x in brightness_levels if x >= min and x <= max])

#last function to call
def render_and_end():
    bpy.ops.render.render(animation=True)

#selects a random object from a list of choices passed as an argument
#a level of elevation can be selected as well (ground, first or second)
#example: ["cubes", "spheres"] --> select a random cube or sphere
#["cubes"] --> selects a random cube
def select_random_object(choices=["cubes", "spheres"], level=None):
    list_obj = []
    for c in choices:
        list_obj.extend(objects[c].values())
    if level is not None:
        list_obj = [x for x in list_obj if x in levels[level]]
    return choice(list_obj)

def enable_collisions(objs):
    for obj in objs:
        obj.rigid_body.enabled = True
        obj.rigid_body.kinematic = False

############################################ ACTIVITIES ##########################################################

def lift_from_ground_activity():

    #take a random object from the ground
    lifted = select_random_object(level="ground")
    print("Selected item for lifting: " + str(lifted))

    enable_collisions(get_all_objects(exceptions=["lights", "cameras"]))

    #get reference to the arm
    arm = objects["robots"]["arm_0"]
    starting_location = [x for x in arm.location]

    #let the arm be controlled by the animation
    arm.rigid_body.kinematic = True
    #let the object to be lifted to be controlled by the animation
    lifted.rigid_body.kinematic = True

    #arm moves near the object (about 3 seconds, 36 frames)
    current_frame = 0
    set_current_frame(current_frame)
    set_keyframe_for_objects([arm, lifted])

    for i in range(0, 3):
        current_frame += 12 # 1 second
        set_current_frame(current_frame)
        arm.location[i] = lifted.location[i]

        #z-axis correction code so that arm falls on top of lifted object instead of merging through it
        if i == 2:
            arm.location[i] += lifted.dimensions[i] / 2
        
        set_keyframe_for_objects([arm])

    #arm has finally moved to location.
    #object and arm move together on the shelf above (3 seconds, 36 frames)
    #shelves are located at z = 0.9 and z = 1.8

    set_keyframe_for_objects([lifted])

    #rise animation
    current_frame += 12
    set_current_frame(current_frame)
    arm.location[2] += 0.9
    lifted.location[2] += 0.9
    set_keyframe_for_objects([arm, lifted])

    #x and y should be set randomly within the boundaries of the shelf
    for i in range(0, 2):
        current_frame += 12 # 1 second
        set_current_frame(current_frame)
        shelf_range = get_shelf_safe_range()
        #scale random values with min + (value * (max - min))
        new_axis_position = shelf_range[i][0] + random()*(shelf_range[i][1] - shelf_range[i][0])
        arm.location[i] = new_axis_position
        lifted.location[i] = new_axis_position
        set_keyframe_for_objects([arm, lifted])

    #drop the object (lift arm for 0.2 m in 1 sec, 12 frames)
    current_frame += 12
    set_current_frame(current_frame)
    arm.location[2] += 0.1
    set_keyframe_for_objects([arm])
    
    #bring the arm back to original position (3 seconds, 36 frames)
    for i in range(0, 3):
        current_frame += 12 # 1 second
        set_current_frame(current_frame)
        arm.location[i] = starting_location[i]
        set_keyframe_for_objects([arm])

def drop_from_highest_shelf_activity():

    #take a random object from the highest shelf
    lifted = select_random_object(level="second")
    print("Selected item for lifting: " + str(lifted))

    enable_collisions(get_all_objects(exceptions=["lights", "cameras"]))

    #get reference to the arm
    arm = objects["robots"]["arm_0"]
    starting_location = [x for x in arm.location]

    #let the arm be controlled by the animation
    arm.rigid_body.kinematic = True

    #arm moves near the object (about 3 seconds, 36 frames)
    current_frame = 0
    set_current_frame(current_frame)
    set_keyframe_for_objects([arm, lifted])

    #temporarily disable rigid_body physics for the lifted object
    lifted.rigid_body.enabled = False
    lifted.rigid_body.kinematic = True
    lifted.keyframe_insert(data_path='rigid_body.enabled', frame=current_frame)
    lifted.keyframe_insert(data_path='rigid_body.kinematic', frame=current_frame)

    #start with z axis
    current_frame += 12
    set_current_frame(current_frame)
    arm.location[2] = lifted.location[2] + lifted.dimensions[2] / 2  #z-axis correction code so that arm falls on top of lifted object instead of merging through it
    set_keyframe_for_objects([arm])

    #move in the other axis
    for i in range(0, 2):
        current_frame += 12 # 1 second
        set_current_frame(current_frame)
        arm.location[i] = lifted.location[i]
        set_keyframe_for_objects([arm])

    #arm has finally moved to location and "grabbed" the object
    #object and arm move together to a random location out of the shelf
    set_keyframe_for_objects([lifted])

    #rise slightly
    current_frame += 12
    set_current_frame(current_frame)
    arm.location[2] += 0.2
    lifted.location[2] += 0.2
    set_keyframe_for_objects([arm, lifted])

    #move in x and y: movement should be a random number between .8 and 2 meters in both axis
    #it should be enough to move it away from the table
    for i in range(0, 2):
        current_frame += 12 # 1 second
        set_current_frame(current_frame)
        #scale random values with min + (value * (max - min))
        new_axis_position = 0.8 * random()*(2 - 0.8)
        arm.location[i] = new_axis_position
        lifted.location[i] = new_axis_position
        set_keyframe_for_objects([arm, lifted])
    
    #drop the lifted object by letting the physics engine take over
    lifted.rigid_body.enabled = True
    lifted.rigid_body.kinematic = False
    lifted.keyframe_insert(data_path='rigid_body.enabled', frame=current_frame)
    lifted.keyframe_insert(data_path='rigid_body.kinematic', frame=current_frame)

    #the arm waits and then moves back to its original position
    current_frame += 12
    set_current_frame(current_frame)
    set_keyframe_for_objects([arm])

    #bring the arm back to original position (3 seconds, 36 frames)
    for i in range(0, 3):
        current_frame += 12 # 1 second
        set_current_frame(current_frame)
        arm.location[i] = starting_location[i]
        set_keyframe_for_objects([arm])


######################################################################################################

activities = {
    'lift_ground' : lift_from_ground_activity,
    'drop_from_high' : drop_from_highest_shelf_activity,
}

argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"
out_path = argv[0]

#choose a random activity
random_activity = choice(list(activities.keys()))
print("Chosen activity: " + random_activity)
activities[random_activity]()

#set random luminosity
set_random_luminosity(objects["lights"]["light_0"])

#set filepath
bpy.context.scene.render.filepath = (os.path.join(out_path, random_activity, datetime.now().strftime("%d%m%Y_%H%M%S"), "frame"))

#bake physics
for obj in get_all_objects(exceptions=["lights", "cameras"]):
    obj.select_set(True)
    bpy.ops.ptcache.bake_all(bake=True)

#end activity
render_and_end()