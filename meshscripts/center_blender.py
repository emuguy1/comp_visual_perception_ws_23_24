import bpy
import mathutils
import os

source_directory = "D:/programmierte_programme/githubworkspace/comp_visual_perception_ws_23_24/files/Scaled_Objects/"
destination_directory = "D:/programmierte_programme/githubworkspace/comp_visual_perception_ws_23_24/files/centered_scaled_Objects/"


# Function to clear mesh objects
def clear_mesh_objects():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()


# Iterate over all files in the source directory
for filename in os.listdir(source_directory):
    i = 0
    if filename.endswith(".obj"):
        clear_mesh_objects()  # Clear mesh objects for each iteration

        object_path = os.path.join(source_directory, filename)

        export_path = os.path.join(destination_directory, filename)
        if os.path.exists(export_path):
            print(f"Skipping {filename} as it already exists in the target directory.")
            continue

        # 1. Import the object

        try:
            bpy.ops.import_scene.obj(filepath=object_path)
        except Exception as e:
            print(f"Error importing {filename}. Reason: {e}. Skipping to the next file.")
            continue

        # Check if there are selected objects after import
        if bpy.context.selected_objects:
            obj = bpy.context.selected_objects[0]
            bpy.context.view_layer.objects.active = obj
            objectsa = bpy.context.object
            objectsa.name = "Cloth"

            # Get reference to the object
            obj = bpy.data.objects["Cloth"]

            bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')

            # Get the object's bounding box
            bbox = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
            min_z = min(bbox, key=lambda v: v[2])[2]

            # Calculate translation vectors
            center_to_origin = -obj.location
            lowest_to_zero = mathutils.Vector((0, 0, -min_z))

            # Apply translations
            obj.location += center_to_origin
            obj.location += lowest_to_zero



            # 5. Export the cloth object as an .obj file to the specified directory
            cloth = bpy.data.objects["Cloth"]  # This assumes the name of the cloth object is 'Cloth'
            export_path = os.path.join(destination_directory, filename)
            bpy.ops.object.select_all(action='DESELECT')
            cloth.select_set(True)

            bpy.ops.export_scene.obj(filepath=export_path, use_selection=True)
            mtl_file_path = os.path.join(destination_directory, os.path.splitext(filename)[0] + ".mtl")
            if os.path.exists(mtl_file_path):
                os.remove(mtl_file_path)
            print("Cloth #", ++i)

        else:
            print(f"No object imported from {filename}.")

clear_mesh_objects()  # Clear mesh objects after the loop completes


