# blackboard2api

## Getting started

### Step 1: Install Python if not already done.
Python 3.8 or newer is required.

### Step 2: Install requirements
execute 
```
pip3 install requirements.txt
```
in order to install all required modules.

### Step 3: Execute the code
Execute the code with 
```
python3 main.py path/to/video path/to/destination
```
The Program takes the video from the first argument and saves the images to the path of the second argument.
If only path/to/video is given, the images will be saved in the root folder of the project.
If no arguments are given, the program looks for a file "test.mp4" in a folder named "testfiles" within the root folder.
