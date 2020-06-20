import argparse
import sys
import subprocess
import os

"""
This script creates a certain number of videos using the chosen scene as setting
and the defined activities as classes. The obtained dataset is assured to be
balanced, as in the number of videos per class will be the same for each class.
Requires a valid Blender scene to be used as setting and a valid script to be
executed on it, as well as a class list for the classes that need to be generated.

NOTE: This script is thought for rendering on Windows, as it uses a Powershell command.
"""

def parse_args():
    parser = argparse.ArgumentParser(description = 
        """Create a certain number of videos using the chosen scene 
        and defined activity in order to build a custom dataset""")

    parser.add_argument('--blender_dir', '-bd', type=str, 
        default='C:\\Program Files\\Blender Foundation\\Blender 2.82\\')
    parser.add_argument('--output_dir', '-od', type=str, required=True)
    parser.add_argument('--blender_file', '-bf', type=str, required=True)
    parser.add_argument('--script_file', '-sf', type=str, required=True)
    parser.add_argument('--video_num', '-n', type=int, required=True)
    parser.add_argument('--class_file', '-cf', type=str, default='.\classInd.txt')

    args = parser.parse_args(sys.argv[1:])
    return args

def read_classes(class_file):
    # Open classInd.txt to take classes
    classes = {}
    with open(class_file, 'r') as classInd:
        for cnt, line in enumerate(classInd):
            classes[line.split()[1]] = line.split()[0]
    return classes

def render_videos(video_num, blender_file, script_file, output_dir, blender_dir, classes):
    current_dir = os.getcwd()
    os.chdir(blender_dir)
    activity_num = int(int(video_num) / len(classes))
    print("""\n\nThis process will render {} videos per class. That's {} less videos than you requested: sorry!...\n\n""".format(
            str(activity_num), 
            str(video_num - activity_num * len(classes)))
    )
    for activity in classes.keys():
        command = '''Measure-Command -Expression {{ 1..{} | % {{ .\\blender.exe -b {} -P {} -- {} --activity {} }}}}'''.format(
                            str(activity_num),
                            blender_file,
                            script_file,
                            output_dir,
                            activity
        )
        print(command)
        p = subprocess.Popen(["powershell.exe", command], stdout=sys.stdout)
        p.communicate()
    os.chdir(current_dir)

def main():
    args = parse_args()
    classes = read_classes(args.class_file)
    if args.video_num < len(classes):
        print("You MUST render at least ONE video PER CLASS")
        sys.exit()
    render_videos(args.video_num, args.blender_file, 
                    args.script_file, args.output_dir, args.blender_dir,
                    classes)

if __name__ == "__main__":
    main()