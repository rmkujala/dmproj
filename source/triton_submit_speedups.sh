#!/bin/bash
#SBATCH -J dmproj_speedups
#SBATCH -e dmproj_speedups_err
#SBATCH -o dmproj_speedups_out
#SBATCH -t 0-10:00:00
#SBATCH --mem-per-cpu=15000
#SBATCH -n 1
#SBATCH -p batch
#SBATCH --array=8-23 #0-23
#SBATCH --constraint=opteron

module load python/2.7.4 numpy/1.7.0
pypy speedups.py $(($SLURM_ARRAY_TASK_ID/8)) $(($SLURM_ARRAY_TASK_ID%8))
