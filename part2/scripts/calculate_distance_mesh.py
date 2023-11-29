import os
import numpy as np
import trimesh
from scipy.spatial import KDTree

# Define your directories
#Felix
cloth_dir = '/home/felix/PycharmProjects/comp_visual_perception_ws_23_24/part2/files/cloth_mesh/'
object_dir = '//home/felix/PycharmProjects/comp_visual_perception_ws_23_24/part2/files/object_mesh/'
output_dir = '/part2/files/distance_mesh/'
#Emanuel
#cloth_dir = 'D:/programmierte_programme/githubworkspace/comp_visual_perception_ws_23_24/part2/files/cloth_mesh/'
#object_dir = 'D:/programmierte_programme/githubworkspace/comp_visual_perception_ws_23_24/part2/files/object_mesh/'
#output_dir = 'D:/programmierte_programme/githubworkspace/comp_visual_perception_ws_23_24/part2/files/distance_mesh/'

# Get list of filenames in the directories
cloth_files = sorted([f for f in os.listdir(cloth_dir) if f.endswith('.obj')])
object_files = sorted([f for f in os.listdir(object_dir) if f.endswith('.obj')])

threshold = 0.1

# Iterate over the files
for cloth_file, object_file in zip(cloth_files, object_files):
    # Load the OBJ files
    cloth = trimesh.load(os.path.join(cloth_dir, cloth_file))
    object = trimesh.load(os.path.join(object_dir, object_file), force='mesh')

    # Sample points on the surface of the object
    # The number of points can be adjusted. More points mean finer sampling
    sampled_points = object.sample(1000000)

    # Extract vertices
    cloth_vertices = cloth.vertices
    object_vertices = object.vertices

    # Create a KDTree for efficient nearest neighbor search
    tree = KDTree(sampled_points)

    k = 5

    # Compute smoothed closest distances
    closest_distances = np.zeros(len(cloth_vertices))
    for i, point in enumerate(cloth_vertices):
        distances, _ = tree.query(point, k=k)
        closest_distances[i] = np.mean(distances)  # Average the distances

    # Normalize distances and convert to grayscale
    min_dist = np.min(closest_distances)
    max_dist = np.max(closest_distances)
    normalized_distances = [(d - min_dist) / (max_dist - min_dist) for d in closest_distances]
    grayscale_values = []
    for d in closest_distances:
        if d <= threshold:
            # Invert the normalization: closer points are lighter, farther are darker
            normalized_value = 1 - (d / threshold)  # Inverts the scale
            grayscale_value = int(255 * normalized_value)
        else:
            # Set distances greater than threshold to black
            grayscale_value = 0
        grayscale_values.append(grayscale_value)
    colors = [[gv, gv, gv, 255] for gv in grayscale_values]

    # Apply colors and export the cloth mesh
    cloth.visual.vertex_colors = colors
    cloth.export(os.path.join(output_dir, cloth_file))
