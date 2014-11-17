from pymir import AudioFile
import matplotlib.pyplot as plt
import os
from os import listdir
from os.path import isfile, join
import seaborn as sb
import numpy as np
import fnmatch
import pickle as pkl

def make_job_list(folderPath) :
    job_list = []
    for root, directories, filenames in os.walk(folderPath):
        for filename in filenames:
            path = os.path.join(root,filename)
            if fnmatch.fnmatch(filename, '*.wav'):
                job_list.append(str(path))

    return job_list

job_list = make_job_list('/Users/kamal/Developpement/Explosound/features_extraction_/ExplosoundSamples-master')


analyzed = 0
audiofile_features = {}
for i in range(30):
	try:
		audiofile = AudioFile.open(job_list[i])
		spectrum = audiofile.spectrum()
		features = [audiofile.rms(), spectrum.centroid(), str(spectrum.flatness())]
		audiofile_features[job_list[i]] = features
	except:
		pass
	else:
		pass
	finally:
		pass	

rms = []
centroid = []
flatness = []

for i in audiofile_features.keys():
	rms.append(audiofile_features[i][0])
	centroid.append(audiofile_features[i][1])
	flatness.append(float(audiofile_features[i][2]))

#serialisation avec pickle 
with open('/Users/kamal/Developpement/Explosound/features_extraction_/rms.pkl', 'wb') as f:
	pkl.dump(rms,f)
with open('/Users/kamal/Developpement/Explosound/features_extraction_/centroid.pkl', 'wb') as f:
	pkl.dump(rms,f)
with open('/Users/kamal/Developpement/Explosound/features_extraction_/flatness.pkl', 'wb') as f:
	pkl.dump(rms,f)

#ouvrir un serializé 
with open('/Users/kamal/Developpement/Explosound/features_extraction_/rms.pkl', 'rb') as f:
	my_list = pkl.load(f)


bins = 7
plt.hist(rms, 16)
plt.show()
plt.hist(centroid, bins)
plt.show()
plt.hist(flatness, bins)
plt.show()


#traitement : éventuelle division par l'écart type 
#traitement possible aussi : centrer réduire le centroid 


