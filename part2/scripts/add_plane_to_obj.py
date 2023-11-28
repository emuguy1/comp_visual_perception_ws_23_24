import bpy
import os

source_directory = "D:/programmierte_programme/githubworkspace/comp_visual_perception_ws_23_24/part2/files/object_mesh/"
destination_directory = "D:/programmierte_programme/githubworkspace/comp_visual_perception_ws_23_24/part2/files/object_mesh/"


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


        # 1. Import the object

        try:
            bpy.ops.import_scene.obj(filepath=object_path)
        except Exception as e:
            print(f"Error importing {filename}. Reason: {e}. Skipping to the next file.")
            continue

        # Check if there are selected objects after import
        if bpy.context.selected_objects:

            obj = bpy.context.selected_objects[0]
            # Add Subdivision Surface modifier
            # subsurf_modifier = obj.modifiers.new(name="Subdivision", type='SUBSURF')
            # subsurf_modifier.levels = 1  # Set the subdivision levels as needed
            # subsurf_modifier.render_levels = 0  # Set render subdivision levels if different from viewport
            bpy.context.view_layer.objects.active = obj

            # 2. Create base plate
            bpy.ops.mesh.primitive_plane_add(size=3, enter_editmode=False, align='WORLD', location=(0, 0, 0))
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.subdivide(number_cuts=100, smoothness=0)
            bpy.ops.object.editmode_toggle()
            base_plane = bpy.context.object
            base_plane.name = "Floor"

            # 3. Export the obj and floor object as an .obj file to the specified directory
            bpy.ops.object.select_all(action='DESELECT')
            base_plane.select_set(True)
            obj.select_set(True)
            #bpy.ops.transform.resize(value=(0.25, 0.25, 0.25))

            bpy.ops.export_scene.obj(filepath=export_path, use_selection=True)
            mtl_file_path = os.path.join(destination_directory, os.path.splitext(filename)[0] + ".mtl")
            if os.path.exists(mtl_file_path):
                os.remove(mtl_file_path)

            print("Cloth #", ++i)

        else:
            print(f"No object imported from {filename}.")

clear_mesh_objects()  # Clear mesh objects after the loop completes

