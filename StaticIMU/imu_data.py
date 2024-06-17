#!/usr/bin/env python3
import rospy
import math
from sbg_driver.msg import SbgEkfQuat
from sbg_driver.msg import SbgImuData
from std_msgs.msg import Float64MultiArray
import numpy as np 
import transformations as tf 
import time

# File path to save the angles
file_path = "angles_data.txt"

start_time = time.time()
def callback1(msg):
    quat = np.array([msg.quaternion.w,msg.quaternion.x,msg.quaternion.y,msg.quaternion.z])
    quat /= np.linalg.norm(quat)
    rotation_matrix=tf.quaternion_matrix(quat)
    euler = tf.euler_from_matrix(rotation_matrix)
    euler = np.array(euler)

    # Append the angles to the text file
    with open(file_path, mode='a') as file:  # Open the file in append mode
        np.savetxt(file, [list(euler)], delimiter=',', fmt='%f')  # Save the angles as a row in the text file

def main():
    while(True):
    	if ((time.time()-start_time)/60 > 30):
    	    break
    	rospy.init_node("imu_data",anonymous=True)
    	rospy.Subscriber("/sbg/ekf_quat",SbgEkfQuat,callback1)


if __name__=='__main__':
    main()
