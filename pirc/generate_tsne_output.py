# Test siamese network for pill recognition. Loads images from a list file
#  and compare the results of passing those images through the network. Matching pairs
#  should have responses that are close together.
# Adam Allevato
# April 12, 2016

# load all the things
import numpy as np
from scipy import misc
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# point to dinesh's caffe install on the Maverick supercomputer because I'm too lazy 
# to build my own
caffe_root = '/work/01932/dineshj/caffe/'
import sys
sys.path.insert(0, caffe_root + 'python')
import caffe

import math
import csv
import copy
# check command line arguments=
if len(sys.argv) < 4:
	print 'usage is test_pirc_siamese.py model weights.caffemodel output.csv path_to_file_with_input_image_paths'

model = sys.argv[1]
pretrained = sys.argv[2]
output_path = sys.argv[3]
input_file_path = sys.argv[4]

MAX_IMGS = 100

# initialize input image array
labels = []
result = []
rank_matrix = []
rank_matrix.append([''])

caffe.set_mode_gpu()
net = caffe.Net(model, pretrained, caffe.TEST)

transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,1,0))

net.blobs['data'].reshape(1, 3, 227, 227)
net.reshape()
# now loop over input images

tsne_output = []

# read the image paths from the file
input_file = open(input_file_path, 'r')
input_file_lines = input_file.read().splitlines()
for i,input_item in enumerate(input_file_lines):
	tokens = input_item.split(' ')
	if len(tokens) == 1 or tokens[1] == '1':
		if i%100 == 0:
			print 'processing input image ' + str(i) + '/' + str(len(input_file_lines)) + ': '  + tokens[0]
		img = misc.imread(tokens[0])
		img = misc.imresize(img, (227, 227))
	
		input_data = transformer.preprocess('data', img)
	
		input_data_np = np.array(input_data)
		net.blobs['data'].data[...] = input_data_np
		
		output = net.forward()
		input_result = output['feat'][0]

		tsne_output.append(copy.deepcopy(input_result))

with open(output_path, 'w') as tsne_file:
	for line in tsne_output:
		tsne_file.write(','.join([str(i) for i in [j for j in line]])+'\n')
