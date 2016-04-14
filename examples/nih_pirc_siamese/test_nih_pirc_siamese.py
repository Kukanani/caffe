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

# check command line arguments=
if len(sys.argv) < 4:
	print 'usage is test_nih_pirc_siamese.py model weights.caffemodel image_list_file_path'

model = sys.argv[1]
pretrained = sys.argv[2]
list_file_path = sys.argv[3]

# initialize input image array
input_imgs = []
labels = []

# read the image paths from the file
list_file = open(list_file_path, 'r')
list_file_lines = list_file.read().splitlines()
for line in list_file_lines:
	# put all the images into a single input array which will then be passed
	# through the network all at once. N images will be stored in an array
	# of size N x 3 x 227 x 227. This is N images with 3 channels (RGB) that
	# are 227x227 pixels
        tokens = line.split(' ')
	img = misc.imread(tokens[0])
	img = misc.imresize(img, (227, 227))
	input_imgs.append(img)
	labels.append(int(tokens[1]))

caffe.set_mode_gpu()
net = caffe.Net(model, pretrained, caffe.TEST)

transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,1,0))

input_data = []
for i in range(len(input_imgs)):
	 input_data.append(transformer.preprocess('data', input_imgs[i]))

#img = misc.imread('/work/04002/aa67857/caffe/examples/nih_pirc_siamese/data/dr/68180-0481-01_PART_1_OF_1_CHAL10_SB_FA217D1B.jpg')
#img = misc.imresize(img, (227,227))
input_data_np = np.array(input_data)
net.blobs['data'].data[...] = input_data_np

print 'DATA BLOB SIZE: ' + str(net.blobs['data'].data.shape)
output = net.forward()

print output
print labels
print len(input_imgs)

feat = output['feat']
f = plt.figure(figsize=(16,9))

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

#for i in range(len(feat)/2):


good = feat[1:-1]
x_list = [x for [x,y] in good]
y_list = [y for [x,y] in good]
plt.plot(x_list, y_list, '.',c=colors[0])
legend.append('dr')

good = [feat[0]]
x_list_single = [x for [x,y] in good]
y_list_single = [y for [x,y] in good]
plt.plot(x_list_single, y_list_single, '.',c=colors[1])
legend.append('36.jpg')

plt.legend(legend)
plt.grid()
f.savefig('test_36_vs_all_dr.png')


# find the top matches

x_list = [x - x_list_single[0] for [x,y] in feat]
y_list = [y - y_list_single[0] for [x,y] in feat]
print x_list
distances = [[np.sqrt(x_list[i]**2+y_list[i]**2),list_file_lines[i]] for i,x in enumerate(x_list)]
sorted_distances = sorted(distances,key=lambda x: x[0])
print sorted_distances[1:10]
