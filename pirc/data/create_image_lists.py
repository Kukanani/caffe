#!/usr/bin/env python
import csv
from random import shuffle, randint

TRAIN_PERCENTAGE = 0.7 # the rest is test

# change to match platform
ABSOLUTE_PATH = '/work/04002/aa67857/caffe/pirc/data/'

# these folders are in ABSOLUTE_PATH. The ground truth table lists ref images first, then consumer images
REF_PATH = 'dr/'
CONSUMER_PATH = 'dc/'

TRAIN_1_PATH = 'train1.txt'
TRAIN_2_PATH = 'train2.txt'
TEST_1_PATH =  'test1.txt'
TEST_2_PATH =  'test2.txt'

def main():

	ground_truth = []

	with open('groundTruthTableSorted.csv', 'rb') as csvfile:
		csvreader = csv.reader(csvfile)
		ground_truth = list(csvreader)[1:] # skip the first line

	pos_pairs = len(ground_truth)

	target_train_pairs = int(TRAIN_PERCENTAGE * pos_pairs)
	target_test_pairs = pos_pairs - target_train_pairs
	print "{} positive pairs from the ground truth table. {} will be used for training.".format(pos_pairs, target_train_pairs)

	#shuffle(ground_truth)

	gend = 0
	train_pairs_1 = []
	train_pairs_2 = []

	for i in range(target_train_pairs):
		# read the next positive pair: they are already shuffled!
		pos_pair = ground_truth[i]

		train_pairs_1.append([pos_pair[0], '1'])
		train_pairs_2.append([pos_pair[1], '1'])

		# choose a random negative pair:
		#   - generate the pair
		#   - check that pair is not actually a positive pair
		neg_first_elem = pos_pair[0]
		# find positive matches for the first element
		pos_indices = [i for i, x in enumerate(ground_truth) if x == neg_first_elem]
		pos_second_elems = [ground_truth[i][1] for i in pos_indices]
		second_elem_valid = False
		while ~second_elem_valid:
			neg_second_elem = ground_truth[randint(0,target_train_pairs-1)][1]
			second_elem_valid = ~(neg_second_elem in pos_second_elems)
			if ~second_elem_valid: # just for curiosity
				print "collision! {} and {} is a positive pair".format(neg_first_elem, neg_second_elem)

		train_pairs_1.append([neg_first_elem, '0'])
		train_pairs_2.append([neg_second_elem, '0'])

		gend = gend+2

	train_pairs_1_shuf = []
	train_pairs_2_shuf = []
	index_shuf = range(len(train_pairs_1))
	shuffle(index_shuf)
	for i in index_shuf:
	    train_pairs_1_shuf.append(train_pairs_1[i])
	    train_pairs_2_shuf.append(train_pairs_2[i])

	print "generate {} training pairs.".format(gend)

	# the rest of the pairs go into the test set
	gend = 0
	test_pairs_1 = []
	test_pairs_2 = []
	for i in range(target_train_pairs,pos_pairs):
		pos_pair = ground_truth[i]
		
		test_pairs_1.append([pos_pair[0], '1'])
		test_pairs_2.append([pos_pair[1], '1'])

		neg_first_elem = ground_truth[i][0]
		# find positive matches for the first element
		pos_indices = [i for i, x in enumerate(ground_truth) if x == neg_first_elem]
		pos_second_elems = [ground_truth[i][1] for i in pos_indices]
		second_elem_valid = False
		while ~second_elem_valid:
			neg_second_elem = ground_truth[randint(target_train_pairs, pos_pairs-1)][1]
			second_elem_valid = ~(neg_second_elem in pos_second_elems)
			if ~second_elem_valid: # just for curiosity
				print "collision! {} and {} is a positive pair".format(neg_first_elem, neg_second_elem)

		test_pairs_1.append([neg_first_elem, '0'])
		test_pairs_2.append([neg_second_elem, '0'])

		gend = gend+2

	test_pairs_1_shuf = []
	test_pairs_2_shuf = []
	index_shuf = range(len(test_pairs_1))
	shuffle(index_shuf)
	for i in index_shuf:
	    test_pairs_1_shuf.append(test_pairs_1[i])
	    test_pairs_2_shuf.append(test_pairs_2[i])

	print "generate {} testing pairs.".format(gend)

	with open(TRAIN_1_PATH, 'wb') as thefile:
		for item in train_pairs_1_shuf:
			thefile.write(ABSOLUTE_PATH + REF_PATH + ' '.join(item) + '\n')
	with open(TRAIN_2_PATH, 'wb') as thefile:
		for item in train_pairs_2_shuf:
			thefile.write(ABSOLUTE_PATH + CONSUMER_PATH + ' '.join(item) + '\n')

	with open(TEST_1_PATH, 'wb') as thefile:
		for item in test_pairs_1_shuf:
			thefile.write(ABSOLUTE_PATH + REF_PATH + ' '.join(item) + '\n')
	with open(TEST_2_PATH, 'wb') as thefile:
		for item in test_pairs_2_shuf:
			thefile.write(ABSOLUTE_PATH + CONSUMER_PATH + ' '.join(item) + '\n')

	print "all done! You should verify that the number of unique reference and consumer images in each file makes sense."
	print "use commands like: awk '{print $1}' test1.txt | sort -u | wc -l"

if __name__ == "__main__": main()
