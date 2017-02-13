#!/bin/bash
#SBATCH -J dmproj_brute_force
#SBATCH -e dmproj_brute_force_err
#SBATCH -o dmproj_brute_force_out
#SBATCH -t 1-00:00:00
#SBATCH --mem-per-cpu=1000
#SBATCH -n 1
#SBATCH -p batch
#SBATCH --array=21
#SBATCH --constraint=opteron

module load python/2.7.4 numpy/1.7.0
pypy brute_force.py $(($SLURM_ARRAY_TASK_ID/8)) $(($SLURM_ARRAY_TASK_ID%8))
