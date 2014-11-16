# Explosound
# 15th November 2014
# see LICENSE for more information

"Creates a gexf valid file containing all files found in the specified folder as nodes, and random\
edges between them"

import sys
import os
from os import listdir
from os.path import isfile, join
import fnmatch
import random
from pymir import AudioFile
import matplotlib.pyplot as plt
import numpy as np
import fnmatch
import pickle as pkl
from sklearn import preprocessing as ppr


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

def get_features(job_list, force_rescan):
	print "get_features"
	if(force_rescan == True):
		print ">force_rescan on " + str(len(job_list)) + " jobs"
		analysed = 0
		audiofile_features = {}
		for i in range(len(job_list)):
			try:
				print "> " + str(i) + " / " + str(len(job_list)),
				audiofile = AudioFile.open(job_list[i])
				print ",s",
				spectrum = audiofile.spectrum()				
				rms = audiofile.rms()
				print ",rms",
				centroid = spectrum.centroid
				print ",centroid",
				flatness = -1
				try:
					flatness = str(spectrum.flatness())
					pass
				except:
					pass
				finally:
					pass

				print ",flatness",				
				features = [rms, centroid, flatness]
				print ",done!"
				audiofile_features[job_list[i]] = features
				analysed = analysed + 1
			except:
				#print "Exception: " + job_list[i]
				pass
			else:
				pass
			finally:
				pass	

		print "<force_rescan " + str(analysed) + "/" + str(len(job_list)) + " scanned."

		rms = []
		centroid = []
		flatness = []

		for i in audiofile_features.keys():
			rms.append(audiofile_features[i][0])
			centroid.append(audiofile_features[i][1])
			flatness.append(float(audiofile_features[i][2]))

		#serialisation avec pickle 
		with open('/Users/neogaldr/cluster/rms.pkl', 'wb') as f:
			pkl.dump(rms,f)
		with open('/Users/neogaldr/cluster/centroid.pkl', 'wb') as f:
			pkl.dump(centroid,f)
		with open('/Users/neogaldr/cluster/flatness.pkl', 'wb') as f:
			pkl.dump(flatness,f)
		with open('/Users/neogaldr/cluster/features.pkl', 'wb') as f:
			pkl.dump(audiofile_features,f)			

	#ouvrir un serialized
	with open('/Users/neogaldr/Developments/Explosound/Cluster/rms.pkl', 'rb') as f:
		rms = pkl.load(f)
	with open('/Users/neogaldr/Developments/Explosound/Cluster/centroid.pkl', 'rb') as f:
		centroid = pkl.load(f)
	with open('/Users/neogaldr/Developments/Explosound/Cluster/flatness.pkl', 'rb') as f:
		flatness = pkl.load(f)
	with open('/Users/neogaldr/Developments/Explosound/Cluster/features.pkl', 'rb') as f:
		features = pkl.load(f)

	#centrer et reduire
	rms = ppr.scale(rms)*100
	centroid = ppr.scale(centroid)*100
	flatness = ppr.scale(flatness)*100

	filtered_features = []

	for i in range(len(rms)):
		filtered_features.append([job_list[i], rms[i], centroid[i], flatness[i]])

	return filtered_features

def proximity_score(featureSet1, featureSet2):
	print "proximityScore random TODO"
	return random.uniform(0.5, 1) 

def get_similarity(features):
	similarity = []

	for id1 in range(0,len(features)):
		for id2 in range(id1,len(features) - 1):
			similarity.append(proximity_score(features[id1], features[id2]))

	return similarity




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
forceRescan = False

print "Hello =)"
print "Generating job list for folder " + folderPath
job_list = make_job_list(folderPath)
print "Generating similarity matrix"
features = get_features(job_list, forceRescan)

similarity = get_similarity(features)

print "____________________________"
print "Generating the resulting graph"
print ">nodes"
# Generate all nodes
node_list = []
id = 0
for feature in features:
	node_list.append(get_gexf_node(id, feature[0], 10, feature[2], feature[3], feature[1],\
		defaultR, defaultG, defaultB))
	id += 1

print ">edges"
# Generate all edges
edge_list = []
id = 0
for edge in similarity:
	#TODO
	print "TODO: make edge edge_list.append(get_gexf_edge(id, nodeId1, nodeId2, edgeDefaultProximity))\
			id+=1"

print ">gexf header and footer"
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
print "Saving generated gexf to ./part1.gexf"
save_to_file("part1.gexf", gexf_file)

print "Good bye !"
