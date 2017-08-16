#include <Servo.h>
#include <ros.h>
#include <geometry_msgs/Vector3.h>
#include "my_servo.h"
#include <std_msgs/Int16.h>
ros::NodeHandle  nh;

std_msgs::Int16 arm_over_msg;
ros::Publisher arm_over("/arm_over", &arm_over_msg);


float sp1,sp2;


void set_speed(float x,float y)
{
   analogWrite(3,abs(x));
      analogWrite(11,abs(y));
   
}

void velocity_obt(const geometry_msgs::Vector3& a)
{
   sp1=a.x;
   sp2=a.y;
    set_speed(sp1,sp2); 
}
ros::Subscriber<geometry_msgs::Vector3> sub("/vel", &velocity_obt );

my_servo arm1,arm2,grip,base;
Servo x;
void arm(int ang)
{
   int acang=arm1.get_cang();
   
   if(ang>=acang)
    {
      for(int i=acang;i<=ang;i++)
      {
        arm1.servo_write(i);
        arm2.servo_write(i);
        delay(25);
      }
    }
    else if(ang<acang)
    {
      for(int i=acang;i>=ang;i--)
      {
        arm1.servo_write(i);
        arm2.servo_write(i);
        delay(25);
      }
    }
}

void attach_servos()
{
  arm2.att(9);
  arm1.att(10); 
  grip.att(5);
  base.att(6);
  
 arm1.servo_write(0);
arm1.servo_write(0);
grip.servo_write(90);
base.servo_write(0);

arm(45);
 
}
void detach_servos()
{
   arm1.dett();
  arm2.dett();
  grip.dett();
  base.dett(); 
  
}
void messageCb( const std_msgs::Int16& toggle_msg)
{

 if(toggle_msg.data==0)
 {
  attach_servos();  
 
  arm(45);
 

  grip.move_in_steps(0,20);
 

  base.move_in_steps(60,20);  
 
  
 
   arm(25);
  //delay(2000);

  grip.move_in_steps(80,20);
  //delay(2000);  


   arm(45);
   base.move_in_steps(0,20); 

  
   arm_over_msg.data=123;
    int i=0;
   while(i<10)
   {
      arm_over.publish(&arm_over_msg);
      i++;
   }

 }
 if(toggle_msg.data==1) 
 {

   arm(0);
   
   grip.move_in_steps(0,20);
   grip.move_in_steps(90,20);

    arm(45);
    
 arm_over_msg.data=123;

     int i=0;
   while(i<10)
   {
      arm_over.publish(&arm_over_msg);
      i++;
   }
   
   
  detach_servos();

 }
 
}
ros::Subscriber<std_msgs::Int16> arm_c("/toggle_led", &messageCb );
void setup() 
{
  sp1=sp2=0.0;
  pinMode(3, OUTPUT);
  pinMode(9, OUTPUT);

  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  
  
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);



  analogWrite(3,0);
      analogWrite(11,0);
      
    nh.initNode();
    nh.subscribe(sub);
   nh.subscribe(arm_c);

    nh.advertise(arm_over);
  
}

void loop() 
{
  nh.spinOnce();
  delay(1);
}
