# MortgageRisk

Scratch: ~/mnt/storage/scratch/mc14641
			../../scratch/mc14641
MySpace ~/mnt/storage/home/mc14641/Thesis
		  mc14641/Thesis/Data

scp Data/file.big mc14641@bc4login.acrc.bris.ac.uk:Thesis/Data
scp -r Code mc14641@bc4login.acrc.bris.ac.uk:Thesis/

virtualenv -> source gpu/bin/activate -> deactivate


Tensorboard:

Run: tensorboard --logdir=Data/logs/ --port 6007
Ssh forward: ssh mc14641@bc4gpulogin.acrc.bris.ac.uk -L 6006:10.143.32.8:6007
Ssh forward: ssh mc14641@bc4gpulogin.acrc.bris.ac.uk -L 6006:137.222.245.207:6007


module load libs/cudnn/8.0-cuda-8.0

# copy back combo files
rsync -rv --include '*/' --include '*Combo.h5' --exclude '*' mc14641@bc4login.acrc.bris.ac.uk:../../scratch/mc14641/data/ /Users/mikecooper/Google\ Drive/Macbook\ Pro/University/4th\ Year/Project/Data/American