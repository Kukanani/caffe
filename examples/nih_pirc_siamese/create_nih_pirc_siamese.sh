#!/usr/bin/env sh
# This script converts the mnist data into leveldb format.

EXAMPLES=./build/examples/nih_pirc_siamese
DATA=./examples/nih_pirc_siamese/data

echo "Creating leveldb..."

rm -rf ./examples/nih_pirc_siamese/nih_pirc_siamese_train_leveldb
rm -rf ./examples/nih_pirc_siamese/nih_pirc_siamese_test_leveldb

$EXAMPLES/convert_nih_pirc_siamese_data.bin \
    $DATA/train-images-idx3-ubyte \
    $DATA/train-labels-idx1-ubyte \
    ./examples/nih_pirc_siamese/nih_pirc_siamese_train_leveldb
$EXAMPLES/convert_nih_pirc_siamese_data.bin \
    $DATA/t10k-images-idx3-ubyte \
    $DATA/t10k-labels-idx1-ubyte \
    ./examples/nih_pirc_siamese/nih_pirc_siamese_test_leveldb

echo "Done."
