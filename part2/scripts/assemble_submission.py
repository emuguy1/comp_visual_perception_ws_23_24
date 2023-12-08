import os
import shutil
import random

folder_path = 'D:/programmierte_programme/githubworkspace/'
source_path_normal = folder_path + 'comp_visual_perception_ws_23_24/part2/files/images_cloth/'
source_path_distance = folder_path + 'comp_visual_perception_ws_23_24/part2/files/images_distance_cloth/'
source_path_meshes = folder_path + 'comp_visual_perception_ws_23_24/part2/files/distance_mesh/'

destination_path_normal = folder_path + 'comp_visual_perception_ws_23_24/part2/files/submission/cloth/'
destination_path_distance = folder_path + 'comp_visual_perception_ws_23_24/part2/files/submission/distances/'
destination_path_meshes = folder_path + 'comp_visual_perception_ws_23_24/part2/files/submission/meshes'


def copy_and_rename_images():
    for i in range(1, 101):
        new_indices = list(range(1, 51))
        for j in range(50):
            source_img1 = os.path.join(source_path_normal, f"{i}_{j}.png")
            source_img2 = os.path.join(source_path_distance, f"{i}_{j}.png")

            new_index_name = new_indices.pop(random.randint(0, len(new_indices)-1))
            dest_img1 = os.path.join(destination_path_normal, f"{i}_{new_index_name}.png")
            dest_img2 = os.path.join(destination_path_distance, f"{i}_{new_index_name}.png")

            shutil.copyfile(source_img1, dest_img1)
            shutil.copyfile(source_img2, dest_img2)
        if i < 6:
            source_mesh = os.path.join(source_path_meshes, f"{i}.obj")
            dest_mesh = os.path.join(destination_path_meshes, f"{i}.obj")
            shutil.copyfile(source_mesh, dest_mesh)


copy_and_rename_images()
