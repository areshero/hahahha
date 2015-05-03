'''
Created on Apr 29, 2015

@author: hehehehehe
'''

import numpy
import matplotlib
import os
matplotlib.use('Agg')
from scipy.cluster.vq import *
import pylab
pylab.close()

xy1=[[2,10],[2,5],[8,4],[5,8],[7,5],[6,4],[1,2],[4,9],[7,3],[1,3]]
xy2=numpy.array(xy1)

cluster_num=3
res, idx = kmeans2(numpy.array(zip(xy2[:,0],xy2[:,1])),cluster_num)

print "local centre points:\n",res

colors = ([([0.4,1,0.4],[1,0.4,0.4],[0.1,0.8,1])[i] for i in idx])
# plot colored points
pylab.scatter(xy2[:,0],xy2[:,1])

# mark centroids as (X)
pylab.scatter(res[:,0],res[:,1], marker='o', s = 500, linewidths=2, c='none')
pylab.scatter(res[:,0],res[:,1], marker='x', s = 500, linewidths=2)

#print os.getcwd()
pylab.savefig('pic.png')