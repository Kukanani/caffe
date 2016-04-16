#!/usr/bin/env sh

TOOLS=/work/01932/dineshj/CS381V/caffe_install_scripts/caffe/build/tools
BASE=/work/04002/aa67857/caffe

cd $BASE/examples/nih_pirc_siamese
$TOOLS/caffe train --solver=$BASE/examples/nih_pirc_siamese/nih_pirc_mnist_full_solver.prototxt
