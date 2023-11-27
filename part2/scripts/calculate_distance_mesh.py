import trimesh
import bpy
#from mathutils import Vector
import numpy as np
from scipy.spatial import distance
import matplotlib


def clear_mesh_objects():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

# Load OBJ file using trimesh
def load_obj(file_path):
    mesh = trimesh.load_mesh(file_path)
    return mesh

# Calculate nearest distance for each point in set1 to set2
def nearest_distance_set1_to_set2(points1, points2):
    distances = []
    for point1 in points1:
        nearest_dist = np.inf
        for point2 in points2:
            dist = distance.euclidean(point1, point2)
            if dist < nearest_dist:
                nearest_dist = dist
        distances.append(nearest_dist)
        print("calculated distance: " + str(nearest_dist))
    return distances

# Update mesh vertex colors based on distances
def update_mesh_with_colors(mesh_obj, distances):
    clear_mesh_objects()
    white = (1, 1, 1)
    black = (0, 0, 0)
    bpy.ops.import_scene.obj(filepath=obj_file_path_1)

    # must switch to Object Mode briefly to get the new set of selected elements
    # and then change the vertex_color layer
    obj = bpy.context.active_object

    mesh = obj.data
    color_layer = mesh.vertex_colors.active
    selected = set(v.index for v in obj.data.vertices if v.select)

    verts = mesh.vertices
    i = 0
    for poly in mesh.polygons:
        for loop_index in poly.loop_indices:
            vidx = mesh.loops[loop_index].vertex_index
            if vidx in selected:
                # How to apply gradient color
                # pure white color on the highest vertices
                # black color on the bottom vertices
                # and of cource interpolated grayscale values for all verts in the middle
                color_layer.data[i].color = (1, 1, 1)
            i += 1

    # set to vertex paint mode to see the result
    # bpy.ops.object.mode_set(mode='VERTEX_PAINT')
    bpy.ops.object.mode_set(mode='EDIT')
    #mesh_obj.poly
    #colors = np.clip(1 - 10 * (distances.pop() - 0.1), 0, 1)
    #mesh_obj.visual.vertex_colors = trimesh.visual.interpolate(colors, 'jet')
    #return mesh_obj
    bpy.ops.export_scene.obj(filepath=output_obj_file, use_selection=True)

source_directory = "D:/programmierte_programme/githubworkspace/comp_visual_perception_ws_23_24/part2/files/"

# Replace with the paths to your OBJ files
obj_file_path_2 = source_directory + "object_mesh/1.obj"
obj_file_path_1 = source_directory + "cloth_mesh/1.obj"
print("Load files")
# Load OBJ files
mesh1 = load_obj(obj_file_path_1)
points_set1 = mesh1.vertices.take([0, 100])
points_set2 = load_obj(obj_file_path_2).vertices

print("Loaded files")
print("count points_set1" + str(points_set1.size))
# Calculate nearest distances for each point in set1 to set2
distances_set1_to_set2 = nearest_distance_set1_to_set2(points_set1, points_set2)
print("calculate distances")
# Update mesh with per-vertex color data based on distances
updated_mesh = update_mesh_with_colors(mesh1, distances_set1_to_set2)

print("export file")
# Save the updated mesh with colors to a new OBJ file
output_obj_file = source_directory + "distance_mesh/1.obj"
updated_mesh.export(output_obj_file)

print(f"Mesh with colors saved to {output_obj_file}")
