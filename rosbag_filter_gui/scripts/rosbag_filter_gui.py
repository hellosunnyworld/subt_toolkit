#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import rospy
from rospkg import get_ros_home
from SimplePyQtGUIKit import SimplePyQtGUIKit
from PyQt5 import QtGui,QtWidgets
import rosbag
import subprocess
import filter_func
import os
import roslaunch
from os import listdir
from os.path import isfile, join

def GetTopicList(path):
    bag = rosbag.Bag(path)
    topics = list(bag.get_type_and_topic_info()[1].keys())
    return topics

def main():
    rospy.init_node('rosbag_filter_gui', anonymous=True)
    app = QtWidgets.QApplication(sys.argv)

    length = 0
    dx = 0
    dy = 0
    dz = 0
    returnThre = 3

    # #GetFilePath
    files=SimplePyQtGUIKit.GetFilePath(isApp=True,caption="Select bag file",filefilter="*bag")
    #  print files
    if len(files)<1:
        print("Please select a bag file")
        sys.exit()
    #  get the directory
    for kk in range(len(files[0])-1,0,-1):
        if files[0][kk] == '/':
            break
    path = files[0][2:kk]
    # get all files under this directory
    onlyfiles = [join(path, f) for f in listdir(path) if isfile(join(path, f))]

    for i in range(len(onlyfiles)):
        print("Having chosen",onlyfiles[i])
        # if onlyfiles[i][-5] == '0':
        #     first = i

    for file_name in onlyfiles:
        print("----------------------------------------------")
        print("Process "+file_name+'...')
        print("Extract topic list from the bag...")
        try:
            # Draw the topic selecting window
            topics=GetTopicList(file_name)
            selectWin = SimplePyQtGUIKit()
            selected=selectWin.GetCheckButtonSelect(topics,app=app,msg="")
            # filter
            print("Converting....")
            filter_func.filter(file_name,selected,app)
        except:
            # Repair the bag if it is broken
            print("Broken rosbag. Repair it by reindexing...")
            cmd="rosbag reindex "+file_name
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout_data, stderr_data = p.communicate()
            print("Repair complete.")
            # retry
            print("Extract topic list from the bag...")
            topics=GetTopicList(file_name)
            selectWin = SimplePyQtGUIKit()
            selected=selectWin.GetCheckButtonSelect(topics,app=app,msg="")

            print("Converting....")
            filter_func.filter(file_name,selected,app)
    # inform the user that the filter is completed
    QtWidgets.QMessageBox.information(QtWidgets.QWidget(), "Message", "Finish convert all bags!!\nContinue to extract feature?")
    

    print("Extract feature...")
    for file_name in onlyfiles:
        print("-------------------------------------------------")
        print("Analyze "+file_name+'...')
        # subprocess_Popen and subprocess_call cannot call roslaunch. 
        # Use roslaunch module of python
        package_path = str(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        cli_args = [package_path+'/subt_proc/launch/subt_proc.launch','file_path:='+file_name[:-4]+"_filter.bag"]
        roslaunch_args = cli_args[1:]
        roslaunch_file = [(roslaunch.rlutil.resolve_launch_arguments(cli_args)[0], roslaunch_args)]
        uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
        roslaunch.configure_logging(uuid)
        parent = roslaunch.parent.ROSLaunchParent(uuid, roslaunch_file)
        parent.start() 
        try:
            parent.spin()
        finally:
            parent.shutdown()
        # read the result of this single bag
        result_path = get_ros_home() + '/' + file_name[(kk-1):-4] + "_filter.txt"
        final_result_path = get_ros_home() + "/result.txt"
        with open(result_path,'r') as f:
            #features = f.read()
            pathMsg = f.readline()
            pathMsgPos = pathMsg.find(':') + 1
            # path length
            length += float(pathMsg[pathMsgPos:])
            # displacements
            dx += float(f.readline())
            dy += float(f.readline())
            dz += float(f.readline())
    # get the final result, display and store
    features = "Path length = "+str(length)+"\n"
    if (abs(dx) < returnThre) and (abs(dy) < returnThre) and (abs(dz) < returnThre): 
        features += "End at the starting point!"
    else:
        features += "End at half way."
    with open(final_result_path,'w') as f:
        f.write(features)
    QtWidgets.QMessageBox.information(QtWidgets.QWidget(), "Message", features)   


if __name__ == '__main__':
    print("rosbag_filter_gui start!!")
    main()

