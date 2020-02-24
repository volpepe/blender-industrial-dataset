import os
import sys
import argparse
import glob
import random
import csv

parser = argparse.ArgumentParser(
    description = 'Create train and test lists for custom dataset',
)
parser.add_argument('--folder', '-f', type=str, default='../../data/custom/rawframes')
args = parser.parse_args(sys.argv[1:])

#get 70% of videos for train and 30% for val
videos = glob.glob(args.folder + '/*/*')
print("Found: " + str(len(videos)) + " videos")
k = int(len(videos) * 70 / 100)
print("{} videos are for training and {} for validation".format(k, len(videos) - k))

train = random.sample(videos, k)
val = [vid for vid in videos if vid not in train]

#open classInd.txt to take classes
classes = {}
with open('classInd.txt', 'r') as classInd:
    for cnt, line in enumerate(classInd):
        classes[line.split()[1]] = line.split()[0]

with open(os.path.sep.join(args.folder.split(os.path.sep)[:-1]) + os.path.sep + 'custom_train_rawframes.txt', 'w') as trainList:
    for vid in train:
        trainList.write("{} {} {}\n".format(os.path.join(vid.split(os.path.sep)[-2], 
            vid.split(os.path.sep)[-1]),
            len(os.listdir(vid)),
            classes[vid.split(os.path.sep)[-2]]))

with open(os.path.sep.join(args.folder.split(os.path.sep)[:-1]) + os.path.sep + 'custom_val_rawframes.txt', 'w') as valList:
    for vid in val:
        valList.write("{} {} {}\n".format(os.path.join(vid.split(os.path.sep)[-2], 
            vid.split(os.path.sep)[-1]),
            len(os.listdir(vid)),
            classes[vid.split(os.path.sep)[-2]]))

print("Generated filelists at {} and {}!".format(
        os.path.sep.join(args.folder.split(os.path.sep)[:-1]) + os.path.sep + 'custom_val_rawframes.txt',
        os.path.sep.join(args.folder.split(os.path.sep)[:-1]) + os.path.sep + 'custom_train_rawframes.txt'))