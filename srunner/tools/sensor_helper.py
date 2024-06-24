import yaml
import os
import limulator

packaging_dir = 'srunner/packaging'
output_dir = 'Output/'

def check_for_vehicle(packaging_dir, vehicle):
    vehicle = vehicle.lower()
    vehicle += ".yaml"
    file_path = os.path.join(packaging_dir, vehicle)

    return os.path.isfile(file_path), file_path


def read_packaging_info(vehicle, scenario_name):
    sensor_descriptions = []

    exist, file = check_for_vehicle(packaging_dir, vehicle)
    if not exist:
        return sensor_descriptions

    file = open(file, 'r')
    data = yaml.safe_load(file)

    for sensor_data in data['sensors']:
        sensor_description = limulator.SensorDescription()

        sensor_description.type = sensor_data['type']
        sensor_description.parent = sensor_data['parent']
        sensor_description.ip = sensor_data['ip']
        sensor_description.port = sensor_data['port']
        sensor_description.write_to_socket = sensor_data['write_to_socket']
        sensor_description.output_folder = os.path.join(output_dir, scenario_name, sensor_data['output_folder'])
        location = limulator.Location(**sensor_data['location'])
        rotation = limulator.Rotation(**sensor_data['rotation'])
        sensor_description.transform = limulator.Transform(location, rotation)

        parameters_data = sensor_data['parameters']

        if 1 <= sensor_data['type'] <= 3:
            sensor_description.scene_capture_sensor_description.image_width = parameters_data['image_width']
            sensor_description.scene_capture_sensor_description.image_height = parameters_data['image_height']
            sensor_description.scene_capture_sensor_description.scanning_frequency = (
                parameters_data)['scanning_frequency']
            sensor_description.scene_capture_sensor_description.show_2D_bounds = parameters_data['show_2D_bounds']
            sensor_description.scene_capture_sensor_description.show_3D_bounds = parameters_data['show_3D_bounds']
            sensor_description.scene_capture_sensor_description.show_occluded_objects = (
                parameters_data)['show_occluded_objects']

            pass
        elif sensor_data['type'] == 4:
            sensor_description.rotating_lidar_description.prf = parameters_data['prf']
            sensor_description.rotating_lidar_description.channels = parameters_data['channels']
            sensor_description.rotating_lidar_description.scanning_frequency = parameters_data['scanning_frequency']
            sensor_description.rotating_lidar_description.wavelength = parameters_data['wavelength']
            sensor_description.rotating_lidar_description.max_range = parameters_data['max_range']
            sensor_description.rotating_lidar_description.min_range = parameters_data['min_range']
            sensor_description.rotating_lidar_description.neg_vertical_fov = parameters_data['neg_vertical_fov']
            sensor_description.rotating_lidar_description.pos_vertical_fov = parameters_data['pos_vertical_fov']
            sensor_description.rotating_lidar_description.horizontal_fov = parameters_data['horizontal_fov']
            sensor_description.rotating_lidar_description.atmosphere_attenuation_rate = (
                parameters_data)['atmosphere_attenuation_rate']

        elif sensor_data['type'] == 6:
            sensor_description.solid_state_lidar_description.max_range = parameters_data['max_range']
            sensor_description.solid_state_lidar_description.min_range = parameters_data['min_range']
            sensor_description.solid_state_lidar_description.frequency = parameters_data['frequency']
            sensor_description.solid_state_lidar_description.channels_h = parameters_data['channels_h']
            sensor_description.solid_state_lidar_description.channels_v = parameters_data['channels_v']
            sensor_description.solid_state_lidar_description.neg_vertical_fov = parameters_data['neg_vertical_fov']
            sensor_description.solid_state_lidar_description.pos_vertical_fov = parameters_data['pos_vertical_fov']
            sensor_description.solid_state_lidar_description.neg_horizontal_fov = parameters_data['neg_horizontal_fov']
            sensor_description.solid_state_lidar_description.pos_horizontal_fov = parameters_data['pos_horizontal_fov']
            sensor_description.solid_state_lidar_description.wavelength = parameters_data['wavelength']
            sensor_description.solid_state_lidar_description.atmosphere_attenuation_rate = (
                parameters_data)['atmosphere_attenuation_rate']

        elif sensor_data['type'] == 7:
            # todo: bounding box sensor
            pass
        elif sensor_data['type'] == 8:
            # todo: radar
            pass

        sensor_descriptions.append(sensor_description)

    return sensor_descriptions
