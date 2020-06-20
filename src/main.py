import sys
import argparse
import os
import bpy

"""Extending path so that all modules can be imported into Blender's environment"""
dir = os.path.join(os.path.dirname(bpy.data.filepath), "src")
if not dir in sys.path:
    sys.path.append(dir)

from functions.env_utilities import set_random_brightness, random_rotate_camera
from env_params.activities import activities, choose_activity
from env_params.refs import objects
from renderer import render_scene
from env_params.actions_phrases import write_csv

###################################################################

def parse_args(argv):
    # Get the path for saving the files
    out_path = argv[0]

    # Get additional optional arguments
    parser = argparse.ArgumentParser(
        description = 'Run blender in background mode',
        prog = "blender -b dataset_stem.blend -P "+__file__+" -- out_path",
    )
    parser.add_argument('--activity', '-a', type=str)
    args = parser.parse_args(argv[1:])
    return args, out_path

def main():
    # This script is executed on Blender's own environment. 
    # This means that all the specified command line arguments are meant to be
    # passed to Blender. Blender stops capturing arguments after the "--" notation.
    # The next few lines of code are meant to capture those arguments, 
    # as they are meant for this script.
    argv = sys.argv[sys.argv.index("--") + 1:]
    args, out_path = parse_args(argv)

    # If the scene is more complex than the one in the example (e.g. multiple cameras
    # and sources of light), this is a good place to write some code to manage all these
    # additional elements (e.g. choosing a camera).

    # Set a random brightness for the scene
    set_random_brightness(objects["lights"]["light_0"])

    # Set a random camera rotation (within boundaries) on a 20% chance
    random_rotate_camera(objects["cameras"]["camera_0"])

    # Choose an activity and execute it
    if args.activity:
        try:
            random_activity = args.activity
            print("Chosen " + str(args.activity) + " activity")
        except:
            print(str(args.activity) + " is not a correct activity")
    else:
        random_activity = choose_activity()
    moves = activities[random_activity]()

    render_folder = render_scene(out_path, random_activity)

    # Add actions CSV to the folder
    write_csv(moves, render_folder)

if __name__ == "__main__":
    main()