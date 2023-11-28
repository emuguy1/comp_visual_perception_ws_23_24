
import os

import numpy as np
import trimesh



def center_obj(input_path, output_path):
    mesh = trimesh.load_mesh(input_path)
    center = mesh.centroid
    # Create a translation matrix to move the centroid to the origin
    translation_to_origin = np.eye(4)
    translation_to_origin[:3, 3] = -center  # Translate by negative centroid
    mesh.apply_transform(translation_to_origin)
    lowest_z = mesh.vertices[:, 2].min()
    translation_to_zero = np.eye(4)
    translation_to_zero[2, 3] = -lowest_z  # Translate by -lowest_z
    mesh.apply_transform(translation_to_zero)

    mesh.apply_transform(trimesh.transformations.scale_matrix(1.0 / mesh.scale))

    mesh.export(output_path)




def main(folder_path, scaled_folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.obj'):
            print("Processing ", filename)
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.join(scaled_folder_path, filename)
            center_obj(input_path, output_path)
    for filename in os.listdir(scaled_folder_path):
        if not filename.endswith('.obj'):
            os.remove(os.path.join(scaled_folder_path, filename))
            print("Removing ", filename)

if __name__ == "__main__":
    folder = 'D:/programmierte_programme/githubworkspace/comp_visual_perception_ws_23_24/files/Scaled_Objects/'
    scaled_folder = 'D:/programmierte_programme/githubworkspace/comp_visual_perception_ws_23_24/files/centered_Scaled_Objects/'
    main(folder, scaled_folder)
