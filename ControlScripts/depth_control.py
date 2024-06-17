#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
from std_msgs.msg import Int32
import time
import numpy as np

nodeName = 'depth_control'

rospy.init_node(nodeName, anonymous=True)

time.sleep(10)
    
pub = rospy.Publisher('thrust_heave', Int32, queue_size=10)

kp = 105
ki = 0
kd = 0.55

st = time.time()


integral_z = 0
prev_error_z = 0


def callBackFunction(message):
    global depth
    depth = message.data
    depth_control(depth)

rospy.Subscriber('depth_info', Float32, callBackFunction)


def depth_control(depth_reading):
    
    global integral_z, prev_error_z	
    # Set the desired depth value you want to maintain
    setpoint_depth = 0.40

    # Compute PID error terms
    error_z = setpoint_depth - depth_reading
    with open('/home/jetson/catkin_ws/src/control/data_logging/depth_reading.txt','a') as output:
        output.write(str(depth_reading)+'\n')

    integral_z += error_z
    derivative_z = error_z - prev_error_z

    pid_z = kp * error_z + ki * integral_z + kd * derivative_z

    thruster_speed = 1595 + int(pid_z)

    # Publish the thruster speed to the 'information' topic
    val = int(thruster_speed)
    pub.publish(3000-thruster_speed)
 
    prev_error_z = error_z

def shut_callback():
    rospy.loginfo("node is shutting down")
    pub.publish(1500)

rospy.on_shutdown(shut_callback)
# Main control loop
start_time = rospy.get_time()
timeout = 300

rate = rospy.Rate(10)

    
if (st - time.time() > timeout):
    rospy.loginfo("node is shutting down")
    pub.publish(1500)
    rospy.signal_shutdown("sssss")
