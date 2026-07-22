# yahboom_rosmaster_teleop

![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-orange)
![ROS 2](https://img.shields.io/badge/ROS%202-Humble-blue)

Joystick teleoperation package for the real ROSMASTER X3 robot (ROS 2).

Part of the AIRclub-UdeSA organization, alongside:
- [`yahboom_rosmaster`](https://github.com/AIRclub-UdeSA/yahboom_rosmaster) — Gazebo Fortress simulator
- [`yahboom_rosmaster_slam`](https://github.com/AIRclub-UdeSA/yahboom_rosmaster_slam) — SLAM on the simulator

This repository targets the **physical robot**, not the simulator.

## Requirements

- Ubuntu 22.04
- ROS 2 Humble
- `joy` and `teleop_twist_joy` packages

## Build

Clone the repository and build it. The cloned folder acts as the ROS 2 workspace itself — no separate workspace folder is needed.

```bash
git clone https://github.com/AIRclub-UdeSA/yahboom_rosmaster_teleop.git
cd yahboom_rosmaster_teleop

source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y --rosdistro humble

colcon build --symlink-install
source install/setup.bash
```

## Quick Start

1. Turn on the robot and wait until the indicator light is fully green.
2. In a sourced terminal, set your ROS domain and verify the connection:

   ```bash
   export ROS_DOMAIN_ID=XX
   ros2 topic list
   ```

3. Launch teleoperation:

   ```bash
   ros2 launch yahboom_rosmaster_teleop teleop.launch.py
   ```

## Controls

| Control | Function |
|---|---|
| Hold R1 / RB | Normal speed |
| Hold L1 / LB | Turbo speed |
| Button A | Increase speed |
| Button B | Decrease speed |
| Stop Y | Emergency stop (speed = 0, no auto-resume) |
| Right stick | Forward/backward, strafe (left/right) |
| Left stick | Turn (yaw) |

> This configuration is designed for a Xbox-style controller. Button indices are defined in `speed_manager.py` — confirm them for your controller with `ros2 topic echo /joy`.

## Provenance

This repository complements [`AIRclub-UdeSA/yahboom_rosmaster`](https://github.com/AIRclub-UdeSA/yahboom_rosmaster), adding real-hardware joystick teleoperation not covered by the simulator workflow.

## License

BSD-3-Clause. See `LICENSE`.
