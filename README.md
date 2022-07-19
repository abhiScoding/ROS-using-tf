# Objectives
1. Design a controller that drives the robot(named Evader) straight at a constant speed of 2m/s. When
the robot is close to an obstacle, the robot should stop, turn in a random new direction,
and drive at the same speed.
2. Write a contollar for the second robot(named Pursuer) that subsribes to the tf messages from Evader
and follows the Evader by going to the spot it was at from two second before.

## Evader Controller (evader.py node)
- Evder subscribes to the laserscan data from the laser attached to it and triggers callback fuction
- The callback fuction stores laser ranges (which defines front of Evader) in a varivale "laserfeed"
- If an obstacle is in front of Evader and if detected, Evader is turned in random diretion using velocity
publisher

## Pursuer Controller (evader_pursuer.py and pursuer.py nodes)
**evader_pursuer.py**<br />
Followings ared added in evader.py:
- Used rosparameter "robot" and assigned value as robot0 and robot1, and stored in a variable "robotname"
- Published pos of both the robots to world frame

**pursuer.py**<br />
- using tf, pursuer subscribes to evader's pos
- speed of pursuer is proportional to difference in pos
- velocity command is given to pursuer using velocity publisher
### ROS concepts used: ROS parameters, tf
### Stage simulator is used in the project
