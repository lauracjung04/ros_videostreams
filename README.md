# ros_videostreams
Practing integration of multiple video streams in ROS, using HF FineVideo dataset

# Set Up
sudo apt install python3

1. Create the virtual environment (one time)
sudo apt install python3-full python3-venv   # only if venv isn't available yet
python3 -m venv ~/hf-env

2. Activate it (every time you open a new terminal)
source ~/hf-env/bin/activate

pip install datasets huggingface_hub #in the virtual environment

Make a hugging face account, go to access tokens, get a one-time access token

hf auth login

paste your token

cd to folder
python3 get_videos.py

run the code, it will collect the first 10 as a representative sample


#set up arduino
#allow access to port
sudo usermod -aG dialout $USER  #just once, requires restart
or 
sudo chmod a+rw /dev/ttyACM0 #required each time you connect the device

the arduino will stream: 
Analog: 1023, Voltage: 5.00, Button Pressed: 0
Analog: 1023, Voltage: 5.00, Button Pressed: 0
Analog: 1023, Voltage: 5.00, Button Pressed: 0
Analog: 1023, Voltage: 5.00, Button Pressed: 0
Analog: 1023, Voltage: 5.00, Button Pressed: 0
Analog: 1023, Voltage: 5.00, Button Pressed: 0

