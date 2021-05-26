#!/bin/bash
#SBATCH --cpus-per-task=16
#SBATCH --time=10:00
#SBATCH --array=1-16%1

N=$SLURM_ARRAY_TASK_ID
w=2000
h=2000
# This keeps the total pixel count in proportion to N:
sw=$(printf '%.0f' `echo "scale=6;sqrt($N)*$w" | bc`)
sh=$(printf '%.0f' `echo "scale=6;sqrt($N)*$h" | bc`)
echo "width x height: $sw x $sh"
./a.out $sw $sh $N
./a.out $sw $sh $N
./a.out $sw $sh $N
