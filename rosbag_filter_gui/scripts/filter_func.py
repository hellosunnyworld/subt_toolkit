from tkinter import N
import rospy
import rosbag
import numpy as np
import math
from SimplePyQtGUIKit import ProgressBar
import sys
from tqdm import tqdm

motion_state = 0
a_sum = np.zeros(3)
g_sum = np.zeros(3)
msgs = []
a_vars = []
g_vars = []
i = -1
nProc = 0
	
def UpdateMotionState():
	global motion_state, a_sum, g_sum, msgs, a_vars, g_vars, i, n
	data = msgs[-1]
	if (nProc > 90):
		a_sum += np.asarray([data.linear_acceleration.x, data.linear_acceleration.y, data.linear_acceleration.z])
		g_sum += np.asarray([data.angular_velocity.x, data.angular_velocity.y, data.angular_velocity.z])
		
		a_avg = a_sum/len(msgs)
		g_avg = g_sum/len(msgs)
		
		a_var = 0
		g_var = 0
		for m in msgs:
			m_a = np.asarray([m.linear_acceleration.x, m.linear_acceleration.y, m.linear_acceleration.z])
			m_g = np.asarray([m.angular_velocity.x, m.angular_velocity.y, m.angular_velocity.z])
			a_var += np.dot((m_a - a_avg),(m_a - a_avg))
			g_var += np.dot((m_g - g_avg),(m_g - g_avg))
			
		a_var = math.sqrt(a_var / len(msgs))
		g_var = math.sqrt(g_var / len(msgs))
		a_vars.append(a_var)
		g_vars.append(g_var)
		i+=1
		if (i>3):
			if (a_vars[i] - a_vars[i-2] >= 0.001) or (g_vars[i] - g_vars[i-2] >= 0.0001):
				motion_state = 1
				return True
	return False
		



def filter(inf, topics, app):
	#outf = input("Please enter the file name of the output bag: ")
	#inf = input("Please enter the file name of the input bag: ")
	outf = inf[:-4]+"_filter.bag"
	global motion_state, a_sum, g_sum, msgs, a_vars, g_vars, i, nProc

	motion_state = 0
	a_sum = np.zeros(3)
	g_sum = np.zeros(3)
	msgs = []
	a_vars = []
	g_vars = []
	i = -1
	nProc = 0
	
	msgCount = 2*rosbag.Bag(inf).get_message_count()
	#print(msgCount)
	#qb = ProgressBar(5,100,app=app)
	pbar = tqdm(total=msgCount) 
	with rosbag.Bag(outf, 'w') as outbag:
		#print("open")
		for topic, msg, t in rosbag.Bag(inf).read_messages():
			if topic == "/imu/data" and motion_state == 0:
				msgs.append(msg)
				if UpdateMotionState():
					t_start = rospy.Time.from_sec(t.to_sec() - 30)
					break
			nProc +=1
			#qb.step = int(n/msgCount*100)
			#print(nProc / msgCount*100)
			pbar.update(n = 1) # Increments counter

		#qb.step = 50	
		pbar.update(n=(msgCount/2-nProc)) # Increments counter	
		nProc = msgCount/2
		for topic, msg, t in rosbag.Bag(inf).read_messages():
			if motion_state == 1 and t >= t_start:
				if topic in topics:
					outbag.write(topic, msg, t)
			nProc+=1
			#qb.step = int(n/msgCount*100)
			#print(nProc/msgCount*100)
			pbar.update(n=1) # Increments counter


