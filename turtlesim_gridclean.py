#!/usr/bin/env python3

import rospy
from std_msgs.msg import *
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import time
import math


def PosCallBack(posi):  #Defining CallBack Function
	global x1, y1, theta1
	
	x1=posi.x
	y1=posi.y
	theta1=posi.theta


def Move(speed, dist, is_forward): 

	vel=Twist()
	x2=x1
	y2=y1

	if is_forward:
		vel.linear.x=abs(speed)
	else:
		vel.linear.x=-abs(speed)

	dist_moved=0
	rate=rospy.Rate(10)
	cmd_vel= '/turtle1/cmd_vel'
	pub=rospy.Publisher(cmd_vel, Twist, queue_size=10)

	current_dist=0

	while current_dist<dist:  #Loop to ensure stream of commands until the bot travels the dist
		pub.publish(vel)
		current_dist=(math.sqrt((x2-x1)**2)+((y2-y1)**2)) #Using Mathematical Distance Formula
		print(f"Moving Distance: {dist}")
	
	vel.linear.x=0
	print("Distance Reached")
	pub.publish(vel)



def Rotate(ang_speed_deg, rel_ang_deg, clockwise):
	vel=Twist()

	vel.linear.x=0
	vel.linear.y=0
	vel.linear.z=0

	vel.angular.x=0
	vel.angular.y=0
	vel.angular.z=0

	theta2=theta1
	ang_speed=math.radians(abs(ang_speed_deg))

	if (clockwise):
		vel.angular.z=-abs(ang_speed)
	else:
		vel.angular.z=abs(ang_speed)

	ang_moved=0
	rate=rospy.Rate(10)
	cmd_vel= '/turtle1/cmd_vel'
	pub=rospy.Publisher(cmd_vel, Twist, queue_size=10)

	t0=rospy.Time.now().to_sec()

	while True:		#Loop to ensure stream of commands until desired angle has been rotated through
		vel.linear.x=0
		rospy.loginfo(f"Turtle rotating by {rel_ang_deg}")
		pub.publish(vel)

		t1=rospy.Time.now().to_sec()
		curr_ang_deg=(t1-t0)*ang_speed_deg

		if curr_ang_deg>=rel_ang_deg:
			rospy.loginfo(f"Rotated {rel_ang_deg}")
			break

	vel.angular.z=0
	pub.publish(vel)



def GoToGoal(go_x, go_y):

	vel=Twist()
	cmd_vel= '/turtle1/cmd_vel'
	pub=rospy.Publisher(cmd_vel, Twist, queue_size=10)

	while True:
		k_lin=0.5

		dist= abs(math.sqrt(((go_x-x1)**2)+(go_y-y1)**2))  #Using Mathematical Distance Formula

		lin_speed=dist*k_lin  #Making linear speed a funtion of distance

		k_ang=4
		des_ang_go=math.atan2(go_y-y1, go_x-x1)  #Taking Tangent inverse to get the angle

		ang_speed=(des_ang_go-theta1)*k_ang  #Making angular speed a function of angle

		vel.linear.x=lin_speed
		vel.angular.z=ang_speed

		
		pub.publish(vel)

		if dist<0.01:  #To stop rotation after reaching the angle
			break

def SetDesOrient(des_ang_rad):  #Set Desired Orientation

	rel_ang_rad=des_ang_rad-theta1
	print(f"theta1 is {theta1}")

	if rel_ang_rad<0:
		clockwise=1
	else:
		clockwise=0
	


	Rotate(30, math.degrees(abs(rel_ang_rad)), clockwise)
	print(f"Orientation set to {math.degrees(abs(rel_ang_rad))}")

	
def GridClean():  #The Function To clean Grid
	des_pose= Pose()
	des_pose.x=1
	des_pose.y=1
	des_pose.theta=0

	GoToGoal(des_pose.x, des_pose.y)
	SetDesOrient(math.radians(des_pose.theta))
	print("Cleaning Grid")
	Move(5, 9, 1)
	Rotate(50, 90, 0)
	Move(1, 1, 1)
	Rotate(50, 90, 0)
	Move(5, 9, 1)
	Rotate(50, 90, 1)
	Move(2, 1, 1)
	Rotate(50, 90, 1)
	Move(5, 9, 1)
	Rotate(50, 90, 0)
	Move(2, 1, 1)
	Rotate(50, 90, 0)
	Move(5, 9, 1)
	Rotate(50, 90, 1)
	Move(2, 1, 1)
	Rotate(50, 90, 1)
	Move(5, 9, 1)
	Rotate(50, 90, 0)
	Move(2, 1, 1)
	Rotate(50, 90, 0)
	Move(5, 9, 1)
	Rotate(50, 90, 1)
	Move(2, 1, 1)
	Rotate(50, 90, 1)
	Move(5, 9, 1)
	Rotate(50, 90, 0)
	Move(2, 1, 1)
	Rotate(50, 90, 0)
	Move(5, 9, 1)
	Rotate(50, 90, 1)
	Move(2, 1, 1)
	Rotate(50, 90, 1)
	Move(5, 9, 1)
	Rotate(50, 90, 0)
	Move(2, 1, 1)
	Rotate(50, 90, 0)
	Move(5, 9, 1)
	print("Grid Cleaned!")


if __name__=='__main__':
	try:

		rospy.init_node('turt_motion', anonymous=True)	   #Initialising Node
		cmd_vel= '/turtle1/cmd_vel'						   
		pub=rospy.Publisher(cmd_vel, Twist, queue_size=10) #Defining Publisher

		pos= '/turtle1/pose'
		posi=Pose()
		sub=rospy.Subscriber(pos, Pose, PosCallBack)	   #Defining Subscriber
		
		time.sleep(2) #Sleep for 2 seconds

		GridClean()
		print("DONE!")


	except rospy.ROSInterruptException: 
		rospy.loginfo("Node terminated")
		pass