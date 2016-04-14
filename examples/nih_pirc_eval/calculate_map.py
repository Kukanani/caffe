#!/usr/bin/env python

# Calculate the MAP for the given input and ground truth table, as determined by the NIH pill challenge criteria.
# See http://pir.nlm.nih.gov/challenge/MAP_example/

import sys
import csv

# parse command line arguments or use defaults
def parse_args():
	if len(sys.argv) < 3:
		print "Usage: calculate_map ground_truth_csv input_csv"
		print "Arguments not specified correctly, continuing with default values."
		ground_truth_path = 'groundTruthTest.csv'
		input_path = 'mr1.csv'
	else:
		ground_truth_path = sys.argv[1]
		input_path = sys.argv[2]
	return (ground_truth_path, input_path)

# loads a "dense" matrix (list of row/columns that should have 1s) and turn them into a dict of lists -- the reference image matches for each consumer image.
# used for loading the ground truth tables
def load_dense(file_path):
	sparse = dict()
	with open(file_path, 'rb') as csvfile:
		thereader = csv.reader(csvfile)
		for row in thereader:
			# each row is one pair. If the columns and rows don't exist, add them. Then then insert a 1 at their intersection.
			# row[0] is the colum header (reference image)
			# row[1] is the row header (consumer image)
			if row[1] not in sparse:
				sparse[row[1]] = []
			sparse[row[1]].append(row[0])
	return sparse

# load a "sparse" matrix (a full csv matrix) as a dict
def load_matrix(file_path):
	sparse = dict()
	cols = []
	with open(file_path, 'rb') as csvfile:
		thereader = csv.reader(csvfile)
		cols = thereader.next()[1:] # need to skip the first (blank) item in the column list
		print 'cols: '
		print cols
		for row in thereader:
			consumer_image = row[0]
			if consumer_image not in sparse:
				sparse[consumer_image] = {}
			for idx,value in enumerate(row[1:]):
				sparse[consumer_image][cols[idx]] = int(value)
	return sparse

def calculate_map(ground_truth, input_matrix):
	N = float(len(input_matrix))

	p = 0.0

	# loop over the entire input matrix
	for cq,row in input_matrix.iteritems():
		# find the ranks that the input assigned for the correct reference images
		match_1 = ground_truth[cq][0]
		match_2 = ground_truth[cq][1]
		rank_1 = float(row[match_1])
		rank_2 = float(row[match_2])

		if rank_1 < rank_2:
			min_rank = rank_1
			max_rank = rank_2
		else:
			min_rank = rank_2
			max_rank = rank_1
		print 'ranks for cq ' + cq + ': ' + str(min_rank) + ' and ' + str(max_rank)
		print 'contribution: ' + str((1.0/min_rank + 2.0/max_rank))

		p = p + (1.0/min_rank + 2.0/max_rank)

	print p
	print N
	p = p / N / 2.0; # normalize to number of images
	return p

if __name__ == "__main__":
	args = parse_args()
	ground_truth = load_dense(args[0])
	input_matrix = load_matrix(args[1])
	precision = calculate_map(ground_truth, input_matrix)

	print 'printing debug information'
	print ground_truth
	print input_matrix
	print '============================'

	print 'The ground truth table is for ' + str(len(ground_truth)) + ' objects.'
	print 'The input matrix is for ' + str(len(input_matrix)) + ' objects.'
	print 'MAP is ' + str(precision)