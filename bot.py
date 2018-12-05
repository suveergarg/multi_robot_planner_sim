import rospy
import nav_msgs.msg
import geometry_msgs.msg
import sensor_msgs.msg
import tf

class bot (object):
	
	def __init__(self, id_, priority):
		self.id=id_
		self.name="/robot_"+str(id_)
		self.priority=priority

		self.present_pos=(0,0)
		self.target_pos=(0,0)
		self.present_dir=0

		self.odom_t= self.name+"/odom"
		self.cmd_vel_t=self.name+"/cmd_vel"
		self.base_scan_t=self.name+ "/base_scan"
		self.target_t= self.name + "/target" 
	
		self.odom=rospy.Subscriber(self.odom_t,nav_msgs.msg.Odometry,self.updatePresentState,queue_size=10) #queue size?
		self.cmd_vel=rospy.Publisher(self.cmd_vel_t, geometry_msgs.msg.Twist,queue_size=10)
		self.base_scan_t=rospy.Subscriber(self.base_scan_t, sensor_msgs.msg.LaserScan, self.updateScan,queue_size=10)
		self.target=rospy.Subscriber(self.target_t, geometry_msgs.msg.Point, self.updateTarget, queue_size=10)
		self.isColliding= False
		self.fluctuationLaser = False
		
		self.discrete_position = (0,0)
		self.discrete_direction = 0
		self.node=0

	def printState(self):
		print(self.id)
		return

	def updatePresentState(self,msg):
		
		self.present_pos = (msg.pose.pose.position.x,msg.pose.pose.position.y)
		quaternion=(msg.pose.pose.orientation.x,msg.pose.pose.orientation.y,msg.pose.pose.orientation.z,msg.pose.pose.orientation.w)
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

	def stop(self):
		
		msg=geometry_msgs.msg.Twist()
		
		msg.linear.x = 0
		msg.linear.y = 0
		msg.angular.z = 0

		self.cmd_vel.publish(msg)

	def descritize(self):

		round_pose_x = ((round(self.present_pos[0],3)*1000)%1000)
		round_pose_y = ((round(self.present_pos[1],3)1000)%1000)
		round_dir = round(self.dir,2)

		if round_pose_x>990 or round_pose_x<10: 
			discrete_position[0] = round(present_pos[0])

		if round_pose_y>990 or round_pose_y<10: 
			discrete_position[1] = round(present_pos[1]) 

	def getPresentNode(self):
		return self.node


	def update(self,successor):
 	
		msg=geometry_msgs.msg.Twist()

		if self.isColliding:
			self.stop()

		else:

			x_remaining = self.target_pos[0] - self.discrete_position[0]
			y_remaining = self.target_pos[1] - self.discrete_position[1]

			self.node=(self.discrete_position[0]-1)*10+self.discrete_position[1]

			if y_remaining > 0 and round(self.dir,2) == 1.57 :                            #step up
				msg.linear.x = 1
				msg.angular.z = 0

			elif y_remaining > 0 and round(self.dir,2) == 1.57 : 	
				msg.linear.x = 0
				msg.angular.z = 1

			elif y_remaining < 0:
		



