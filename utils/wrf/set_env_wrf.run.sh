#!/usr/bin/env bash

module purge
module use /opt/intel/oneapi/modulefiles
module load mpi

export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so
export OMP_NUM_THREADS=$SLURM_WRF_CPUS_PER_TASK

spack env activate intel

ulimit -s unlimited
