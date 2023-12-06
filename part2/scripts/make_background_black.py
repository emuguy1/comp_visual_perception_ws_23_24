import os
from PIL import Image

#Felix
#folder_path = '/home/felix/PycharmProjects/'
#python_path = TODO
#Emanuel
folder_path = 'D:/programmierte_programme/githubworkspace/'
python_path = 'C:/Users/emanu/AppData/Local/Programs/Python/Python37/python.exe'

def overlay_transparent_on_black(input_path, output_path):
    try:
        img = Image.open(input_path)

        # Convert image to RGBA if not already in that mode
        img = img.convert("RGBA")

        # Create a new black background image with the same dimensions
        background = Image.new("RGBA", img.size, (0, 0, 0, 255))

        # Composite the original image onto the black background
        overlaid_img = Image.alpha_composite(background, img)

        # Save the overlaid image
        overlaid_img.save(output_path)

        print(f"Image processed successfully. Saved as: {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

def process_images_in_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' not found.")
        return

    # Iterate through files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith('.png'):
            input_file = os.path.join(folder_path, file_name)
            output_file = os.path.join(folder_path, file_name)
            overlay_transparent_on_black(input_file, output_file)

# Replace with your folder path
folder_to_process_one = folder_path+'comp_visual_perception_ws_23_24/part2/files/images_cloth/'
folder_to_process_two = folder_path+'comp_visual_perception_ws_23_24/part2/files/images_distance_cloth/'
folder_to_process_three = folder_path+'comp_visual_perception_ws_23_24/part2/files/sample_mesh_images/1/'
folder_to_process_four = folder_path+'comp_visual_perception_ws_23_24/part2/files/sample_mesh_images/2/'
folder_to_process_five = folder_path+'comp_visual_perception_ws_23_24/part2/files/sample_mesh_images/3/'
folder_to_process_six = folder_path+'comp_visual_perception_ws_23_24/part2/files/sample_mesh_images/4/'

process_images_in_folder(folder_to_process_one)
process_images_in_folder(folder_to_process_two)
process_images_in_folder(folder_to_process_three)
process_images_in_folder(folder_to_process_four)
process_images_in_folder(folder_to_process_five)
process_images_in_folder(folder_to_process_six)