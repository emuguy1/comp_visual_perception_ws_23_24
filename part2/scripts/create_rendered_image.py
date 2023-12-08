import os
import bpy
import mathutils
import math
import random

# Felix
# folder_path = '/home/felix/PycharmProjects/'
# python_path = TODO
# Emanuel
folder_path = 'D:/programmierte_programme/githubworkspace/'
python_path = 'C:/Users/emanu/AppData/Local/Programs/Python/Python37/python.exe'

# Path to your OBJ file
filec = 1
is_distance_mesh = False
is_sample_run = False


def render_image():
    # Clear existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Making background transparent
    bpy.context.scene.render.film_transparent = True

    # Import the OBJ file
    if is_sample_run:
        bpy.ops.wm.obj_import(filepath=obj_path_sample)
    else:
        bpy.ops.wm.obj_import(filepath=obj_path)

    # Ensure the imported object is selected and active
    imported_obj = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active = imported_obj
    bpy.ops.object.shade_smooth()

    # Enable vertex color if is distance mesh
    if is_distance_mesh:
        # create new material and add vertex color as a color attribute
        mat = bpy.data.materials.new(name="VertexMat")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[3].default_value = (1, 1, 1, 1)
        mat.node_tree.nodes.new(type='ShaderNodeVertexColor')
        mat.node_tree.nodes["Color Attribute"].layer_name = "Color"
        mat.node_tree.links.new(mat.node_tree.nodes["Color Attribute"].outputs[0],
                                mat.node_tree.nodes["Principled BSDF"].inputs[0])
        imported_obj.data.materials.append(mat)
        bpy.context.object.active_material.shadow_method = 'NONE'
        bpy.context.object.active_material.diffuse_color = (1, 1, 1, 1)

    # Set up rendering parameters
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'  # Use the Cycles rendering engine
    scene.render.resolution_x = 512  # Set resolution width
    scene.render.resolution_y = 512  # Set resolution height
    scene.cycles.device = 'GPU'  # Use GPU rendering

    bpy.ops.object.light_add(type='SUN', radius=2, align='WORLD', location=(150, 150, 0))
    if is_distance_mesh:
        bpy.context.object.data.cycles.cast_shadow = False
    else:
        bpy.context.object.cycles.shadow_terminator_offset = 0.1

    # Create and position the camera
    camera_data = bpy.data.cameras.new(name='Camera')
    camera_object = bpy.data.objects.new('Camera', camera_data)
    scene.collection.objects.link(camera_object)
    scene.camera = camera_object

    camera_data.lens = 90

    def get_object_center(obj):
        local_bbox_center = sum((mathutils.Vector(b) for b in obj.bound_box), mathutils.Vector()) / 8
        return obj.matrix_world @ local_bbox_center

    # Function to calculate the visible size of the object in the camera's direction
    def visible_size(obj, h_angle, v_angle):
        dimensions = obj.dimensions
        # Adjustments to calculate size more accurately
        size_x = dimensions.x * abs(math.cos(h_angle))
        size_y = dimensions.y * abs(math.sin(h_angle))
        size_z = dimensions.z * abs(math.sin(v_angle))

        # Combine components to get the visible size
        return math.sqrt(size_x ** 2 + size_y ** 2 + size_z ** 2)

    # Function to calculate camera distance
    def calculate_camera_distance(obj, camera, desired_fill, h_angle, v_angle):
        # Visible size in the camera's direction
        visible_obj_size = visible_size(obj, h_angle, v_angle)

        # Camera's field of view calculation based on focal length
        sensor_width = camera.data.sensor_width
        focal_length = camera.data.lens
        camera_fov = 2 * math.atan(sensor_width / (2 * focal_length))

        # Calculate the required distance
        return visible_obj_size / (2 * math.tan(camera_fov / 2)) / desired_fill

    desired_fill = 1  # e.g., 80% fill

    # Function to orient the camera towards a target
    def look_at(obj, target):
        direction = target - obj.location
        rot_quat = direction.to_track_quat('-Z', 'Y')
        obj.rotation_euler = rot_quat.to_euler()

    # Create and position the camera (not shown for brevity)

    num_images = 50  # Total number of images to render

    if is_sample_run:
        num_images = 10

    for image_index in range(num_images):
        # Random horizontal and vertical angles
        h_angles = [216, 0, 324, 72, 252, 108, 144, 180, 36, 288]
        v_angles = [19, 28, 31, 41, 34]
        h_angle = math.radians(h_angles.pop(math.floor(image_index / 5)) + image_index)
        v_angle = math.radians(v_angles.pop(image_index % 5) + image_index % 4)
        if is_sample_run:
            v_angle = math.radians(45)
            h_angles = [216, 0, 324, 72, 252, 108, 144, 180, 36, 288]
            if filec == 4:
                h_angles = [38, 327, 75, 289, 352, 271, 82, 70, 20, 308]
            h_angle = math.radians(h_angles.pop(image_index))
        # Update camera distance
        distance = calculate_camera_distance(imported_obj, camera_object, desired_fill, h_angle, v_angle)

        # Calculate the actual center of the object
        obj_center = get_object_center(imported_obj)

        # Calculate camera position
        camera_x = math.sin(h_angle) * distance * math.cos(v_angle)
        camera_y = math.cos(h_angle) * distance * math.cos(v_angle)
        camera_z = distance * math.sin(v_angle)

        camera_object.location = obj_center + mathutils.Vector((camera_x, -camera_y, camera_z))

        # Point the camera to the object
        look_at(camera_object, obj_center)

        # Update the export path for each image
        if is_distance_mesh:
            scene.render.filepath = f"{export_path_distance[:-4]}_{image_index + 1}.png"
        elif not is_sample_run:
            scene.render.filepath = f"{export_path_normal[:-4]}_{image_index + 1}.png"
        else:
            scene.render.filepath = f"{export_path_sample[:-4]}{image_index + 1}.png"

        # Render the image
        bpy.ops.render.render(write_still=True)


for i in range(1, 10):
    filenum = str(filec)
    obj_path = folder_path + 'comp_visual_perception_ws_23_24/part2/files/distance_mesh/' + filenum + '.obj'
    export_path_normal = folder_path + 'comp_visual_perception_ws_23_24/part2/files/images_cloth/' + filenum + '.png'
    export_path_distance = folder_path + 'comp_visual_perception_ws_23_24/part2/files/images_distance_cloth/' + filenum + '.png'
    obj_path_sample = folder_path + 'comp_visual_perception_ws_23_24/part2/files/sample_mesh/' + filenum + '.obj'
    export_path_sample = folder_path + 'comp_visual_perception_ws_23_24/part2/files/sample_mesh_images/' + filenum + '/.png'
    is_distance_mesh = False
    render_image()
    if not is_sample_run:
        is_distance_mesh = True
        render_image()
    filec = filec + 1

#os.system(python_path + " " + folder_path + "comp_visual_perception_ws_23_24/part2/scripts/make_background_black.py")
