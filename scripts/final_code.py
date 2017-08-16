import cv2
import numpy as np
import rospy
from visualization_msgs.msg import Marker
from std_msgs.msg import *
from geometry_msgs.msg import *
import time
from datetime import timedelta
import sys
import math


manual_op=0


max_speed=150
initial_speed=[max_speed,max_speed]
speed=initial_speed
ids={}
id_dict={}
exiting=False

flist={}

run_id_check=False
armp = rospy.Publisher('/toggle_led', Int16, queue_size=10)

rospy.init_node('gunda', anonymous=True)


rate = rospy.Rate(10) # 10hz

vpub = rospy.Publisher('/vel', Vector3, queue_size=10)

reset_stat = rospy.Publisher('/reset_stat', Int16, queue_size=10)
cidd=0
p_ids_count=0
ldist=0
rdist=0
ang=0
got_every_id=False
path_follow_stat=False
ir_val=0
def set_speed(sp1,sp2):
	global vpub
	vpub.publish(Vector3(sp1,sp2,0))

def differ(x,y):
	if x>=0 and y>=0:
		return abs(x-y)
	if x>=0 and y<=0:
		return abs(x+abs(y))
	if x<=0 and y>=0:
		return abs(abs(x)+y)
	if x<=0 and y<=0:
		return abs(abs(x)-abs(y))


def turn_(left,right,sang=50):
	global speed
	global rospy
	global ang
	global path_follow_stat
	print "going to turn"
	
	speed=[0,0]
	set_speed(0,0)	
	time.sleep(0.5)	
	bef_ang=ang
	while abs(ang-bef_ang)<=sang:
		print abs(ang-bef_ang),ang
		set_speed(left*250,right*250)
		time.sleep(0.01)
	speed=[0,0]
	set_speed(0,0)	
	time.sleep(2)

	speed=[250,250]
	set_speed(250,250)	
	time.sleep(.5)

	speed=[0,0]
	set_speed(0,0)	
	time.sleep(2)
	path_follow_stat=True
	print "finished turning"
def okay_(xyz_):
	global path_follow_stat
	global cidd
	if xyz_.data==1:
		cidd=200
	print "got oaky from cam and can move"
	set_speed(250,250);
	time.sleep(0.5) #offset dist to get away from black lines
	path_follow_stat=True
	
def Update_dist(dist_):
	global ldist
	global rdist
	global ang
	global ir_val
	ldist=dist_.linear.x
	rdist=dist_.linear.y
	if ldist == 0:
		ldist = 1500
	if rdist == 0:
		rdist = 1500
	ang=dist_.linear.z
	if dist_.angular.y>800:
		ir_val=1
	else:
		ir_val=0

def perform_test_marker():
	global speed
	global path_follow_stat	
	global reset_stat
	print "detected_black"
	reset_stat.publish(1)
	speed=[0,0]
	set_speed(0,0)
	time.sleep(2)


