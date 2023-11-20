import bpy
import os


source_directory = "D:/programmierte_programme/githubworkspace/comp_visual_perception_ws_23_24/files/Submission/Cloths/"
destination_directory = "D:/programmierte_programme/githubworkspace/comp_visual_perception_ws_23_24/files/Submission/Objects/"
number_file = "D:/number.txt"

number = 0

with open(number_file, 'r') as file:
    number = int(file.read())

with open(number_file, 'w') as file:
    file.write(str((number+1)))

filename = str(number)+".obj"

object_path = os.path.join(source_directory, filename)
export_path = os.path.join(destination_directory, filename)

bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

bpy.ops.import_scene.obj(filepath=object_path)
bpy.ops.import_scene.obj(filepath=export_path)
