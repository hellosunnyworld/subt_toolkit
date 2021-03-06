# subt_toolkit
## Introduction
This is a GUI interface for filtering according to topic and time as well as detecting path length and whether returning to the starting point.   
Each time this GUI processes all files (which must be rosbags) under the directory given by the user, considering these files as components of one complete running task of nuc or uav robot. This software first filters all rosbags and then computes the path length and the ending status of this one whole task.

## Usage and Function Description
### Installation and Run
1. This repository contains two ROS packages. Create one ROS workspace on your own computer and move these two packages into this workspace.
2. Install the dependency library PyQt5:
```
  pip install pyqt5
```
Note: To use this library, the python version should be python3.   
4. Compile this workspace   
5. Run the software:   
```
  cd [workspace]
  source devel/setup.bash
  python3 src/subt_proc_gui/scripts/rosbag_filter_gui.py
```

### Operate and Get the Results
1. After starting the program, one window will pop out for the input directory. Users should select the first file under the required directory which contains all rosbags of one task. All the files under the given directory must be rosbags. ![select bag](select_bag.PNG)
In this window, all the files under /media/muhanlin/Elements/R1_922_nuc will be selected after the user clicking "Open".    
Then the program displayed the names of selected files in the terminal and start to filter them one by one. ![selected_bags](selected_bag.PNG)
3. The second window pops out to ask the user to select the reserved topics (the program may spend tens of seconds extracting all topics and drawing the window, depending on the bag size). Drag the sliding bar to select all required topics and click "OK".    
![select_topic](select_topic.PNG)   
Then the program displays the names of all selected topics and starts filtering. We can see the progress of filter from the progress bar.    
![filter](filter.PNG)   
The format of the progress bar is: num_of_processed_msgs/total_num_of_msgs [current_elapsed_time<remaining_time, num_of_msgs/s]   
Sometimes one error is reported, but it does not influence the result.   ![err](potential_filter_err.PNG)   
The program works like this repeatedly to filter out all given rosbags.   
Note: If you want to compute path length and the ending status, /aft_mapped_to_init must be selected.         
   
There are some broken bags in subt database. This toolkit can fix them automatically when encountering them.   
![err_fix](err_fix.PNG)
4. After completing filtering, the program starts to compute path length and the ending status automatically if the user click "OK" in the message window.    
![finish_filter](finish_filter.PNG)   
The calculation is completed while playing the rosbags. We can see the progress messages in the terminal, outputted by roslaunch. After completing playing one rosbag, it will take about 20 seconds to terminate the processing node and record the data. The path length and displacements of the current single bag are not only displayed in the terminal, but also stored in txt files named after this single bag under the home directory of ros. After the process work of all bags completed, the total path length and whether the robot returns to the startng point finally will be shown by message window and stored in result.txt under the home directory of ros.   
![compute](compute_feature.PNG)   
![result](result.PNG)
## Visualization
I recommend you to use rviz or the following tool to check the path encoded in rosbags.   
[visualization tool]: https://github.com/facontidavide/PlotJuggler
## Current Issue
Still need rigorous data to verify the results of computing path length and determining whether returning to the original point. 
## Reference
https://github.com/AtsushiSakai/rosbag_filter_gui      
https://github.com/tqdm/tqdm
