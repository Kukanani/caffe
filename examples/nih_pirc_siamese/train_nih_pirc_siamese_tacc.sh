#!/usr/bin/env sh

TOOLS=/work/01932/dineshj/CS381V/caffe_install_scripts/caffe/build/tools

$TOOLS/caffe train --solver=examples/nih_pirc_siamese/nih_pirc_siamese_solver.prototxt
