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
k = int(len(videos) * 70 / 100)
print("{} videos are for training and {} for validation".format(k, len(videos) - k))

train = random.sample(videos, k)
val = [vid for vid in videos if vid not in train]

print("Train set:\n")

with open(os.path.sep.join(os.getcwd().split(os.path.sep)[:-1]) + os.path.sep + 'custom_train_rawframes.txt', 'w') as trainList:
    for vid in train:
        print(vid)
        trainList.write("{} {} {}\n".format(os.path.join(vid.split(os.path.sep)[-2], 
            vid.split(os.path.sep)[-1]),
            len(os.listdir(vid)) - 1,
            classes[vid.split(os.path.sep)[-2]]))

print("Val set:\n")

with open(os.path.sep.join(os.getcwd().split(os.path.sep)[:-1]) + os.path.sep + 'custom_val_rawframes.txt', 'w') as valList:
    for vid in val:
        print(vid)
        valList.write("{} {} {}\n".format(os.path.join(vid.split(os.path.sep)[-2], 
            vid.split(os.path.sep)[-1]),
            len(os.listdir(vid)) - 1,
            classes[vid.split(os.path.sep)[-2]]))

print("Generated filelists at {} and {}!".format(
        os.path.sep.join(os.getcwd().split(os.path.sep)[:-1]) + os.path.sep + 'custom_val_rawframes.txt',
        os.path.sep.join(os.getcwd().split(os.path.sep)[:-1]) + os.path.sep + 'custom_train_rawframes.txt'))

os.chdir(current_dir)