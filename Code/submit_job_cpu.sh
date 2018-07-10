#!/bin/bash       
#SBATCH --job-name=DATA_CLEANING
#SBATCH -t 3-00:00 # Runtime in D-HH:MM
#SBATCH -p hmem # Partition to submit to
#SBATCH --mem=500G
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH -J DATA_CLEANING    # name
#SBATCH -o hostname_%j.out # File to which STDOUT will be written                                                                                    
#SBATCH -e hostname_%j.err # File to which STDERR will be written                                                                                    
#SBATCH --mail-type=END # Type of email notification- BEGIN,END,FAIL,ALL                                                                             
#SBATCH --mail-user=mc14641@bristol.ac.uk # Email to which notifications will be sent                                                                

module add libs/tensorflow/1.2
module load libs/cudnn/8.0-cuda-8.0
source env/bin/activate



# srun python cifar_model_lab4_4.1.py

#srun -p hmem --nodes=1 --ntasks-per-node=1 --cpus-per-task=1 -A comsm0018  -t 3-00:00 --mem=500G python -u Code/Model/DataProcessing/American/DataProcessing.py
srun -p hmem --nodes=1 --ntasks-per-node=1 --cpus-per-task=1 -A comsm0018  -t 3-00:00 --mem=500G python -u Code/Model/Train.py

wait
