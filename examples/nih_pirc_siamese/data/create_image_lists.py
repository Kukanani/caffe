#!/usr/bin/env python
import csv
from random import shuffle, randint

TRAIN_PERCENTAGE = 0.7 # the rest is test

# change to match platform
ABSOLUTE_PATH = '/home/adam/caffe/examples/nih_pirc_siamese/data/'

# these folders are in ABSOLUTE_PATH. The ground truth table lists ref images first, then consumer images
REF_PATH = 'dr/'
CONSUMER_PATH = 'dc/'

TRAIN_1_PATH = 'train1.txt'
TRAIN_2_PATH = 'train2.txt'
TEST_1_PATH = 'test1.txt'
TEST_2_PATH = 'test2.txt'

def main():

	ground_truth = []

	with open('groundTruthTable.csv', 'rb') as csvfile:
		csvreader = csv.reader(csvfile)
		ground_truth = list(csvreader)[1:] # skip the first line

	pos_pairs = len(ground_truth)
	target_train_pairs = TRAIN_PERCENTAGE * pos_pairs
	print "{} positive pairs from the ground truth table. {} will be used for training.".format(pos_pairs, target_train_pairs)

	shuffle(ground_truth)

	train_pairs_ct = 0
	train_pairs_1 = []
	train_pairs_2 = []

	while train_pairs_ct < target_train_pairs:
		# choose a random positive pair: they are already shuffled!
		pos_pair = ground_truth[train_pairs_ct]

		train_pairs_1.append([pos_pair[0], '1'])
		train_pairs_2.append([pos_pair[1], '1'])

		# choose a random negative pair:
		#   - generate the pair
		#   - check that pair is not actually a positive pair
		neg_first_elem = ground_truth[train_pairs_ct][0]
		# find positive matches for the first element
		pos_indices = [i for i, x in enumerate(ground_truth) if x == neg_first_elem]
		pos_second_elems = [ground_truth[i][1] for i in pos_indices]
		second_elem_valid = False
		while ~second_elem_valid:
			neg_second_elem = ground_truth[randint(0,pos_pairs-1)][1]
			second_elem_valid = ~(neg_second_elem in pos_second_elems)
			if ~second_elem_valid: # just for curiosity
				print "collision! {} and {} is a positive pair".format(neg_first_elem, neg_second_elem)

		train_pairs_1.append([neg_first_elem, '0'])
		train_pairs_2.append([neg_second_elem, '0'])

		train_pairs_ct = train_pairs_ct + 1

	# the rest of the pairs go into the test set
	test_pairs_1 = []
	test_pairs_2 = []
	for i in range(train_pairs_ct-1,pos_pairs-1):
		pos_pair = ground_truth[i]
		
		test_pairs_1.append([pos_pair[0], '1'])
		test_pairs_2.append([pos_pair[1], '1'])

		neg_first_elem = ground_truth[i][0]
		# find positive matches for the first element
		pos_indices = [i for i, x in enumerate(ground_truth) if x == neg_first_elem]
		pos_second_elems = [ground_truth[i][1] for i in pos_indices]
		second_elem_valid = False
		while ~second_elem_valid:
			neg_second_elem = ground_truth[randint(0,pos_pairs-1)][1]
			second_elem_valid = ~(neg_second_elem in pos_second_elems)
			if ~second_elem_valid: # just for curiosity
				print "collision! {} and {} is a positive pair".format(neg_first_elem, neg_second_elem)

		test_pairs_1.append([neg_first_elem, '0'])
		test_pairs_2.append([neg_second_elem, '0'])

	with open(TRAIN_1_PATH, 'wb') as thefile:
		for item in train_pairs_1:
			thefile.write(ABSOLUTE_PATH + REF_PATH + ' '.join(item) + '\r')
	with open(TRAIN_2_PATH, 'wb') as thefile:
		for item in train_pairs_2:
			thefile.write(ABSOLUTE_PATH + CONSUMER_PATH + ' '.join(item) + '\r')

	with open(TEST_1_PATH, 'wb') as thefile:
		for item in test_pairs_1:
			thefile.write(ABSOLUTE_PATH + REF_PATH + ' '.join(item) + '\r')
	with open(TEST_2_PATH, 'wb') as thefile:
		for item in test_pairs_2:
			thefile.write(ABSOLUTE_PATH + CONSUMER_PATH + ' '.join(item) + '\r')

if __name__ == "__main__": main()