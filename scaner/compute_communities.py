from pyorient.ogm import Graph, Config
import networkx as nx
import os
from subprocess import call
import pyorient
from celery.utils.log import get_task_logger
from collections import Counter

logger = get_task_logger(__name__)

ORIENTDB_HOST = os.environ.get('ORIENTDB_HOST')

client = pyorient.OrientDB(ORIENTDB_HOST, 2424)
session_id = client.connect("root", "root")
client.db_open("mixedemotions", "admin", "admin")



def execution():

	edges = []
	nodes = []
	for r in client.query('select  @rid from user limit -1'):
		nodes.append(str(r.oRecordData['rid']))
	
	for r in client.query('select from follows limit -1'):
		edges.append((str(r.oRecordData['out']), str(r.oRecordData['in'])))
	if edges and nodes:
		G = nx.Graph()
		G.add_nodes_from(nodes)
		G.add_edges_from(edges)
		nodes = G.nodes()


		import community

		partition = community.best_partition(G)
		c = Counter(partition.values())
		#partition2 = community.generate_dendrogram(G, part_init=None, weight='weight', resolution=1.0)
		#drawing
		#size = float(len(set(partition.values())))
		#pos = nx.spring_layout(G)
		#count = 0.
		#for com in set(partition.values()) :
		#    count += 1.
		#    list_nodes = [nodes for nodes in partition.keys()
		#                                if partition[nodes] == com]
		#    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
		#                            node_color = str(count / size))
		#nx.draw_networkx_edges(G,pos, alpha=0.5)
		try:
			client.command("delete edge Belongs_to_Community from (select from User) to (select from Community)")
			client.command("delete from Community UNSAFE")
		except:
			print("Primera ejecución")
		
		reg = []
		for item in partition:
		    if partition[item] not in reg:
		        client.command("insert into Community set id= {id}, user_count={user_count}".format(id=partition[item], user_count=c[partition[item]]))
		    client.command("update user set community = {community} where @rid = '{rid}'".format(community=partition[item], rid=item))
		    client.command("create edge Belongs_to_Community from (select from User where @rid = {rid}) to (select from Community where id = {id})".format(rid=item, id =partition[item]))
		    reg.append(partition[item])

		print("FINISH :::::TASK::::::")
	else:
		print("Error: You do not have a network between users in yout database")