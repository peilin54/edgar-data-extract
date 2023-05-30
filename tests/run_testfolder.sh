#!/bin/bash

# This folder contains 2 test.
# 1. Run code with one .txt file in the ./test-1/ folder. Then use shell `diff` to compare output .csv files with those in ./test-1/test_data folder.
python ../edgar/edgar_form4.py -inpath ./test-1/test_data/ -outpath ./test-1/ 

cd test-1
echo "===================test 1   ====================="
diff nonDerivative.csv test_data/
diff derivative.csv  test_data/
diff footnotes.csv  test_data/
cd ..

#2. Run code with 100 .txt files in ./test-100/ folder. Compare output .csv files with those in ./test-100/test_data.  
#This will read from a list_txt file to get file reading order, to minimize difference caused by system reading the 100 files in different order.

python ../edgar/edgar_form4.py -inpath ./test-100/test_data/ -outpath ./test-100/ -readlist True

cd test-100
echo "===================test 100 ====================="
diff nonDerivative.csv test_data/
diff derivative.csv  test_data/
diff footnotes.csv  test_data/
cd ..

# python main.py  -inpath ./tests/test-1/test_data -outpath ./tests/test-1
#
#
#
