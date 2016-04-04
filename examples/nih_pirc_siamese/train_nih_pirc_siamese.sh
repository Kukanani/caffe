#!/usr/bin/env sh

TOOLS=./build/tools

$TOOLS/caffe train --solver=examples/nih_pirc_siamese/nih_pirc_siamese_solver.prototxt
