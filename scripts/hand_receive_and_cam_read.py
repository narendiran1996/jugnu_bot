#!/usr/bin/env python
# license removed for brevity
import rospy
import time
from std_msgs.msg import *
from visualization_msgs.msg import *

opub = rospy.Publisher('/okay', Int16, queue_size=10)
armp = rospy.Publisher('/toggle_led', Int16, queue_size=10)

rospy.init_node('hand_recive_and_cam_read', anonymous=True)
rate = rospy.Rate(10) # 10hz

stat=0
run_checkup=0
run_checkup_2=0
def reset_stat(a):
	global stat
	global run_checkup
	print a
	run_checkup=1
	stat=0
	
def cam_got(ad):
	global run_checkup_2
	global run_checkup
	global stat
	global armp
	if run_checkup_2==1:
		if ad.id == 201:
			print "we got 201"
			armp.publish(0)
	
		else:
			print "just leave and go"
		
			opub.publish(0)
			stat=4;
		run_checkup_2=0
		run_checkup=0
def idiot():
	global run_checkup_2
	global run_checkup
	global stat
	global armp
	print "IDIOT"
	if run_checkup_2==1:
		print "lov"
		if True:
			print "we got 201"
			armp.publish(0)
	
		else:
			print "just leave and go"
		
			opub.publish(0)
			stat=4;
		run_checkup_2=0
		run_checkup=0
def arm_over(zyx_):
	global stat
	global opub
	if stat==0:
		opub.publish(1)
		stat=stat+1

armsus=rospy.Subscriber("/arm_over", Int16, arm_over)
armres=rospy.Subscriber("/reset_stat", Int16,reset_stat)
armcam=rospy.Subscriber("/Estimated_marker_bot",Marker,cam_got)
while not rospy.is_shutdown():
       	if run_checkup==1:
		
		run_checkup_2=1
		time.sleep(2)
		#idiot()	
	rate.sleep()
