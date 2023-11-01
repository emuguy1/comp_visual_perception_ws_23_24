import pymeshlab as ml
import os


def scale_to_unit_sphere(input_path, output_path):
    ms = ml.MeshSet()
    ms.load_new_mesh(input_path)

    # Compute the transformation matrix for normalization to unit sphere
    ms.compute_matrix_from_scaling_or_normalization(unitflag=True)

    # Save the transformed mesh
    ms.save_current_mesh(output_path, save_textures=False, texture_quality=-1)


def main(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.obj'):
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.join(folder_path, 'scaled_' + filename)
            scale_to_unit_sphere(input_path, output_path)
            mtl_file = output_path.replace('.obj', '.obj.mtl')
            if os.path.exists(mtl_file):
                os.remove(mtl_file)
            print(f"Processed and saved scaled mesh to {output_path}")


if __name__ == "__main__":
    folder = '/home/felix/uni/WS23/CompVisP/'  # Replace with your folder path
    main(folder)
