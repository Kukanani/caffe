#!/usr/bin/env sh

TOOLS=~/caffe/tools

$TOOLS/caffe train --solver=examples/nih_pirc_siamese/nih_pirc_mnist_full_solver.prototxt
