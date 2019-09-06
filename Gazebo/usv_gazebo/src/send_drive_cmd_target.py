#!/usr/bin/env python
import rospy

from usv_gazebo_plugins.msg import Drive
from usv_gazebo.cfg import usv_gazebo_Config

from dynamic_reconfigure.server import Server

mach_pub = rospy.Publisher('target/usv_2/cmd_drive', Drive, queue_size=5)

para_cfg = [0, 0, 0]

def getConfigCallback(config, level): #spare_function::spare_function_Config
    global para_cfg
    if config.PC_Ctrl:
        para_cfg[0] = 1
        current = 0
    else:
        current = 0
        para_cfg[0] = 0
    para_cfg[1] = config.speed
    para_cfg[2] = config.rudder
    
    if para_cfg[0] == 0:
        drive = Drive()
        drive.left = para_cfg[1] + para_cfg[2]
        drive.right = para_cfg[1] - para_cfg[2]
        mach_pub.publish(drive)
    return config

if __name__ == "__main__":
    rospy.init_node("target_cmd", anonymous = True)

    config_srv = Server(usv_gazebo_Config, getConfigCallback)

    rate = rospy.Rate(10)
    max_count = 500
    current = 0
    v = 0.1
    while not rospy.is_shutdown():
        if para_cfg[0] == 1:
            #print ('process')
            if current < max_count:
                drive = Drive()
                drive.left = v
                drive.right = v
                mach_pub.publish(drive)
                current += 1

            else:
                current = 0
                v = -v
                print ('change order')
            

        rate.sleep()
    rospy.spin()

