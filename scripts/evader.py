#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import random
import math


laserfeed = [3,3]

def callback(data):
    global laserfeed
    laserfeed = data.ranges[90:270]

# evader node
def evader():
    rospy.init_node('evader', anonymous = True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    vel = Twist()
    
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        rospy.Subscriber("/base_scan", LaserScan, callback)
        rate.sleep()

        minRange = min(laserfeed)
        
        if minRange < 1:
            vel.linear.x = 0
            vel.angular.z = random.randint(0, int(2*math.pi))
        else:
            vel.angular.z = 0 
            vel.linear.x = 2
    
        pub.publish(vel)
  
        
if __name__ == '__main__':

    try:
        evader()
    except rospy.ROSInterruptException:
        pass
