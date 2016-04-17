"""
This module contains functions for evaluting submissions to the C3PI Pill 
Image Recognition challange.    
"""
__author__ = 'Pill Image Recognition Challenge'
__version__ = '0.0.1'

import pandas as pd
import numpy as np

import sys
import os
import contextlib
import datetime

#
# Using a context manager so that we can write to stdout or file in the same
# manner. When writing to a file, if the file does not exist it is created. 
# Data is appended to the file.
# Based on code from stack overflow:
# http://stackoverflow.com/questions/17602878/how-to-handle-both-with-open-and-sys-stdout-nicely
@contextlib.contextmanager
def smart_open(filename=None):
    if filename:
        fh = open(filename, 'a+')
    else:
        fh = sys.stdout
    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()


def mean_average_precision(rank_matrix, ground_truth_subset_matrix):
    """
    Compute the mean average precision. mean over Q queries, of average
    precision per query.
    ..math::
    \frac{1}{Q}\sum_{i=1}^Q\frac{1}{N_i}\sum_{j=1}^{N_i}\frac{j}{rank(\textrm{TP}_{i,j})}
    """
    correct_rankings = np.multiply(np.array(rank_matrix.ix[:,1:]), np.array(ground_truth_subset_matrix.ix[:,1:]))
    correct_rankings.sort()
    query_list = np.vsplit(correct_rankings, correct_rankings.shape[0])

    average_precision_sum = 0.0
    for query_results in query_list:
        query_results = query_results[query_results.nonzero()]
        precision_sum = 0.0
        # Compute the average precision.
        for index,rank in enumerate(query_results):
            precision_sum += (index+1)/rank
        average_precision_sum += precision_sum/len(query_results)

    return average_precision_sum/len(query_list)


def valid_ranking(rank_matrix):
    """
    Check that the entries in the rank matrix are valid: inside expected range
    and unique.
    """
    expected_values = np.tile(np.array(range(1,rank_matrix.shape[1]+1)),[rank_matrix.shape[0],1])
    return np.array_equal(expected_values, np.sort(rank_matrix))


def load_rank_matrix(matrix_filename):
    """
    Load the rank matrix. First column contains the query/consumer-quality image file names. First
    row contains the reference image file names. We require that both the column and row be ordered
    in alphabetical order. To ensure this we sort the data accordingly. We then check that the
    rank matrix is valid and return the whole dataset as a pandas dataframe.
    """
    rank_matrix = pd.read_csv(matrix_filename)
    
    # Sort the rows and columns
    rank_matrix.sort_values(by=rank_matrix.columns.values[0],
                            inplace = True)
    rank_matrix = rank_matrix.reindex_axis(list([rank_matrix.columns[0]])+list(sorted(rank_matrix.columns[1:])),axis=1)
    rank_matrix_data = rank_matrix.iloc[:,1:].values    
    if not valid_ranking(rank_matrix_data):
        raise Exception(matrix_filename+' is not a valid ranking matrix!')
    return rank_matrix


def ground_truth_to_subset_matrix(ground_truth_filename,rank_matrix):
    """
    This function extracts the ground truth subset which corresponds to the query/consumer-quality and 
    reference images contained in the rank_matrix dataframe. The function returns the ground truth dataframe.
    We assume that the full ground truth dataset is a superset of that found in the rank_matrix.
    """
    ground_truth_table_all = pd.read_csv(ground_truth_filename)
    ground_truth_table_subset = ground_truth_table_all[ground_truth_table_all['ref_images'].isin(rank_matrix.columns[1:]) & 
        ground_truth_table_all['cons_images'].isin(rank_matrix.ix[:,0])]
    ref_names_dict = dict(zip(rank_matrix.columns[1:],range(len(rank_matrix.columns[1:]))))
    cons_names_dict = dict(zip(rank_matrix.ix[:,0],range(len(rank_matrix.ix[:,0]))))
    ground_truth_matrix_subset_ref = [ref_names_dict[i] for i in list(ground_truth_table_subset.ref_images)]
    ground_truth_matrix_subset_cons = [cons_names_dict[i] for i in list(ground_truth_table_subset.cons_images)]
    ground_truth_matrix_subset = np.zeros([rank_matrix.shape[0],rank_matrix.shape[1]-1])
    ground_truth_matrix_subset[np.array(ground_truth_matrix_subset_cons),np.array(ground_truth_matrix_subset_ref)]=1
    ground_truth_matrix_subset = pd.concat([pd.DataFrame(rank_matrix.ix[:,0]),pd.DataFrame(ground_truth_matrix_subset,columns=rank_matrix.columns[1:])],axis=1)
    return ground_truth_matrix_subset


def main(argv=None):
    # For the exit codes to be multi platform we don't use the os.EX.. codes as
    # those are only defined on unix/mac. We define them here with the same 
    # values.
    EX_OK = 0
    EX_DATAERR = 65
    if argv is None:
        argv = sys.argv[1:]
    if len(argv)< 2:
        print('Wrong number of arguments.')
        print('Usage: python ' + __file__ + ' yourentryname_MR.csv groundtruth_table.csv [outputfilename.csv]')
        return EX_DATAERR
    try:
        rank_matrix = load_rank_matrix(argv[0])
        ground_truth_matrix_subset = ground_truth_to_subset_matrix(argv[1],rank_matrix)
        mean_avg_precision = mean_average_precision(rank_matrix, ground_truth_matrix_subset)
        fname = None if len(argv)<3 else argv[2]
        with smart_open(fname) as fh:
            entry_name, _ = os.path.splitext(os.path.basename(argv[0]))
            fh.write(entry_name + ', ' + 
                     str(mean_avg_precision)  + ', ' + 
                     str(datetime.datetime.now()) + ', ' + 
                     'python ' + 
                     __file__ + ' ' +
                     ' '.join(argv) + '\n')                  
    except Exception as err:
        print(err)
        return EX_DATAERR
    return EX_OK

    
if __name__ == "__main__":
    sys.exit(main())
    
