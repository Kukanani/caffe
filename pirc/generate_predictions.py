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
	print 'usage is test_pirc_siamese.py model weights.caffemodel output.csv path_to_file_with_reference_image_paths path_to_file_with_input_image_paths'

model = sys.argv[1]
pretrained = sys.argv[2]
output_path = sys.argv[3]
input_file_path = sys.argv[5]
list_file_path = sys.argv[4]

MAX_IMGS = 700

# initialize input image array
labels = []
result = []
rank_matrix = []
rank_matrix.append([''])

caffe.set_mode_gpu()
net = caffe.Net(model, pretrained, caffe.TEST)

transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,1,0))

input_img_names = []
print 'processing reference file ' + list_file_path
# read the image paths from the file
list_file = open(list_file_path, 'r')
list_file_lines = list_file.read().splitlines()

img_index = 0
while img_index < len(list_file_lines):
	img_count = 0
	input_imgs = []
	while img_count < MAX_IMGS and img_index < len(list_file_lines):
		line = list_file_lines[img_index]
        	
		# put all the images into a single input array which will then be passed
		# through the network all at once. N images will be stored in an array
		# of size N x 3 x 227 x 227. This is N images with 3 channels (RGB) that
		# are 227x227 pixels
        	tokens = line.split(' ')
		if tokens[1] == '1' and tokens[0] not in input_img_names:
			img_count = img_count + 1
			input_img_names.append(tokens[0])
			img = misc.imread(tokens[0])
			img = misc.imresize(img, (227, 227))
			input_imgs.append(img)
			#labels.append(int(tokens[1]))
			rank_matrix[0].append(tokens[0].split('/')[-1])
		img_index = img_index + 1
	if len(input_imgs) > 0:	
		input_data = []
		for i in range(len(input_imgs)):
			input_data.append(transformer.preprocess('data', input_imgs[i]))
		
		print 'found {} reference images'.format(len(input_imgs))
		input_data_np = np.array(input_data)
		net.blobs['data'].reshape(len(input_imgs), 3, 227, 227)
		net.reshape()
		net.blobs['data'].data[...] = input_data_np
		output = net.forward()
		result.extend(copy.deepcopy(output['feat']))
		#f = plt.figure(figsize=(16,9))

legend = []
colors = ['#ff0000', '#ffff00', '#00ff00', '#00ffff', '#0000ff', 
     '#ff00ff', '#990000', '#999900', '#009900', '#009999']
#for i in range(2):
#	good = [a for ix,a in enumerate(feat) if labels[ix]==i]
#	print str(good)
#	x_list = [x for [x,y] in good]
#	y_list = [y for [x,y] in good]
#	plt.plot(x_list, y_list, '.',c=colors[i])
#	legend.append(str(i))

x_list = [x for [x,y] in result]
y_list = [y for [x,y] in result]
#plt.plot(x_list, y_list, '.',c=colors[0])
#legend.append('dr')

net.blobs['data'].reshape(1, 3, 227, 227)
net.reshape()
# now loop over input images

# read the image paths from the file
input_file = open(input_file_path, 'r')
input_file_lines = input_file.read().splitlines()
for i,input_item in enumerate(input_file_lines):
	tokens = input_item.split(' ')
	if tokens[1] == '1':
		if i%100 == 0:
			print 'processing input image ' + str(i) + '/' + str(len(input_file_lines)) + ': '  + tokens[0]
		img = misc.imread(tokens[0])
		img = misc.imresize(img, (227, 227))
	
		input_data = transformer.preprocess('data', img)
	
		input_data_np = np.array(input_data)
		net.blobs['data'].data[...] = input_data_np
		
		output = net.forward()
		input_result = output['feat']

		#plt.plot(x_list_single, y_list_single, '.',c=colors[1])
		#legend.append('36.jpg')
	
		#plt.legend(legend)
		#plt.grid()

		# find the distances
		distances = [np.linalg.norm(input_result-dr_result) for dr_result in result]

		# calculate ranking
		dist_array = np.array(distances)
		temp = dist_array.argsort()
		ranks = np.empty(len(dist_array),int)
		ranks[temp] = np.add(np.arange(len(dist_array)), 1).tolist()
		ranks = ranks.tolist()
		ranks.insert(0,input_item.split('/')[-1])
		#print sorted_distances[1:10]
		rank_matrix.append(ranks)

with open(output_path, 'w') as csvfile:
	thewriter = csv.writer(csvfile)
	for row in rank_matrix:
		thewriter.writerow(row)
