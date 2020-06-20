import bpy 
from datetime import datetime
import os
import time

from env_params.refs import get_all_objects

render_config = {
    "fps": 12
    # More confings might be added
}

def render_scene(out_path, random_activity):
    #set filepath
    timestamp = ''
    activity_folder = folder = os.path.join(out_path, random_activity)
    if not os.path.exists(activity_folder):
        os.mkdir(activity_folder)
    while True:
        timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
        folder = os.path.join(activity_folder, timestamp)
        #if folder doesn't exist, create it and start rendering, else retry in a second to avoid problems
        if not os.path.exists(folder):
            os.mkdir(folder)
            break
        else:
            time.sleep(1)
    bpy.context.scene.render.filepath = os.path.join(folder, 'img_0')

    #bake physics (calculate physics for all objects except the ones we moved directly)
    for obj in get_all_objects(exceptions=["lights", "cameras"]):
        obj.select_set(True)
        bpy.ops.ptcache.bake_all(bake=True)

    #render activity with the set keyframes and setting
    bpy.ops.render.render(animation=True)

    #returns folder where the video was saved in case additional files need to be added 
    return folder