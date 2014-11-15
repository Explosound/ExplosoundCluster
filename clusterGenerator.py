# Explosound
# 15th November 2014
# see LICENSE for more information

"Creates a gexf valid file containing all files found in the specified folder as nodes, and random\
edges between them"

import sys
import os
import fnmatch
import random

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)
#print 'Folder =', str(sys.argv[1])

# Make the job list

# Creates a list of all wav files found in all folders
# recursively
def make_job_list(folderPath) :
	job_list = []
	for root, directories, filenames in os.walk(folderPath):
		for filename in filenames:
			path = os.path.join(root,filename)
			if fnmatch.fnmatch(filename, '*.wav'):
				job_list.append(str(path))

	return job_list

def get_gexf_header():
	return "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\
	<gexf xmlns=\"http://www.gexf.net/1.2draft\" version=\"1.2\" xmlns:viz=\"http://www.gexf.net/1.2draft/viz\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd\">\
	  <meta lastmodifieddate=\"2014-10-05\">\
	    <creator>Gephi 0.8.1</creator>\
	    <description></description>\
	  </meta>\
	  <graph defaultedgetype=\"undirected\" mode=\"static\">\
	    <attributes class=\"node\" mode=\"static\">\
	      <attribute id=\"modularity_class\" title=\"Modularity Class\" type=\"integer\"></attribute>\
	    </attributes>"

def get_gexf_footer():
	return "  </graph>\
</gexf>"

def get_gexf_node(id, filePath, size, x, y, z, r, g, b):
	return "<node id=\""+str(id)+ "\" label=\"" + str(filePath) + "\">\
        <attvalues>\
          <attvalue for=\"modularity_class\" value=\"0\"></attvalue>\
        </attvalues>\
        <viz:size value=\"" +str(size)+ "\"></viz:size>\
        <viz:position x=\""+str(x)+"\" y=\""+str(y)+"\" z=\""+str(z)+"\"></viz:position>\
        <viz:color r=\""+str(r)+"\" g=\""+str(g)+"\" b=\""+str(b)+"\"></viz:color>\
      </node>"

def get_gexf_edge(id, source, target, proximity):
	return "<edge id=\""+str(id)+"\" source=\""+str(source)+"\" target=\""+ str(target) + "\" weight=\""+ str(proximity) + "\"/>"

def save_to_file(filePath, gexfToSave):
	text_file = open(filePath, "w")
	text_file.write(gexfToSave)
	text_file.close()

nodes = "<nodes>" + get_gexf_node(0, "/test/file", 30, 0,0,0, 90, 90, 255) + get_gexf_node(1, "/toto/file", 30, -50,0,0, 200,90,90) + "</nodes>"
edges = "<edges>" + get_gexf_edge(0, 0, 1, 1) + "</edges>"

gexf_file = get_gexf_header() + nodes + edges + get_gexf_footer()

save_to_file("output.gexf", gexf_file)

#MAIN ======================================================================================
folderPath = sys.argv[1]
defaultSize = 10
defaultR = 153
defaultG = 153
defaultB = 153
minX = -500
maxX = 500
minY = -500
maxY = 500
minZ = -10
maxZ = 10
edgeCreationProbability = 0.0013
edgeDefaultProximity = 1

# Generate all nodes
node_list = []
id = 0
for job in make_job_list(folderPath):
	node_list.append(get_gexf_node(id, job, 10, random.uniform(minX, maxX), random.uniform(minY, maxY), random.uniform(minZ, maxZ),\
		defaultR, defaultG, defaultB))
	id += 1


# Generate all edges
edge_list = []
id = 0
for nodeId1 in range(0, len(node_list)):
	for nodeId2 in range(0, len(node_list)):
		if(random.uniform(0, 1) < edgeCreationProbability):
			edge_list.append(get_gexf_edge(id, nodeId1, nodeId2, edgeDefaultProximity))
			id+=1


# Generate the gexf
gexf_file = get_gexf_header()

gexf_file += "<nodes>"
for node in node_list:
	gexf_file += node
gexf_file += "</nodes>"

gexf_file += "<edges>"
for edge in edge_list:
	gexf_file += edge
gexf_file += "</edges>"

gexf_file += get_gexf_footer()

# Export result
save_to_file("part1.gexf", gexf_file)
