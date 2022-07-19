#!/usr/bin/env python3

import roslib
roslib.load_manifest('lab5')
import rospy
from geometry_msgs.msg import Twist
import math
import tf

vel = Twist()

# pursuer controller
def pursuer():
    rospy.init_node('pursuer', anonymous = True)
    listener = tf.TransformListener()
    pub = rospy.Publisher('/robot_1/cmd_vel', Twist, queue_size=10)
    
    rate = rospy.Rate(10)
    rospy.sleep(1)
    while not rospy.is_shutdown():
       
        try:
            now = rospy.Time.now()
            past = now - rospy.Duration(0.6)
            listener.waitForTransformFull("/robot_1/base_link", now,
                                      "/robot_0/base_link", past,
                                      "/world", rospy.Duration(2.0))
            (trans, rot) = listener.lookupTransformFull("/robot_1/base_link", now,
                                      "/robot_0/base_link", past,
                                      "/world")
        except (tf.Exception, tf.LookupException, tf.ConnectivityException):
            continue

        angular = 4.1* math.atan2(trans[1], trans[0])
        linear = 0.52* math.sqrt(trans[0] ** 2 + trans[1] ** 2)
        vel.linear.x = linear
        vel.angular.z = angular

        pub.publish(vel)
        rate.sleep()
      

if __name__ == '__main__':

    try:
        pursuer()
    except rospy.ROSInterruptException:
        pass

# Referances:
# [1] http://wiki.ros.org/tf/Tutorials/Writing%20a%20tf%20listener%20%28Python%29
# [2] http://wiki.ros.org/tf/Tutorials/Time%20travel%20with%20tf%20%28Python%29