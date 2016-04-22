#!/usr/bin/env python

# Calculate the MAP for the given input and ground truth table, as determined by the NIH pill challenge criteria.
# See http://pir.nlm.nih.gov/challenge/MAP_example/

NUM_HARD_NEGATIVES = 2 # number of hard negs to gen for each consumer image

import sys
import csv
import operator
# parse command line arguments or use defaults
def parse_args():
	if len(sys.argv) < 5:
		print "Usage: calculate_map ground_truth_csv input_csv test1(reference) test2(consumer)"
		return false
	else:
		return (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

# loads a "dense" matrix (list of row/columns that should have 1s) and turn them into a dict of lists -- the reference image matches for each consumer image.
# used for loading the ground truth tables
def load_dense(file_path):
	sparse = dict()
	with open(file_path, 'rb') as csvfile:
		thereader = csv.reader(csvfile)
		cols = thereader.next()
		for row in thereader:
			# each row is one pair. If the columns and rows don't exist, add them. Then then insert a 1 at their intersection.
			# row[0] is the colum header (reference image)
			# row[1] is the row header (consumer image)
			if row[2] not in sparse:
				sparse[row[2]] = []
			sparse[row[2]].append(row[1])
	return sparse

# load a "sparse" matrix (a full csv matrix) as a dict
def load_matrix(file_path):
	sparse = dict()
	cols = []
	with open(file_path, 'rb') as csvfile:
		thereader = csv.reader(csvfile)
		cols = thereader.next()[1:] # need to skip the first (blank) item in the column list
		#print 'cols: '
		#print cols
		for row in thereader:
			consumer_image = row[0].split(' ')[0]
			if consumer_image not in sparse:
				sparse[consumer_image] = {}
			for idx,value in enumerate(row[1:]):
				sparse[consumer_image][cols[idx]] = int(value)
	return sparse

def find_hard_negatives(ground_truth, input_matrix):
	N = float(len(input_matrix))

	hard_negatives = []

	ctr=0
	# loop over the entire input matrix
	for cq,ranks in input_matrix.iteritems():
		if ctr<10:
			# find the ranks that the input assigned for the correct reference images
			match_1 = ground_truth[cq][0]
			match_2 = ground_truth[cq][1]
			rank_1 = float(ranks[match_1])
			rank_2 = float(ranks[match_2])

			hard_negs_for_this_cq = 0
			rank = 0
			ascending_rank_tuples = sorted(ranks.items(), key=operator.itemgetter(1))
			print ascending_rank_tuples
			while hard_negs_for_this_cq != NUM_HARD_NEGATIVES:
				rank_tuple = ascending_rank_tuples[rank]
				if rank_tuple[1] is not rank_1 and rank_tuple[1] is not rank_2:
					hard_negatives.append([cq,rank_tuple[0]])
					hard_negs_for_this_cq = hard_negs_for_this_cq + 1
				rank = rank + 1
		ctr = ctr+1

	return hard_negatives

def append_negative_pairs_to_files(cq_file, ref_file):
	pass

def shuffle_files_linked(file1, file2):
	pass

if __name__ == "__main__":
	args = parse_args()

	if args:
		ground_truth = load_dense(args[0])
		input_matrix = load_matrix(args[1])
		hard_negatives = find_hard_negatives(ground_truth, input_matrix)
		append_negative_pairs_to_files(args[2], args[3])
		shuffle_files_linked(args[2], args[3])
		print '============================'

		print '{} hard negatives found.'.format(len(hard_negatives))
		print 'first hard negatives:'
		for x in hard_negatives[0:20:2]:
			print str(x)
		print '867.jpg hard negatives:' + str([v[1] for v in hard_negatives if v[0]=='867.jpg'])

		print '============================'
	else:
		print "Arguments not specified correctly, quitting."