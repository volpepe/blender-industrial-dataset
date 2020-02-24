import argparse
import sys
import subprocess
import os

parser = argparse.ArgumentParser(
    description = 'Create a certain number of videos for custom dataset',
)

parser.add_argument('--blender_dir', '-bd', type=str, default='C:\\Program Files\\Blender Foundation\\Blender 2.82\\')
parser.add_argument('--output_dir', '-od', type=str, required=True)
parser.add_argument('--blender_file', '-bf', type=str, required=True)
parser.add_argument('--script_file', '-sf', type=str, required=True)
parser.add_argument('--video_num', '-n', type=int, required=True)
parser.add_argument('--class_file', '-cf', type=str, default='.\classInd.txt')
args = parser.parse_args(sys.argv[1:])

#open classInd.txt to take classes
classes = {}
with open(args.class_file, 'r') as classInd:
    for cnt, line in enumerate(classInd):
        classes[line.split()[1]] = line.split()[0]

if args.video_num < len(classes):
    print("You MUST render at least ONE video PER CLASS")
    sys.exit()

current_dir = os.getcwd()
os.chdir(args.blender_dir)

activity_num = int(int(args.video_num) / len(classes))

print("\n\nThis process will render {} videos per class. That's {} less videos than you requested: sorry!...\n\n".format(
    str(activity_num), 
    str(args.video_num - activity_num * len(classes)))
)

for activity in classes.keys():
    command = 'Measure-Command -Expression {{ 1..{} | % {{ .\\blender.exe -b {} -P {} -- {} --activity {} }}}}'.format(
                    str(activity_num),
                    args.blender_file,
                    args.script_file,
                    args.output_dir,
                    activity)
    print(command)
    p = subprocess.Popen(["powershell.exe", command], stdout=sys.stdout)
    p.communicate()

os.chdir(current_dir)

