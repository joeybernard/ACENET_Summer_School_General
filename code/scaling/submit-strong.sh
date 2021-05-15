#!/bin/bash
#SBATCH --cpus-per-task=8
#SBATCH --time=1:0
#SBATCH --array=1-8%1

./a.out 2000 2000 $SLURM_ARRAY_TASK_ID
./a.out 2000 2000 $SLURM_ARRAY_TASK_ID
./a.out 2000 2000 $SLURM_ARRAY_TASK_ID
