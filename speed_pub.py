#! /usr/bin/env python

import rospy
from duckietown_msgs.msg import WheelsCmdStamped
import numpy as np
from sensor_msgs.msg import CompressedImage
import matplotlib.pyplot as plt
import cv2

class LaserSubscriber():
    _r = None
    def __init__(self):
        self._s = rospy.Subscriber('/duckiequeen/camera_node/image/compressed', CompressedImage, self.callback)
        rospy.loginfo('[INFO] Started Laser Subscriber Node ..')
        self.img = None

    def callback(self, msg):
        np_arr = np.fromstring(msg.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        cv2.imshow('dump', image_np)
        cv2.waitKey(1)
        

class Publisher():
    def __init__(self):
        self._p = rospy.Publisher('duckiequeen/wheels_driver_node/wheels_cmd', WheelsCmdStamped, queue_size=1)
        self._s = WheelsCmdStamped()
        rospy.loginfo('[INFO] Started Publisher Node ..')

    def MoveStraight(self, l_v, r_v):
      self._s.vel_left = l_v
      self._s.vel_right = r_v
      self.publish_once_in_cmd_vel(self._s)

    def Stop(self):
      self._s.vel_left = 0
      self._s.vel_right = 0
      self.publish_once_in_cmd_vel(self._s)


    def publish_once_in_cmd_vel(self, cmd):
        while True:
            connections = self._p.get_num_connections()
            if connections > 0:
                self._p.publish(cmd)
                break
            else:
                rospy.Rate(1).sleep()


# Test
if __name__ == '__main__':
    try:
        rospy.init_node('our_shitty_duckiequeen', anonymous=True)
        bullshit = LaserSubscriber()
        speed_publisher = Publisher()
        speed_publisher.MoveStraight(0.5,0.5)

        rospy.sleep(5) # Move for five seconds
        speed_publisher.MoveStraight(0.0,0.0)
        rospy.spin()
        # speed_publisher.StopRobot()
    except rospy.ROSInterruptException:
        pass

