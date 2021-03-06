import csv
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--csv_path", type=str, required=True, help="Path to CSV file")
args = ap.parse_args()

object_table = [
    ["id", "type", "color", "size"],
    ["cone_0", "cone", "orange", "small"],
    ["cone_1", "cone", "blue", "small"],
    ["cone_2", "cone", "orange", "medium"],
    ["cube_0", "cube", "blue", "small"],
    ["cube_1", "cube", "green", "medium"],
    ["cube_2", "cube", "very_small", "pink"],
    ["cube_3", "cube", "very_small", "orange"],
    ["cube_4", "cube", "big", "light_blue"],
    ["cube_5", "cube", "very_small", "purple"],
    ["cube_6", "cube", "small", "green"],
    ["cube_7", "cube", "big", "green"],
    ["cube_8", "cube", "medium", "pink"],
    ["cube_8", "cube", "medium", "pink"],
    ["cylinder_0", "cylinder", "medium", "pink"],
    ["cylinder_1", "cylinder", "big", "dark_grey"],
    ["sphere_0", "sphere", "big", "yellow"],
    ["sphere_1", "sphere", "big", "light_blue"],
    ["sphere_2", "sphere", "very_small", "orange"],
    ["sphere_3", "sphere", "small", "pink"],
    ["sphere_4", "sphere", "very_small", "yellow"],
    ["sphere_5", "sphere", "big", "green"],
    ["arm", "arm", "big", "dark_grey"],
    ["arm_color", "arm", "big", "blue"],
    ["arm_copy", "arm", "big", "dark_grey"],
    ["door_0", "door", "big", "violet"],
    ["door_1", "door", "big", "blue"],
    ["door_2", "door", "big", "beige"],
    ["door_3", "door", "very_big", "violet"],
    ["door_4", "door", "very_big", "green"],
    ["door_5", "door", "big", "brown"],
    ["door_6", "door", "big", "purple"],
    ["door_7", "door", "big", "black"],
    ["door_8", "door", "big", "green"],
    ["door_9", "door", "big", "red"],
    ["door_10", "door", "big", "grey"],
    ["door_11", "door", "big", "violet"],
    ["door_12", "door", "big", "blue"],
    ["door_13", "door", "big", "green"],
]

with open(args["csv_path"], "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerows(object_table)