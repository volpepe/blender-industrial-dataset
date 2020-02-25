import os
import sys
import argparse
import glob
import random

parser = argparse.ArgumentParser(
    description = 'Create train and test lists for custom dataset',
)
parser.add_argument('--folder', '--f', type=str, default='../../data/custom/rawframes')
args = parser.parse_args(sys.argv[1:])

#open classInd.txt to take classes
classes = {}
with open('classInd.txt', 'r') as classInd:
    for cnt, line in enumerate(classInd):
        classes[line.split()[1]] = line.split()[0]

current_dir = os.getcwd()
os.chdir(args.folder)

#get 70% of videos for train and 30% for val
videos = glob.glob('*/*')
print("Found: " + str(len(videos)) + " videos")

video_list = {}
for activity in classes.keys():
    video_list[activity] = {'train': [], 'val': []}
    activity_videos = [vid for vid in videos if vid.startswith(activity)]
    k = int(len(activity_videos) * 70 / 100)
    video_list[activity]['train'] = random.sample(activity_videos, k)
    video_list[activity]['val'] = [vid for vid in activity_videos if vid not in video_list[activity]['train']]
    print("Sampled {} videos for training and {} for validation in activity {}".format(len(video_list[activity]['train']), 
        len(video_list[activity]['val']), activity))

train_path = os.path.sep.join(os.getcwd().split(os.path.sep)[:-1]) + os.path.sep + 'custom_train_rawframes.txt'
val_path = os.path.sep.join(os.getcwd().split(os.path.sep)[:-1]) + os.path.sep + 'custom_val_rawframes.txt'

with open(train_path, 'w') as trainList:
    for activity in classes.keys():
        for vid in video_list[activity]['train']:
            trainList.write("{} {} {}\n".format(vid,
                        len(os.listdir(vid)) - 1,
                        classes[activity]))

with open(val_path, 'w') as valList:
    for activity in classes.keys():
        for vid in video_list[activity]['val']:
            valList.write("{} {} {}\n".format(vid,
                        len(os.listdir(vid)) - 1,
                        classes[activity]))

print("Generated filelists at {} and {}!".format(train_path, val_path))

os.chdir(current_dir)