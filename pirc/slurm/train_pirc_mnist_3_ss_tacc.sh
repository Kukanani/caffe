#!/usr/bin/env sh
TOOLS=/work/01932/dineshj/CS381V/caffe_install_scripts/caffe/build/tools
BASE=/work/04002/aa67857/caffe/pirc

cd $BASE
$TOOLS/caffe train --solver=$BASE/pirc_mnist_3_ss_solver.prototxt --snapshot=$BASE/mnist_3_ss/mnist_3_ss_iter_5000.solverstate
