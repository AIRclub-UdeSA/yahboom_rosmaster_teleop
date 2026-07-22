import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    config_file = os.path.join(
        get_package_share_directory('yahboom_rosmaster_teleop'),
        'config',
        'joy_mecanum.yaml'
    )

    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joy_node',
        output='screen',
    )

    teleop_node = Node(
        package='teleop_twist_joy',
        executable='teleop_node',
        name='teleop_twist_joy_node',
        parameters=[config_file],
        output='screen',
    )

    speed_manager_node = Node(
        package='yahboom_rosmaster_teleop',
        executable='speed_manager',
        name='speed_manager',
        output='screen',
    )

    return LaunchDescription([
        joy_node,
        teleop_node,
        speed_manager_node,
    ])