"""
This module contains functions for evaluting submissions to the C3PI Pill 
Image Recognition challange.    
"""
__author__ = 'Pill Image Recognition Challenge'
__version__ = '0.0.1'


import os
import numpy as np
import numpy.testing as npt
import pir_challenge as pirc

class test_pir_challenge(object):
    '''
    Test class used by the nose framework:
    1. nosetests (minimal output, number of tests and summary pass or fail)
    2. nosetests -v (lists the tests and whether each passed or failed)
    3. nosetests -v --nocapture (lists the tests, whether each passed or failed,
                                 and our output)
    Running a single test:
    nosetests <file>:<test_case>.<test_method>
    nosetests test_pir_challenge.py:test_pir_challenge.test_valid_ranking
    
    To the left of the colon is the path to the module.
    To the right of the colon is the class and method to run.
    '''
    
    def absolute_path(self, test_input_file_name):
        """
        Get the absolute path to the test input file. This allows us to run
        nosetests from any directory.

        The input is expected to be given relative to this file.
        """
        full_path = os.path.dirname(os.path.abspath(__file__)) 
        return os.path.join(full_path, 'data', test_input_file_name)    
    
    def test_valid_ranking(self):
        # Valid rankings.
        ranking1 = np.array([[3,2,1],[1,3,2]])
        ranking2 = np.array([[2,1],[2,1]])

        assert(pirc.valid_ranking(ranking1) == True)
        assert(pirc.valid_ranking(ranking2) == True)

        # Invalid rankings.
        ranking3 = np.array([[3,1],[2,1]])
        ranking4 = np.array([[1.5,1],[2,1]])
        assert(pirc.valid_ranking(ranking3) == False)
        assert(pirc.valid_ranking(ranking4) == False)
        
    def test_load_rank_matrix(self):
        '''
        This tests if the function that reads in a ranking matrix file works
        as expected. 
        '''
        test_matrix_file = 'rankingMatrix10by10.csv'
        cols_sorted = ['',
             '00093-0311-01_PART_1_OF_1_CHAL10_SF_26211358.jpg',
             '00093-7155-98_PART_1_OF_1_CHAL10_SF_4A21A50D.jpg',
             '00143-1268-01_PART_1_OF_1_CHAL10_SF_7321B9DD.jpg',
             '00172-5728-60_PART_1_OF_1_CHAL10_SF_5821AC5D.jpg',
             '00173-0595-00_PART_1_OF_1_CHAL10_SF_10230838.jpg',
             '00527-1311-01_PART_1_OF_1_CHAL10_SF_2D2696B4.jpg',
             '00781-5184-01_PART_1_OF_1_CHAL10_SF_6E21B76D.jpg',
             '50111-0563-01_PART_1_OF_1_CHAL10_SF_6B243581.jpg',
             '53489-0146-01_PART_1_OF_1_CHAL10_SF_8021C06E.jpg',
             '60505-1308-01_PART_1_OF_1_CHAL10_SF_4F21A7DD.jpg']
        rows_sorted = ['1718.jpg',
             '2281.jpg',
             '2436.jpg',
             '2478.jpg',
             '2500.jpg',
             '382.jpg',
             '41.jpg',
             '464.jpg',
             '491.jpg',
             '902.jpg']
             

        test_ranking_matrix_dataframe = pirc.load_rank_matrix(self.absolute_path(test_matrix_file))
        assert(np.array_equal(sorted(test_ranking_matrix_dataframe.ix[:,0]),rows_sorted))
        assert(np.array_equal(sorted(test_ranking_matrix_dataframe.columns[1:]),cols_sorted[1:]))
    
    def test_ground_truth_to_subset_matrix(self):
        ground_truth_filename = 'unwrappedTable.csv'
        test_subsetting_files = ['rankingMatrix10by10.csv']
        cols_sorted = ['',
             '00093-0311-01_PART_1_OF_1_CHAL10_SF_26211358.jpg',
             '00093-7155-98_PART_1_OF_1_CHAL10_SF_4A21A50D.jpg',
             '00143-1268-01_PART_1_OF_1_CHAL10_SF_7321B9DD.jpg',
             '00172-5728-60_PART_1_OF_1_CHAL10_SF_5821AC5D.jpg',
             '00173-0595-00_PART_1_OF_1_CHAL10_SF_10230838.jpg',
             '00527-1311-01_PART_1_OF_1_CHAL10_SF_2D2696B4.jpg',
             '00781-5184-01_PART_1_OF_1_CHAL10_SF_6E21B76D.jpg',
             '50111-0563-01_PART_1_OF_1_CHAL10_SF_6B243581.jpg',
             '53489-0146-01_PART_1_OF_1_CHAL10_SF_8021C06E.jpg',
             '60505-1308-01_PART_1_OF_1_CHAL10_SF_4F21A7DD.jpg']
        rows_sorted = ['1718.jpg',
             '2281.jpg',
             '2436.jpg',
             '2478.jpg',
             '2500.jpg',
             '382.jpg',
             '41.jpg',
             '464.jpg',
             '491.jpg',
             '902.jpg']
        for test_file in test_subsetting_files:
            rank_matrix = pirc.load_rank_matrix(self.absolute_path(test_file))
            ground_truth_matrix_subset = pirc.ground_truth_to_subset_matrix(self.absolute_path(ground_truth_filename),rank_matrix)
            print(ground_truth_matrix_subset.ix[:,0])
            print(rows_sorted)
            assert(np.array_equal(sorted(ground_truth_matrix_subset.ix[:,0]),rows_sorted))
            assert(np.array_equal(sorted(ground_truth_matrix_subset.columns[1:]),cols_sorted[1:]))
        
    def test_mean_average_precision(self):
        ground_truth_filename = 'unwrappedTable.csv'
        input_output = [('rankingFromGroundTruthMatrix5by2000orderChanged.csv',1.0), ('ranking10by10correct.csv',1.0),
                        ('rankingFromGroundTruthMatrix5by2000.csv',1.0),('rankingFromGroundTruthMatrix3000by2000.csv',1.0),
                        ('ranking10by10ThirdRanking.csv',1.0/3.0)]
        for test_file, known_mean_avg_precision in input_output:
            rank_matrix = pirc.load_rank_matrix(self.absolute_path(test_file))
            ground_truth_matrix_subset = pirc.ground_truth_to_subset_matrix(self.absolute_path(ground_truth_filename),rank_matrix)
            mean_avg_precision = pirc.mean_average_precision(rank_matrix, ground_truth_matrix_subset)
            print('Known MAP: {:0.2f}, Computed MAP: {:0.2f}'.format(known_mean_avg_precision, mean_avg_precision))
            npt.assert_almost_equal(mean_avg_precision, known_mean_avg_precision)


        
            

