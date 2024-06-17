#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32
import time
import numpy as np

nodeName = 'surge_control'

rospy.init_node(nodeName, anonymous=True)
pub = rospy.Publisher('thrust_surge', Int32, queue_size=10)

st = time.time()
time_out = 300

time.sleep(10)


def shut_callback():
    rospy.loginfo("node is shutting down")
    pub.publish(1500)

rospy.on_shutdown(shut_callback)

rate = rospy.Rate(10)

while not rospy.is_shutdown():

    if (time.time() - st > 20) and (time.time() - st < 25):
        pub.publish(1570) 
    elif (time.time() - st > 25) and (time.time() - st < 30)    
        pub.publish(1600)
    else:
        pub.publish(1500)    
        
        
    if (st - time.time() > time_out):
        rospy.loginfo("node is shutting down")
        pub.publish(1500)
        break

rospy.signal_shutdown("sssss")


