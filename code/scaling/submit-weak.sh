#!/bin/bash
#SBATCH --cpus-per-task=16
#SBATCH --time=10:00
#SBATCH --array=1-16%1

N=$SLURM_ARRAY_TASK_ID
w=2000
h=2000
sw=$(printf '%.0f' `echo "scale=6;sqrt($N)*$w" | bc`)
sh=$(printf '%.0f' `echo "scale=6;sqrt($N)*$h" | bc`)
./a.out $sw $sh $N
./a.out $sw $sh $N
./a.out $sw $sh $N
