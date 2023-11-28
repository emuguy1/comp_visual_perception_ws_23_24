import os
import numpy as np
import trimesh
from scipy.spatial import KDTree

# Define your directories
cloth_dir = '/home/felix/PycharmProjects/comp_visual_perception_ws_23_24/files/submission/cloths'
object_dir = '/home/felix/PycharmProjects/comp_visual_perception_ws_23_24/files/submission/objects'
output_dir = '/home/felix/PycharmProjects/comp_visual_perception_ws_23_24/files/colored_cloths'

# Get list of filenames in the directories
cloth_files = sorted([f for f in os.listdir(cloth_dir) if f.endswith('.obj')])
object_files = sorted([f for f in os.listdir(object_dir) if f.endswith('.obj')])

# Iterate over the files
for cloth_file, object_file in zip(cloth_files, object_files):
    # Load the OBJ files
    cloth = trimesh.load(os.path.join(cloth_dir, cloth_file))
    object = trimesh.load(os.path.join(object_dir, object_file))

    # Extract vertices
    cloth_vertices = cloth.vertices
    object_vertices = object.vertices

    # Create a KDTree for efficient nearest neighbor search
    tree = KDTree(object_vertices)

    # Compute the closest distance for each point in the cloth to the object
    closest_distances = np.zeros(len(cloth_vertices))
    for i, point in enumerate(cloth_vertices):
        distance, _ = tree.query(point)
        closest_distances[i] = distance

    # Normalize distances and convert to grayscale
    min_dist = np.min(closest_distances)
    max_dist = np.max(closest_distances)
    normalized_distances = [(d - min_dist) / (max_dist - min_dist) for d in closest_distances]
    grayscale_values = [int(255 * d) for d in normalized_distances]
    colors = [[gv, gv, gv, 255] for gv in grayscale_values]

    # Apply colors and export the cloth mesh
    cloth.visual.vertex_colors = colors
    cloth.export(os.path.join(output_dir, cloth_file))
