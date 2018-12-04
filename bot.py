import rospy
import nav_msgs.msg
import geometry_msgs.msg
import sensor_msgs.msg

class bot (object):
	
	def __init__(self, id_, priority):
		self.id=id_
		self.name="/robot_"+str(id_)
		self.priority=priority

		self.present_pos=(0,0)
		self.target_pos=(0,0)
		self.dir=(0,0)

		self.odom_t= self.name+"/odom"
		self.cmd_vel_t=self.name+"/cmd_vel"
		self.base_scan_t=self.name+ "/base_scan"
		self.target_t= self.name + "/target" 
	
		self.odom=rospy.Subscriber(self.odom_t,nav_msgs.msg.Odometry,self.updateOdom,queue_size=10) #queue size?
		self.cmd_vel=rospy.Publisher(self.cmd_vel_t, geometry_msgs.msg.Twist,queue_size=10)
		self.base_scan_t=rospy.Subscriber(self.base_scan_t, sensor_msgs.msg.LaserScan, self.updateScan,queue_size=10)
		self.target=rospy.Subscriber(self.target_t, geometry_msgs.msg.Point, self.updateTarget, queue_size=10)
		self.isColliding=False
		
			
	def printState(self):
		print(self.id)

	def updateOdom(self,msg):
		return

	def updateScan(self,msg):
		return
	
	def updateTarget(self,msg):
		return

	def update(self):
		return
