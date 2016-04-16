#!/bin/bash

#SBATCH -p gpu
#SBATCH -A CS381V-Visual-Recogn
#SBATCH -J NIH_PIRC_MNIST_FULL
#SBATCH -n 20
#SBATCH --time=09:00:00 
#SBATCH --error=/work/04002/aa67857/caffe/nih_pirc/logs/nih_pirc_mnist_full.err 
#SBATCH --output=/work/04002/aa67857/caffe/nih_pirc/logs/nih_pirc_mnist_full.out
#SBATCH --job-name=cs381v-mnist-full
#SBATCH --mail-user=adam.d.allevato@gmail.com
#SBATCH --mail-type=all
 
echo job $JOB_ID execution at: `date`
NODE_HOSTNAME=`hostname -s`
echo "running on node $NODE_HOSTNAME"

/work/04002/aa67857/caffe/nih_pirc/train_nih_pirc_mnist_full_tacc.sh
