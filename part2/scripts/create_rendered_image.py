import bpy
import mathutils
import math
import random

# Path to your OBJ file
obj_path = 'D:/programmierte_programme/githubworkspace/comp_visual_perception_ws_23_24/part2/files/distance_mesh/1.obj'
export_path = 'D:/programmierte_programme/githubworkspace/comp_visual_perception_ws_23_24/part2/files/images_cloth/1.png'

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Making background transparent
bpy.context.scene.render.film_transparent = True

# Import the OBJ file
bpy.ops.import_scene.obj(filepath=obj_path)

# Ensure the imported object is selected and active
imported_obj = bpy.context.selected_objects[0]
bpy.context.view_layer.objects.active = imported_obj

# Set up rendering parameters
scene = bpy.context.scene
scene.render.engine = 'CYCLES'  # Use the Cycles rendering engine
scene.render.resolution_x = 512  # Set resolution width
scene.render.resolution_y = 512  # Set resolution height

# Set background to black
world = bpy.data.worlds['World']
world.use_nodes = True
bg_node = world.node_tree.nodes.new(type='ShaderNodeBackground')
bg_node.inputs['Color'].default_value = (0, 0, 0, 1)


# Create and position the camera
camera_data = bpy.data.cameras.new(name='Camera')
camera_object = bpy.data.objects.new('Camera', camera_data)
scene.collection.objects.link(camera_object)
scene.camera = camera_object

camera_data.lens = 10

# Calculate the bounding box center of the object
bbox_center = sum((mathutils.Vector(b) for b in imported_obj.bound_box), mathutils.Vector()) / 8

# Function to calculate camera distance to fill a desired percentage of the frame
def calculate_camera_distance(obj, camera, desired_fill):
    # Get the dimensions of the object
    dimensions = obj.dimensions

    # Calculate the diagonal length of the bounding box
    diagonal = math.sqrt(sum([dim ** 2 for dim in dimensions]))

    # Assuming the camera FoV is horizontal
    camera_fov = camera.data.angle_x

    # Calculate the required distance
    return diagonal / (2 * math.tan(camera_fov / 2)) / desired_fill


desired_fill = 1  # e.g., 80% fill

# Function to orient the camera towards a target
def look_at(obj, target):
    direction = target - obj.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    obj.rotation_euler = rot_quat.to_euler()

# Create and position the camera (not shown for brevity)

num_images = 5  # Total number of images to render

for image_index in range(num_images):
    # Random horizontal and vertical angles
    h_angle = math.radians(random.uniform(0, 360))
    v_angle = math.radians(random.uniform(0, 45))

    # Update camera distance
    distance = calculate_camera_distance(imported_obj, camera_object, desired_fill)

    # Calculate camera position
    camera_x = math.sin(h_angle) * distance * math.cos(v_angle)
    camera_y = math.cos(h_angle) * distance * math.cos(v_angle)
    camera_z = distance * math.sin(v_angle)

    camera_object.location = bbox_center + mathutils.Vector((camera_x, -camera_y, camera_z))

    # Point the camera to the object
    look_at(camera_object, bbox_center)


    # Update the export path for each image
    scene.render.filepath = f"{export_path[:-4]}_{image_index}.png"

    # Render the image
    bpy.ops.render.render(write_still=True)