#!/usr/bin/env python3
import rospy
import math
from sbg_driver.msg import SbgEkfQuat
from std_msgs.msg import Int32
import numpy as np 
import transformations as tf 
import time

integral = 0
derivative = 0
prev_error = 0

kp= 10
kd= 2.1
ki=0


def callback1(msg):
    quat = np.array([msg.quaternion.w,msg.quaternion.x,msg.quaternion.y,msg.quaternion.z])
    quat /= np.linalg.norm(quat)
    rotation_matrix=tf.quaternion_matrix(quat)
    euler = tf.euler_from_matrix(rotation_matrix)
    euler = np.array(euler)*180/np.pi
    pid_control(0, euler[1])
    with open('/home/jetson/catkin_ws/src/control/data_logging/pitch_reading.txt','a') as output:
        output.write(str(euler[1])+'\n')
   


def pid_control(setpoint, measured_value):
    global integral,derivative,prev_error,kp,kd,ki
    error = setpoint - measured_value
    integral += error
    derivative = error - prev_error

    output = kp * error + ki * integral + kd * derivative
 
    val = Int32()
    val.data=int(output)
    pub.publish(val)
    
def shut_callback():
    rospy.loginfo("shutting down node")
    pub.publish(0)   

if __name__=='__main__':

    rospy.init_node("pitch_control",anonymous=True)
    rospy.Subscriber("/sbg/ekf_quat",SbgEkfQuat,callback1)

    global pub
    pub = rospy.Publisher("thrust_pitch",Int32,queue_size=10)
    
    rospy.on_shutdown(shut_callback)

    rospy.spin()     
