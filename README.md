# JUGNU BOT - the shopping bot

&emsp;A shopping bot which can detect direction, follow path (between walls), detect items, pick and deliver items.


## Description

&emsp;A robot takes in the list of items to buy from the user using an Android Application. Processes the information and uses Aruco Markers for finding the direction and path to follow. Locates the item to be picked using the unique Arcuco Markers. Then, picks the item needed and deliver it to starting location.


## Components Used
*	Raspberry PI 3
*	Atmega2560
*	Arduino Uno
*	Cameras
*	IR Sensors
*	Ultrasonic Sensors
*	Magnetometer
*	Servo Motors
*	DC Motors
*	Motor Driver IC
*	Batteries

## Block Diagram

&emsp;The block digram of the entire process can be seen below:

<center>
    <img src="https://raw.githubusercontent.com/narendiran1996/jugnu_bot/master/jugnu_readme_src/block_diag.JPG" alt="BLOCK_DIAGRAM" width="500"/>
</center>


##  Major Modules
*	Android Application
*	Aruco Markers
*	Sensor Measurement
*	Navigation
*	Arm Control
*	Item Detection
*	Item Picking
*	Item Delivery



### Android Application
&emsp;An android app is used to select the items to get and provide the item ids to the PC via Socket connection. 

<center>
    <img src="https://raw.githubusercontent.com/narendiran1996/jugnu_bot/master/jugnu_readme_src/app_screen.jpg" alt="ANDROID_APP_SCREENSHOT" width="250"/>
</center>

The socket connection to the PC with the snippet for receiving,

<center>
    <img src="https://raw.githubusercontent.com/narendiran1996/jugnu_bot/master/jugnu_readme_src/ando_pc.png" alt="SOCKET CONNECTION" width="350"/>
</center>
<center>
    <img src="https://raw.githubusercontent.com/narendiran1996/jugnu_bot/master/jugnu_readme_src/code_ser_snip.JPG" alt="SERVER_SNIPPET" width="550"/>                        
</center>


### Aruco Markers
&emsp;Aruco Marks are used for finding the direction and the items.

<center>
<img src="https://raw.githubusercontent.com/narendiran1996/jugnu_bot/master/jugnu_readme_src/aruco_git.png" alt="ARUCO_JUNCTION" width="350"/>   
 </center>

&emsp;Here, an example of direction detection is given. If the item we ordered is Chocolate the robot goes to the left, if it’s box then the robot goes to the right. This is done throughout the shop for direction detection.

<center>
<img src="https://raw.githubusercontent.com/narendiran1996/jugnu_bot/master/jugnu_readme_src/aucod_dd.png" alt="ARUCO_SIGN_BOARD" width="350"/>   
</center>


### Aruco Detection
&emsp;The detection of aruco is done using the code available in [Aruco Detection](https://github.com/narendiran1996/aruco_detection).



### Sensor Measurement
	
&emsp;The sensors used are listed below:


1. Ultrasonic Sensor (HC-SR04)
2. Magnetometer Sensor (HMC5883L)
3. IR Sensor

* Ultrasonic Sensor is used in Path following during navigation.(to find the distance from the walls)
* Magnetometer Sensor is used for turning the robot to the desired angle.
* IR Sensors is used to detect the presence of an item (each item consist of a black line to indicate its presence)
	
The Measurement is done using Atmega2560 using standard libraries for each sensors and the values are published to ROS master in topic /dist.



### Arm control
&emsp;Four Servo Motors are used for building the arm. It can be as
*	The Base - turning clockwise and anticlockwise
*	The Wrist - for making angular/altitudinal changes.
*	The Grip - to hold the item.

#### The Base
&emsp;&emsp;It has a single Servo Motor for turing the arm both in anticlockwise and clockwise direction. 
		
#### The Wrist
&emsp;&emsp;It has two Servo Motor for changing the height and position of The Grip.
		
#### The Grip
&emsp;&emsp;A gripper with Servo Motors is used to hold the items


### Navigation
Autonomous Navigation involves the use of camera and sensors(Ultrasonic). It involves:

*	Path following – uses Ultrasonic Sensors
*	Direction Identification – uses Camera

#### Path Following

*	Ultrasonic Sensor attached to the bot on both sides(right and left) gives us distance from the walls of the shop.
*	The bot follows the path using the distances by maintaining a particular distance(threshold value) from the wall. We adjust the speed for controlling the robot.
*	The snippet used is shown:

![PATH_FOLLOWING_SNIPPET](https://raw.githubusercontent.com/narendiran1996/jugnu_bot/master/jugnu_readme_src/code_path_fol.JPG)
 
*	In case if the distance of separation between is decreased, it compensates by moving (by velocity changing) in the opposite direction such the separation becomes the threshold distance.

![PATH_FOLLOW_1](https://raw.githubusercontent.com/narendiran1996/jugnu_bot/master/jugnu_readme_src/dir.png)
 
*	In case a corner is encountered, it uses the ultrasonic sensor to find which has more distance and turn in that particular direction.

![PATH_FOLLOW_2](https://raw.githubusercontent.com/narendiran1996/jugnu_bot/master/jugnu_readme_src/dir_cor.png)
 
### Direction Identification
*	While traversing the shop, there would be confusion on which direction to go in case of a junction being encountered.
*	We have used Aruco based sign boards.
*	Each item(can be modified to category in future) is assigned an id and its’ Aruco Marker is used.
*	The direction of the particular item is also encoded in different Aruco Marker.
*	These two Markers are placed aside to indicate the items’ direction.
sign_board = {item_i_1 : direction, item_id_2 : direction, . . . , item_id_n : direction}

				
## Item Detection
*	Here as stated a Aruco markers is assigned for every item and they are pasted these markers below the items. A Black line is 	placed on the floor for each items.
*	Using IR Sensors these black lines are detected and the bot is then stopped.
*	Then we perform Aruco detection using the Side camera/cameras.
*	If the Marker Id matches with our needed marked id, we pick the item, else we just move on.

![ITEM_DETECTION](https://raw.githubusercontent.com/narendiran1996/jugnu_bot/master/jugnu_readme_src/arucod_item_Det.png)

## Item Delivery
&emsp;Once the Item has been picked, the marker id changes to the exit marker id(here #200) and the robot goes to the exit and drops the item.

# Results
&emsp;The final output robot is shown below


<center>
<img src="https://raw.githubusercontent.com/narendiran1996/jugnu_bot/master/jugnu_readme_src/IMG_20170802_070108.jpg" alt="BOT_1" width="250"/>   
<img src="https://raw.githubusercontent.com/narendiran1996/jugnu_bot/master/jugnu_readme_src/IMG_20170802_070023.jpg" alt="BOT_2" width="250"/>   
</center>

The Youtube Video showing the demo can be seen below:

[![VIDEO LINK](http://img.youtube.com/vi/6H3P8CFzQXI/0.jpg)](http://www.youtube.com/watch?v=6H3P8CFzQXI)


