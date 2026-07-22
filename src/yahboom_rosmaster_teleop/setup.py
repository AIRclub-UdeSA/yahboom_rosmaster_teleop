import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'yahboom_rosmaster_teleop'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='AIRclub-UdeSA',
    maintainer_email='AIRClub@udesa.edu.ar',
    description='Joystick teleoperation package for the real ROSMASTER X3 robot',
    license='BSD-3-Clause',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'speed_manager = yahboom_rosmaster_teleop.speed_manager:main'        
        ],
    },
)
