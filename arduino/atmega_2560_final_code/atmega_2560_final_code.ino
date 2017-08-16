#include <ros.h>
#include <Servo.h>
#include <Wire.h> 
#include <geometry_msgs/Twist.h>

#include "ultra_sonic.h"
#include "magneto_.h"

ros::NodeHandle  nh;



geometry_msgs::Twist dist_msg;
ros::Publisher dist("/dist",&dist_msg);

ultra_sonic f1(37,36);
ultra_sonic f2(35,34);

void setup()
{
  setup_mag();
  
  nh.initNode();
  
  nh.advertise(dist);

}

long interval = 100;
long previousMillis=0;
void loop()
{ 
    
  unsigned long currentMillis = millis();
  if(currentMillis - previousMillis > interval) 
  { 
    loop_mag();
    previousMillis = currentMillis;
    loop_mag();
    dist_msg.linear.x =f1.get_dist_mm();
    dist_msg.linear.y =f2.get_dist_mm();
    dist_msg.linear.z =heading_in_degrees;
    dist_msg.angular.x =0;
    dist_msg.angular.y =analogRead(A1);
    dist_msg.angular.z =0;
    dist.publish( &dist_msg );
    
  } 
    nh.spinOnce();
  delay(1);

}

