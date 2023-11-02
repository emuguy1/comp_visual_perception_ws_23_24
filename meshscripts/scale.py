
import os
import trimesh



def scale_to_unit_sphere(input_path, output_path):
    mesh = trimesh.load_mesh(input_path)

    mesh.apply_transform(trimesh.transformations.scale_matrix(1.0 / mesh.scale))

    mesh.export(output_path)




def main(folder_path, scaled_folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.obj'):
            print("Processing ", filename)
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.join(scaled_folder_path, filename)
            scale_to_unit_sphere(input_path, output_path)
    for filename in os.listdir(scaled_folder_path):
        if not filename.endswith('.obj'):
            os.remove(os.path.join(scaled_folder_path, filename))
            print("Removing ", filename)

if __name__ == "__main__":
    folder = '/home/felix/PycharmProjects/comp_visual_perception_ws_23_24/files/Objects'
    scaled_folder = '/home/felix/PycharmProjects/comp_visual_perception_ws_23_24/files/Scaled_Objects'
    main(folder, scaled_folder)
