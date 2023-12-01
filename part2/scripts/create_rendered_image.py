import os
import bpy
import mathutils
import math
import random

# Path to your OBJ file
obj_path = 'D:/programmierte_programme/githubworkspace/comp_visual_perception_ws_23_24/part2/files/distance_mesh/2.obj'
export_path = 'D:/programmierte_programme/githubworkspace/comp_visual_perception_ws_23_24/part2/files/images_cloth/2.png'
is_distance_mesh = False

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
bpy.ops.object.shade_smooth()


# Set up rendering parameters
scene = bpy.context.scene
scene.render.engine = 'CYCLES'  # Use the Cycles rendering engine
scene.render.resolution_x = 512  # Set resolution width
scene.render.resolution_y = 512  # Set resolution height

if not is_distance_mesh:
    bpy.ops.object.light_add(type='SUN', radius=2, align='WORLD', location=(150, 150, 50))


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

num_images = 5  # Total number of images to render

for image_index in range(num_images):
    # Random horizontal and vertical angles
    h_angle = math.radians(random.uniform(0, 360))
    v_angle = math.radians(random.uniform(0, 45))

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
    scene.render.filepath = f"{export_path[:-4]}_{image_index}.png"

    # Render the image
    bpy.ops.render.render(write_still=True)

os.system("C:/Users/emanu/AppData/Local/Programs/Python/Python37/python.exe D:/programmierte_programme/githubworkspace/comp_visual_perception_ws_23_24/part2/scripts/make_background_black.py")
