# subt_toolkit
## Introduction
This is a GUI interface for filtering according to topic and time as well as detecting path length and whether returning to the starting point.   
Each time this GUI processes all files (which must be rosbags) under the directory given by the user, considering these files as components of one complete running task of nuc or uav robot. This software first filters all rosbags and then computes the path length and the ending status of this one whole task.

## Usage and Function Description
### Installation and Run
1. This repository contains two ROS packages. Create one ROS workspace on your own computer and move these two packages into this workspace.
2. Compile this workspace
3. Run the software:
```
  source devel/setup.bash
  rosrun rosbag_filter_gui rosbag_filter_gui.py
```

### Operate and Get the Results
1. At first, one hint tells the user the software starts successfully:![start](image.png)
2. One window will pop out. Users should select the first file under the required directory which contains all rosbags of one task. All the files under the given directory must be rosbags. ![select directory](select_bag.png)
In this window, all files under /media/muhanlin/Elements/R1_922_nuc will be selected after the user clicking "Open". 
