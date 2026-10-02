# ros_videostreams

A hands-on ROS 2 project that turns physical hardware into a video remote control.

An Arduino with a **potentiometer** and a **momentary button** streams readings over serial. ROS 2 nodes bridge that data onto topics, translate it into commands, and play videos from the [HF FineVideo dataset](https://huggingface.co/datasets/HuggingFaceFV/finevideo) in `rqt_image_view`.

**Goals**

- Learn the core ROS 2 concepts: nodes, topics, and launch files.
- Use physical hardware input to control video playback in rqt:
  - **Next** video
  - **Previous** video
  - **Play / pause**

---

## How it works

**Demo Video**
https://github.com/user-attachments/assets/94226502-090f-4f73-a865-5188ef304631

```
Arduino (pot + button)
        │  serial
        ▼
serial_bridge_node ──► /potentiometer, /button
        │
        ▼
serial_2_cmdinput_node OR command_input_node ──► /video_command   ("next" | "previous" | "play/pause")
        │
        ▼
video_player_node ──► /video/image_raw ──► rqt_image_view
```

| Input                                   | Command      |
| --------------------------------------- | ------------ |
| Potentiometer changes **to** 1023 (max) | `next`       |
| Potentiometer changes **to** 0 (min)    | `previous`   |
| Button pressed                          | `play/pause` |


`command_input_node` is an alternative way to send the same commands: it reads them from the keyboard in a terminal and publishes them to `/video_command` instead of using serial inputs

## RQT Graph!
![ROS graph of nodes and topics](graphs/rosgraph.png)

---

## Prerequisites

- Ubuntu with **ROS 2 Jazzy**
- An Arduino with a potentiometer and momentary button (sketch in `pot2serial/pot2serial.ino`)
- A [Hugging Face](https://huggingface.co) account (to download the dataset)

---

## Setup

### 1. Python environment and video download (all in terminal)

Create a virtual environment (one time):

```bash
sudo apt install python3 python3-full python3-venv   # only if venv isn't available yet
python3 -m venv ~/hf-env
```

Activate it (every time you open a new terminal):

```bash
source ~/hf-env/bin/activate
```

Install the Hugging Face libraries inside the virtual environment:

```bash
pip install datasets huggingface_hub
```

Create a Hugging Face access token (Hugging Face → Settings → Access Tokens), then log in and paste the token when prompted:

```bash
hf auth login
```

Download the sample videos. This collects the first 11 videos in Biology (i just like science) as a representative sample:

```bash
cd ros_videostreams/src
python3 get_videos.py
```

### 2. Arduino and serial port

Upload `pot2serial/pot2serial.ino` (from ros_videostreams/src) to the Arduino. It streams lines like:

```
Analog: 1023, Voltage: 5.00, Button Pressed: 0
Analog: 0, Voltage: 0.00, Button Pressed: 1
```

Allow your user to access the serial port, using **one** of these:

```bash
# Option A: one time only (requires logging out and back in, or a restart)
sudo usermod -aG dialout $USER

# Option B: must be repeated every time you reconnect the device
sudo chmod a+rw /dev/ttyACM0

Note: The port CAN change depending on your configuration. You can add this tag at the end of the run command to change it to match your set-up. port:=/dev/ttyACM0

Note: This script uses a baud rate of 115200.

```

> Close the Arduino IDE serial monitor before running the ROS nodes. Only one program can hold the port at a time.

### 3. Video player dependencies

```bash
sudo apt install python3-opencv ros-jazzy-rqt-image-view
```

### 4. Build the workspace

```bash
cd ~/Documents/ros_videostreams
colcon build
source install/setup.bash
```

---

## Running

### Option A: launch file (recommended)

```bash
ros2 launch ros_videostreams videostreams.launch.py
```

The launch file starts the serial bridge, the video player, and the rqt window.

To use a different serial port:

```bash
ros2 launch ros_videostreams videostreams.launch.py port:=/dev/ttyACM1
```

The default baud rate is 115200.

If you are using the keyboard input instead of the Arduino-driven command node, run `command_input_node` in a **separate terminal**:

```bash
ros2 run ros_videostreams command_input_node
```

### Option B: run each node manually

Use one terminal per command:

```bash
ros2 run ros_videostreams serial_bridge_node
ros2 run ros_videostreams video_player_node
ros2 run rqt_image_view rqt_image_view /video/image_raw
ros2 run ros_videostreams command_input_node
ros2 run ros_videostreams serial_2_cmdinput_node
```

---

## Nodes

| Node                      | Purpose                                                                  |
| ------------------------- | ------------------------------------------------------------------------ |
| `serial_bridge_node`      | Reads the Arduino's serial stream and publishes the pot and button data  |
| `serial_2_cmdinput_node`  | Converts pot/button events into `next`, `previous`, `play/pause`         |
| `command_input_node`      | Publishes the same commands typed at the command line                    |
| `video_player_node`       | Plays videos and publishes frames on `/video/image_raw`                  |
| `/rqt_gui_cpp_node_*`     | Interface between rqt_image_view and ROS graph, etc                      |

## Topics

| Topic              | Content                                       |
| ------------------ | --------------------------------------------- |
| `/potentiometer`   | Pot value, 0 to 1023                          |
| `/button`          | Button state, `true` / `false`                |
| `/video_command`   | `next`, `previous`, or `play/pause`           |
| `/video/image_raw` | Video frames shown in `rqt_image_view`        |
| `/parameter_events`| Logs of parameter changes, eg. port, baud rate|
| `/rosout`          | Logs of output errors, warnings, or msgs      |


---

## Debugging tips

```bash
ros2 topic list
ros2 topic echo /potentiometer
ros2 topic echo /button
ros2 topic echo /video_command
```

| Problem                                             | Likely fix                                                                                             |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `Permission denied` on `/dev/ttyACM0`               | Run the `dialout` or `chmod` step above                                                                |
| Package not found                                   | Run `source install/setup.bash`; check the package name is `ros_videostreams`                          |
| Blank rqt window                                    | The video player isn't publishing yet; check `ros2 topic list` for `/video/image_raw`                  |

---

## Future work: voice control

Not yet integrated. The goal is to say "next" or "previous" to control playback, using `speech_2_txt.py` which is already in the repo.

Set-up steps for the stand-alone voice control file:
```bash
source ~/hf-env/bin/activate
pip install SpeechRecognition
sudo apt install portaudio19-dev python3-pyaudio
pip install pyaudio
```