def Marker_Detected(k):
	global cidd
	global sus
	global speed
	global ids
	global sus
	global flist
	global id_dict
	global run_id_check
	global exiting
	global path_follow_stat
	global got_every_id
	global exiting
	global armp
	x=k.pose.position.x
	y=k.pose.position.y
	z=k.pose.position.z
	cid=k.id
	dist=0
	ids[cid]=cid
	val=math.sqrt(x**2+y**2+z**2)
	id_dict[cid]=[x,y,z,val]
	#print len(ids)
	
	if len(ids)==5 and run_id_check==True and path_follow_stat==False:

		l_id=[]
		r_id=[]
		print "five ids detected"
		
		path_follow_stat=False
		speed=[0,0]
		set_speed(0,0)
		s=np.array(id_dict.values())[:,1]
		avg=np.average(s)
		for id_i in ids:
			if id_dict[id_i][1]<avg:
				if id_i not in l_id:
					l_id.append(id_i)
			elif id_dict[id_i][1]>avg:
				if id_i not in r_id:
					r_id.append(id_i)
		for ll in l_id:	
			diff={}
			mid=0
			mdiff=999
			for rr in r_id:	
				diff[rr]=differ(id_dict[rr][0],id_dict[ll][0])
				if mdiff>diff[rr]:
					mdiff=diff[rr]
					mid=rr
			flist[ll]=mid
	 
		speed=[0,0]
		run_id_check=False
		got_every_id=True

	

	if run_id_check==False and got_every_id==True and exiting==False:
		
		sus.unregister()
		print cidd
		print flist
		direct=flist[cidd]
		if cidd==200:
			print "we are going to exit"
			exiting=True
			#direct=444
			speed=[250,250]
			set_speed(speed[0],speed[1])
			time.sleep(0.25)
			speed=[0,0]
			set_speed(speed[0],speed[1])
			time.sleep(2)	
		print direct
		ids.clear()
		
		id_dict.clear();
		flist.clear()

		
		set_speed(0,0)
		time.sleep(0.5)
		if direct == 222:
			print "left"
			turn_(0,1)
		elif direct == 111:
			speed=[250,250]
			set_speed(250,250)
			time.sleep(2)
			print "straight"
			path_follow()
		elif direct ==333:
			print "right"
			#changed
			turn_(1,0)
			#dont need after this
		elif direct ==444:
			print "WERDFGHNM RIGHT"
		
			turn_(1,0)
			#DONT NEED BEFORE THIS
		else:
			print "stoping si also fun"
			speed=[0,0]
			set_speed(0,0)
		

		
		
		run_id_check=False
		got_every_id=False

		path_follow_stat=True

def path_follow():
	mxval=300	
	global speed
	global ldist
	global rdist
	global speed
	global path_follow_stat
	global run_id_check
	global ir_val
	global sus
	global ids
	global id_dict
	global flist
	global exiting
	if path_follow_stat==True:
		if ir_val==1:
			path_follow_stat=False

			
			perform_test_marker()
		
		else:
			
			print "path following",ldist,rdist
			if ldist>500 or rdist>500:
				path_follow_stat=False
				speed=[250,250]
				set_speed(speed[0],speed[1])
				time.sleep(0.5)
				speed=[0,0]
				set_speed(speed[0],speed[1])
				time.sleep(5)	
				if ldist>500 and rdist>500:		
					ids.clear()
			
					id_dict.clear();
					flist.clear()					
					print "waiting for the arucos - direction"
					run_id_check=True
					if exiting==True:
		
						print "dropping"			
						armp.publish(1)
						set_speed(0,0)
						sys.exit()
						exiting=False
					sus = rospy.Subscriber("/Estimated_marker", Marker,  Marker_Detected)
					
				if (ldist<500 and rdist>500):	
					print "compulsory turn"
					turn_(0,1)
				if (rdist<500 and ldist>500):					
					print "compulsory turn"
					turn_(1,0)

			
			if ldist<mxval and rdist<mxval:
				speed=[250,250]
			elif ldist>mxval and rdist<mxval :
				speed=[250,170]
			elif ldist<mxval and rdist>mxval:
				speed=[170,250]
			


			


			set_speed(speed[0],speed[1])


sus = rospy.Subscriber("/Estimated_marker", Marker,  Marker_Detected)
okay_sub = rospy.Subscriber("/okay",Int16,okay_)
dist_sub = rospy.Subscriber("/dist", Twist,  Update_dist)

def Init_all(x):
	global cidd
	global path_follow_stat

	cidd=x.data
	path_follow_stat=True

	print "we got our job",cidd
	
begin_sub=rospy.Subscriber("/begin_",Int16,Init_all)
if __name__ == '__main__':
	exiting=False
	if manual_op==1:
		cidd=201
		path_follow_stat=True


	while not rospy.is_shutdown():
		path_follow()
		rate.sleep()
