#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sbg_driver.msg import SbgImuData
import numpy as np
from wlmodem import WlModem
import time

class Transceiver(Node):

    def __init__(self):
        super().__init__('Modem')

        # Initialize the modem as an instance variable
        
        self.modem = WlModem("/dev/ttyUSB1")
        self.modem.connect()
        if not self.modem.connect():
            print("Failed to connect to modem")
            return

        success = self.modem.cmd_configure('a', 3)
        if success:
            print('success')

        else:
            print('failed')
            sys.exit(1)    
        if self.modem.cmd_get_diagnostic().get("link_up"):
            print("Link is up")

        self.modem.cmd_flush_queue()
        print("Queue flushed.")

        data = b"HelloSea"
        print("Sending initial data:", data)
        success = self.modem.cmd_queue_packet(data)
        print("Initial send status:", "Success" if success else "Failed")
        self.start = time.time() 

        self.acceleration = np.array(['0', '0', '0'])
        self.gyro = np.array(['0', '0', '0'])
        self.received = None

        # Subscription to IMU data
        self.subscription = self.create_subscription(
            SbgImuData,
            'sbg/imu_data',
            self.imu_callback,
            10)
        self.subscription  # prevent unused variable warning

    def imu_callback(self, msg):

        self.acceleration = [f"{val:#<8}" for val in np.round([msg.accel.x, msg.accel.y, msg.accel.z], 3).astype(str)]
        self.gyro = [f"{val:#<8}" for val in np.round([msg.gyro.x, msg.gyro.y, msg.gyro.z], 3).astype(str)]

        pkt = self.modem.get_data_packet(timeout=1)
        if pkt:
            print("Received packet:", pkt)
            self.received = pkt.decode("utf-8")

        # Send data at 1-second intervals
        data = self.select_data_to_send()
        if data:
            success = self.modem.cmd_queue_packet(data)
            print("Sent:", data, "| Status:", "Success" if success else "Failed")



    def select_data_to_send(self):

        if self.received == 'ax######':
            return self.acceleration[0].encode('utf-8')
        elif self.received == 'ay######':
            return self.acceleration[1].encode('utf-8')
        elif self.received == 'az######':
            return self.acceleration[2].encode('utf-8')
        elif self.received == 'wx######':
            return self.gyro[0].encode('utf-8')
        elif self.received == 'wy######':
            return self.gyro[1].encode('utf-8')
        elif self.received == 'wz######':
            return self.gyro[2].encode('utf-8')
        else:
            return self.acceleration[0].encode('utf-8')  # Default to 'ax'


def main(args=None):
    rclpy.init(args=args)

    node = Transceiver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
