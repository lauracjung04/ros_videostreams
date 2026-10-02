from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ros_videostreams',
            executable='serial_bridge_node',
            name='serial_bridge_node',
            output='screen',
        ),
        Node(
            package='ros_videostreams',
            executable='video_player_node',
            name='video_player_node',
            output='screen',
        ),
        Node(
            package='rqt_image_view',
            executable='rqt_image_view',
            name='rqt_image_view',
            arguments=['/video/image_raw'],
            output='screen',
        ),
        Node(
            package='ros_videostreams',
            executable='serial_2_cmdinput_node',
            name='serial_2_cmdinput_node',
            output='screen',
        ),
        Node(
            package='ros_videostreams',
            executable='command_input_node',
            name='command_input_node',
            output='screen',
        ),
    ])