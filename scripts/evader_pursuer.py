#!/usr/bin/env python3

import roslib
roslib.load_manifest('lab5')
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import random
import math
import tf
from nav_msgs.msg import Odometry

vel = Twist()
odom = Odometry()
laserfeed = [3,3]

def callback(data):
    global laserfeed
    laserfeed = data.ranges[90:270]

def callback1(data1):
    global odom
    odom = data1 

# broadcast position of evader and pursuer to world
def robot_pose(robotname):
    rospy.Subscriber("/%s/odom" %robotname, Odometry, callback1)
    br = tf.TransformBroadcaster()
    br.sendTransform((odom.pose.pose.position.x, odom.pose.pose.position.y, odom.pose.pose.position.z),
                        tf.transformations.quaternion_from_euler(odom.pose.pose.orientation.x, odom.pose.pose.orientation.y, odom.pose.pose.orientation.z),
                        rospy.Time.now(),
                        "/%s/odom" %robotname,
                        "world")


# evader controller
def evader():
    rospy.init_node('evader', anonymous = True)
    robotname = rospy.get_param('~robot')
    pub = rospy.Publisher('/robot_0/cmd_vel', Twist, queue_size=10)
    
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        rospy.Subscriber("/robot_0/base_scan", LaserScan, callback)

        rate.sleep()
        min_dist = min(laserfeed)
        
        if min_dist < 2.3:
            vel.linear.x = 0
            vel.angular.z = random.randint(0, int(2*math.pi))
        else:
            vel.angular.z = 0 
            vel.linear.x = 2
    
        pub.publish(vel)
        robot_pose(robotname)
        

if __name__ == '__main__':

    try:
        evader()
    except rospy.ROSInterruptException:
        pass



# Referances:
# [1] http://wiki.ros.org/tf/Tutorials/Writing%20a%20tf%20broadcaster%20%28Python%29
