#!/usr/bin/env python
import rospy

from usv_gazebo_plugins.msg import Drive
from usv_gazebo.cfg import usv_gazebo_Config

from dynamic_reconfigure.server import Server

mach_pub = rospy.Publisher('self/usv/cmd_drive', Drive, queue_size=5)

def getConfigCallback(config, level): #spare_function::spare_function_Config
    para_cfg = [0, 0,0]

    para_cfg[0] = config.speed
    para_cfg[1] = config.rudder
    
    drive = Drive()
    drive.left = para_cfg[0] + para_cfg[1]
    drive.right = para_cfg[0] - para_cfg[1]
    mach_pub.publish(drive)
    return config

if __name__ == "__main__":
    rospy.init_node("self_cmd", anonymous = True)

    config_srv = Server(usv_gazebo_Config, getConfigCallback)

    rospy.spin()

