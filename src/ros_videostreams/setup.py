from setuptools import find_packages, setup

package_name = 'ros_videostreams'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ljung6',
    maintainer_email='ljung6@example.com',
    description='Arduino-controlled video/audio scrubber',
    license='MIT',
    entry_points={
        'console_scripts': [
            'serial_bridge_node = ros_videostreams.serial_bridge_node:main',
            'video_player_node = ros_videostreams.video_player_node:main',
            'command_input_node = ros_videostreams.command_input_node:main',
            'serial_2_cmdinput_node = ros_videostreams.serial_2_cmdinput_node:main'
        ],
    },
)