#include <ros/ros.h>
#include <ros/console.h>
#include <ros/time.h>
#include "std_msgs/String.h"
#include "nav_msgs/Odometry.h"
#include <math.h>
#include <rosbag/view.h>
#include "sensor_msgs/Imu.h"
#include <cstdlib>
#include <fstream>
#include <string>
using namespace std;

double length;
double currtime;
double lasttime;
int motion_state_;
double vx, vy, vz;
double ax, ay, az;
struct Pos{
	int x;
	int y;
	int z;
}origin;
int systemDelay = 10;
int systemInitCount = 0;
bool systemInited = false;
bool systemFinished = false;
double odometryTime = 0;
double curTime[8];
float curX[8], curY[8], curZ[8];
int odomeID = -1;
float accuDis = 0;
float dx = 0;
float dy = 0;
float dz = 0;

// call the callback function after receive a subscription message
void odomCallback(const nav_msgs::Odometry::ConstPtr& msg)
{
 //ROS_INFO("odom callback");
 if (!systemInited) {
 	systemInitCount++;
	if (systemInitCount > systemDelay) 
		systemInited = true;
    	else if (systemInitCount == systemDelay)
  		lasttime= msg->header.stamp.toSec();   
  	else if (systemInitCount == 0){
	  	origin.x = msg->pose.pose.position.x;
	 	origin.y = msg->pose.pose.position.y;
	 	origin.z = msg->pose.pose.position.z;
  	}
 }

 if (systemFinished)
 	return;

 odometryTime = ros::WallTime::now().toSec();

 if (systemInited) {
 	float disX = msg->pose.pose.position.x - curX[odomeID];
 	float disY = msg->pose.pose.position.y - curY[odomeID];
 	float disZ = msg->pose.pose.position.z - curZ[odomeID];
 	accuDis += sqrt(disX * disX + disY * disY + disZ * disZ);
    
 	dx = msg->pose.pose.position.x - origin.x;
	dy = msg->pose.pose.position.y - origin.y;
	dz = msg->pose.pose.position.z - origin.z;
 }

 odomeID = (odomeID + 1) % 8;
 curTime[odomeID] = msg->header.stamp.toSec();
 curX[odomeID] = msg->pose.pose.position.x;
 curY[odomeID] = msg->pose.pose.position.y;
 curZ[odomeID] = msg->pose.pose.position.z;
}

int main(int argc, char ** argv){
	length = 0;
	motion_state_ = 0;
	// ROS node initialize
	ros::init(argc, argv, "subt_proc");
	// create node handler
	ros::NodeHandle n;
	string file_name;
	ros::param::get("file_name",file_name);
	for (int i = file_name.length()-1; i >= 0; i--){
        if (file_name[i] == '/'){
			file_name = file_name.substr((i+1),(file_name.length()-4-(i+1)))+".txt";
            break;
		}
	}
	ROS_INFO(("The result will be stored in "+file_name).c_str());
	ROS_INFO("Prepare to subscribe");
	// Create a Subsriber, subscribe the topic /chatte, register callback function chatterCallback
	ros::Subscriber sub = n.subscribe<nav_msgs::Odometry>("/aft_mapped_to_init",100,odomCallback);
	// Loop waiting for the callback function
	ros::WallRate rate(100);
	bool status = ros::ok();
	//double last_time_diff = 0.0;
	while (status) {
		ros::spinOnce();

		double timeDiff = ros::WallTime::now().toSec() - odometryTime;

		if (systemInited && timeDiff > 20.0) {
      			systemFinished = true;
    			break;
    		}

    		status = ros::ok();
    		rate.sleep();
 	}
 	ROS_INFO("path length %f", accuDis);
	ofstream record;
	record.open(file_name);
	record.trunc;
 
	record << "Path length: " << accuDis << endl;

	ROS_INFO("go for %f in x-axis", dx);
	record << dx << endl;
	ROS_INFO("go for %f in y-axis", dy);
	record << dy << endl;
	ROS_INFO("go for %f in z-axis", dz);
	record << dz << endl;

	record.close();
	return 0;
}

