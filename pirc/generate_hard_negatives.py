#!/usr/bin/env python

# Calculate the MAP for the given input and ground truth table, as determined by the NIH pill challenge criteria.
# See http://pir.nlm.nih.gov/challenge/MAP_example/

NUM_HARD_NEGATIVES = 2 # number of hard negs to gen for each consumer image

import sys
import csv
import operator
# parse command line arguments or use defaults

ground_truth_csv_path = ''
input_csv_path = ''

output_ref_path = ''
output_cq_path = ''

all_pairs = []

def parse_args():
	if len(sys.argv) < 5:
		#print 'Usage: calculate_map ground_truth_csv input_csv test1(reference)_tomodify test2(consumer)_tomodify'
		return False
	else:
		ground_truth_csv_path = sys.args[1]
		input_csv_path = sys.args[2]
		output_ref_path = sys.args[3]
		output_cq_path = sys.args[4]
		return True

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
					hard_negatives.append([rank_tuple[0],cq,0])
					hard_negs_for_this_cq = hard_negs_for_this_cq + 1
				rank = rank + 1
		ctr = ctr+1

	return hard_negatives

def save_pairs_to_files(all_pairs, ref_path, cq_path):
	with open(ref_path, 'w') as ref_file, open(cq_path, 'w') as cq_file:
		for i in len(all_pairs):
			ref_file.write(all_pairs[0] + ' ' + str(all_pairs[2]) + '\n')
			cq_file.write(all_pairs[1] + ' ' + str(all_pairs[2]) + '\n')

def load_pairs_from_files(ref_path, cq_path):
	pairs = []
	with open(ref_path, 'r') as ref_file, open(cq_path, 'r') as cq_file:
		ref_length = 0
		cq_length = 0
		for i, ref_line in enumerate(ref_file):
			cq_line = cq_file.readline()
			pairs.append([ref_line.split(' ')[0], cq_line.split(' ')[0], int(ref_line.split(' ')[1])])
			ref_length = i
		cq_length = sum(1 for cq_line in cq_file)
		if cq_length != ref_length:
			print 'Error while loading files ' + ref_path + ' and ' + cq_path + ': the files don\'t have the same number of lines!'
	return pairs

if __name__ == "__main__":
	if parse_args():
		ground_truth = load_dense(ground_truth_csv_path)
		input_matrix = load_matrix(input_csv_path)
		hard_negatives = find_hard_negatives(ground_truth, input_matrix)
		all_pairs = load_pairs_from_files(output_ref_path, output_cq_path)
		all_pairs.append(hard_negatives)
		shuffle(all_pairs)
		save_pairs_to_files(all_pairs, output_ref_path, output_cq_path)
		print '============================'

		print '{} hard negatives found.'.format(len(hard_negatives))
		print 'first hard negatives:'
		for x in hard_negatives[0:20:2]:
			print str(x)
		print '867.jpg hard negatives:' + str([v[1] for v in hard_negatives if v[0]=='867.jpg'])

		print '============================'
	else:
		print "Arguments not specified correctly, quitting."