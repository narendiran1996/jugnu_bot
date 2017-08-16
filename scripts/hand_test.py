#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Int16

def talker():
    pub = rospy.Publisher('toggle_led', Int16, queue_size=10)
    rospy.init_node('tasdasdalker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
	x=input('Emter p[topm')
	pub.publish(x)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
