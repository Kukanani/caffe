from generate_hard_negatives import GenHardNeg
import sys
from random import shuffle

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print 'must specify list of reference images!'
        exit()
    ref_list_path = sys.argv[1]

    ref_prefix = ''
    cq_prefix  = ''

    ref_list = []
    with open(ref_list_path, 'r') as thefile:
        for row in thefile:
            path = row.split(' ')[0]
            tokens = path.rpartition('/')
            if len(ref_prefix) == 0:
                ref_prefix = tokens[0] + tokens[1]
                cq_prefix = ref_prefix.replace('dr','dc')
            ref_list.append(tokens[2])

    ground_truth_csv_path = 'data/groundTruthTableN.csv'

    g = GenHardNeg()

    ground_truth = g.load_dense(ground_truth_csv_path)

    cq_list = []
    for cq, ref in ground_truth.iteritems():
        if any(el in ref for el in ref_list):
            cq_list.append(cq_prefix + cq)

    #shuffle(cq_list) # this isn't needed, we're not training
    for cq in cq_list:
        print cq