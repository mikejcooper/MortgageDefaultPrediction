#!/bin/bash

module add libs/tensorflow/1.2
module add libs/cudnn/8.0-cuda-8.0
srun -p hmem --nodes=1 --ntasks-per-node=2 --cpus-per-task=1 -A comsm0018  -t 0-10:00 --mem=500G --pty bash
#srun -p cpu --nodes=1 --ntasks-per-node=2 --cpus-per-task=1 -A comsm0018  -t 2-00:00 --mem=100G --pty bash
