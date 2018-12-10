import rospy
import nav_msgs.msg
import geometry_msgs.msg
import sensor_msgs.msg
import tf
import math

class bot (object):
	
	def __init__(self, id_, target,present,previous):
		self.id = id_
		self.name = "/robot_"+str(id_)
		self.priority = 0

		self.present_pos = (0,0)
		self.target_pos = (5,5)
		self.present_dir = 1.57
		self.target_dir=0

		self.odom_t = self.name+"/odom"
		self.cmd_vel_t = self.name+"/cmd_vel"
		self.base_scan_t = self.name+ "/base_scan"
		self.target_t = self.name + "/target" 
	
		self.odom = rospy.Subscriber(self.odom_t,nav_msgs.msg.Odometry,self.updatePresentState,queue_size=10) #queue size?
		self.cmd_vel = rospy.Publisher(self.cmd_vel_t, geometry_msgs.msg.Twist,queue_size=10)
		self.base_scan_t = rospy.Subscriber(self.base_scan_t, sensor_msgs.msg.LaserScan, self.updateScan,queue_size=10)
		self.target = rospy.Subscriber(self.target_t, geometry_msgs.msg.Point, self.updateTarget, queue_size=10)
		self.isColliding = False
		self.fluctuationLaser = False
		
		self.discrete_position = (2,2)
		self.previous_node= previous
		self.present_node = present
		self.next_node= 0
		self.target_node=target
		self.isFirst = True

	def printState(self):
		print(self.id)
		return

	def updatePresentState(self,msg):
		
		self.present_pos = (msg.pose.pose.position.x,msg.pose.pose.position.y)
		quaternion =	(msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,msg.pose.pose.orientation.z,msg.pose.pose.orientation.w)
		euler = tf.transformations.euler_from_quaternion(quaternion)
		self.present_dir = euler[2]
		self.descritize()
		#print("direction:(",euler[0],euler[1],euler[2],")  Position:",self.present_pos)

 	def updateScan(self,msg):

 		ranges = msg.ranges
 		minimum = min(ranges)
 		self.fluctuationLaser+=1
 		self.fluctuationLaser=self.fluctuationLaser%2
  		if self.fluctuationLaser == 0:
  			if minimum < 0.4 :
 				self.isColliding = True
 			else: 
 				self.isColliding = False
 			
		#print("robot isColliding: ",self.isColliding)
	
	def updateTarget(self,msg):
		
		self.target_pos = (msg.x,msg.y)
		self.target_node = msg.x *10 +msg.y

	def stop(self):
		
		msg=geometry_msgs.msg.Twist()
		msg.linear.x = 0
		msg.linear.y = 0
		msg.angular.z = 0
		self.cmd_vel.publish(msg)

	def descritize(self): 
		self.discrete_position = (math.floor(self.present_pos[0]),math.floor(self.present_pos[1])) 
		
	def getPresentNode(self):
		return self.present_node

	def assignDir(self):

		if(abs(self.present_dir)<=0.2):
			if(self.next_node-self.present_node>0):
				self.target_dir=1.57
				self.priority=0
			else:
				self.target_dir=-1.57
				self.priority=0

		elif(abs(self.present_dir)-1.57)<=0.2 and self.present_dir>0:
			if(self.next_node-self.present_node>0):
				self.target_dir=0
				self.priority=1
			else:
				self.target_dir=3.14
				self.priority=1

		elif(abs(self.present_dir)-3.14)<=0.2:
			if(self.next_node-self.present_node>0):
				self.target_dir=1.57
				self.priority=0
			else:
				self.target_dir=--1.57
				self.priority=0

		elif(abs(self.present_dir)-1.57)<=0.2 and self.present_dir<0:
			if(self.next_node-self.present_node>0):
				self.target_dir=0
				self.priority=1
			else:
				self.target_dir=3.14
				self.priority=1
		self.isFirst=False		
		#print(self.target_dir)
		#print(self.present_dir)

	def update(self,successor):
 		
		msg=geometry_msgs.msg.Twist()

		#debug
		#print("target_dir:", self.target_dir)
		#print("present_dir:", self.present_dir)

		succ = list()
		for s in successor:
			succ.append(s)

		

		if(len(succ)>1 and abs(self.target_node-succ[0])>abs(self.target_node-succ[1])):
			self.next_node = succ[1]
		else:
			self.next_node = succ[0]

		if self.present_node==self.target_node:
			print("reached")

		elif self.isColliding and self.priority==0:
			self.stop()
		
		
		elif abs(round(self.target_dir-self.present_dir,2)) > 0.01 and not self.isFirst:

			if(round(self.target_dir,2)>round(self.present_dir,2)):
				msg.angular.z=0.1
				msg.linear.x=0
				print("Turn Left")
			else:
				msg.angular.z=-0.1
				msg.linear.x=0
				print("Turn Right") 		
			
		else :
			print("next_node:",self.next_node)
			print("present_node:",self.present_node)
			print("previous_node:",self.previous_node)
			msg.angular.z=0
			if(abs(self.next_node-self.present_node)==abs(self.present_node-self.previous_node)):
				msg.linear.x=0.1
				print("Forward")
			else:
				self.assignDir()
				self.previous_node=self.present_node-(self.next_node-self.present_node)
			
		self.cmd_vel.publish(msg)

		#print("Discrete_node:",(self.discrete_position[0]-1)*10+self.discrete_position[1])
		
		if self.present_node != int((self.discrete_position[0]-1)*10+self.discrete_position[1]):
			self.previous_node=self.present_node
			self.present_node= int((self.discrete_position[0]-1)*10+self.discrete_position[1])
	