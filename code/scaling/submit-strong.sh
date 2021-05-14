#!/bin/bash
#SBATCH -A def-svassili
#SBATCH --cpus-per-task=16
#SBATCH --time=1:0
#SBATCH --array=1-16%1

./a.out 2000 2000 $SLURM_ARRAY_TASK_ID
./a.out 2000 2000 $SLURM_ARRAY_TASK_ID
./a.out 2000 2000 $SLURM_ARRAY_TASK_ID
