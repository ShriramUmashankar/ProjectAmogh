#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32
from std_msgs.msg import Float64
from std_msgs.msg import Int32
from std_msgs.msg import Float64MultiArray
import time
import numpy as np

time_out=300
st= time.time()

nodeName = "depth_pitch"
rospy.init_node(nodeName, anonymous=True)

static = Float64MultiArray()
static.data=[1500,1500]

thrust1=0
thrust2=0
thrust = [1500,1500]
print("hello")

time.sleep(10)
    
pub = rospy.Publisher('thrust_info', Float64MultiArray, queue_size=10)

def callback1(msg):
    global thrust1,thrust2
    print(msg.data)
    thrust1 =float(msg.data)
    thrust2 =float(3000-msg.data)
    
def callback2(msg):
    global thrust,thrust1,thrust2
    
    thrust[0] = float(msg.data + thrust1)
    thrust[1] = float(msg.data + thrust2)
    
    thrust_pub = Float64MultiArray() 
    thrust_pub.data = thrust
    pub.publish(thrust_pub)
    with open('/home/jetson/catkin_ws/src/control/data_logging/thrust_reading.txt','a') as output:
        output.write(str(thrust)+'\n')

        
def shut_callback():
    rospy.loginfo("shutting down node")
    pub.publish(static)
    rospy.signal_shutdown("Shutting down due to conditions being met")

rospy.Subscriber('thrust_heave',Int32,callback1)
rospy.Subscriber('thrust_pitch',Int32,callback2)


rospy.on_shutdown(shut_callback)

rate = rospy.Rate(10)


if (time.time()-st) > time_out:
    pub.publish(static)
    rospy.signal_shutdown("Shutting down due to condition being met")

rospy.spin()    

