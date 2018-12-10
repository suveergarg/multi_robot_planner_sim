import rospy
import nav_msgs.msg
import geometry_msgs.msg
import sensor_msgs.msg
import bot 
import graph
import networkx as nx
import matplotlib.pyplot as plt
import pygraphviz as pgv

class server(object):

	def __init__(self):
		
		self.bots=[]
		self.G=graph.create_graph()
		rospy.init_node("Central_Server",anonymous=True)
		self.target=[65,72,18,40,90,54]
		self.present = [12,22,32,42,52,62]
		self.previous = [13,21,33,41,53,61]
		for i in range(6):
			self.bots.append(bot.bot(i,self.target[i],self.present[i],self.previous[i]))						
								
	def update(self):
		for i in range(6):
			self.bots[i].update(self.G.successors(self.bots[i].getPresentNode()))
	

if __name__ == '__main__':
	
	Server=server()
	
	
	while not rospy.is_shutdown():
		Server.update()
		#rospy.spin()
