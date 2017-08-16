#!/usr/bin/env python

import rospy
from std_msgs.msg import Int16

import socket            
import netifaces as ni

bpub = rospy.Publisher('/begin_', Int16, queue_size=10)
rospy.init_node('server_android_info', anonymous=True)
rate = rospy.Rate(10)


ni.ifaddresses('eth0')
ipa = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
host =ipa
port = 12345
s = socket.socket()
print host+"  -  "+str(port)
s.bind((host, port))

items={'[CHOCOLATE]':201,'[BOX]':202,'CANCEL':0,'[]':0}

try:
	while True:
		s.listen(1)     
		c, addr = s.accept() 
		#print 'Got connection from', addr
		data = c.recv(8192)
		ax=items[data]
		print ax
		if ax!=0:
			bpub.publish(ax)
		c.close()       
		
except:
	s.close()
