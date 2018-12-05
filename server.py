
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
		for i in range(1):
			self.bots.append(bot.bot(i,i))						
								


	def update(self):

		self.bots[0].printState()

	

if __name__ == '__main__':
	
	Server=server()
	Server.update()
	
	while not rospy.is_shutdown():
		rospy.spin()
