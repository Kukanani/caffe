The Challenge evaluation code is written in Python 3.5.1 (Anaconda 2.4.1) and uses pandas 0.17.1.

To run the code from the command line, navigate into the directory called pir_challenge. Then run the following (where yourentryname_MR.csv is the similarity matrix that your algorithm generates):

python pir_challenge.py yourentryname_MR.csv groundTruthTable.csv

The output will be a string that lists your entry name, the Mean Average Precision (MAP) score, the current time and date, and the filename containing the code calculating the MAP score.

This package also includes some tests that you can use to check that the evaluation code runs as expected. You must have nosetests installed with your version of Python for the tests to work. To run the tests, navigate to the pir_challenge directory in your command line, and use the following command:

nosetests

If the evaluation code runs as expected, you should see an output of "OK."