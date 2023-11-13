import bpy
import os
import trimesh

source_directory = "D:/programmierte_programme/githubworkspace/comp_visual_perception_ws_23_24/files/Scaled_Objects/"
destination_directory = "D:/programmierte_programme/githubworkspace/comp_visual_perception_ws_23_24/files/sCloths/"


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

            # 2. Set the object as a collision object
            bpy.ops.object.modifier_add(type='COLLISION')
            obj.collision.thickness_outer = 0.01
            obj.collision.use_culling = False
            bpy.ops.object.shade_smooth()
            bpy.ops.transform.resize(value=(4, 4, 4))

            # 2.1 Create base plate
            bpy.ops.mesh.primitive_plane_add(size=10, enter_editmode=False, align='WORLD', location=(0, 0, 0))
            bpy.ops.object.modifier_add(type='COLLISION')
            obj.collision.thickness_outer = 0.01
            base_plane = bpy.context.object
            base_plane.name = "Floor"

            # 3. Create the cloth object
            bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(0, 0, 0))
            cloth = bpy.context.object
            cloth.name = "Cloth"
            bpy.ops.transform.translate(value=(0, 0, 4))
            bpy.ops.transform.resize(value=(4, 4, 4))
            bpy.ops.object.modifier_add(type='CLOTH')
            cloth_mod = cloth.modifiers["Cloth"]
            cloth_mod.settings.quality = 10
            cloth_mod.collision_settings.use_self_collision = True
            cloth_mod.collision_settings.collision_quality = 6
            cloth_mod.settings.bending_stiffness = 6
            cloth_mod.settings.mass = 1
            bpy.ops.object.shade_smooth()
            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.subdivide(number_cuts=50, smoothness=0)
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.modifier_add(type='SUBSURF')

            # 4. Simulate the cloth physics
            for frame in range(1, 121):  # Simulating for 100 frames as an example
                bpy.context.scene.frame_set(frame)
                bpy.ops.wm.redraw_timer(type='DRAW', iterations=1)

            # 5. Export the cloth object as an .obj file to the specified directory
            bpy.data.objects.remove(bpy.data.objects["Floor"])
            cloth = bpy.data.objects["Cloth"]  # This assumes the name of the cloth object is 'Cloth'
            export_path = os.path.join(destination_directory, filename)
            bpy.ops.object.select_all(action='DESELECT')
            cloth.select_set(True)
            #bpy.ops.transform.resize(value=(0.25, 0.25, 0.25))

            bpy.ops.export_scene.obj(filepath=export_path, use_selection=True)
            mtl_file_path = os.path.join(destination_directory, os.path.splitext(filename)[0] + ".mtl")
            if os.path.exists(mtl_file_path):
                os.remove(mtl_file_path)
            mesh = trimesh.load_mesh(export_path)
            mesh.apply_transform(trimesh.transformations.scale_matrix(0.25))
            mesh.export(export_path)
            print("Cloth #", ++i)

        else:
            print(f"No object imported from {filename}.")

clear_mesh_objects()  # Clear mesh objects after the loop completes

