#!/usr/bin/env bash

export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so
export OMP_NUM_THREADS=$SLURM_WRF_CPUS_PER_TASK

spack env activate intel
spack load intel-oneapi-mpi

ulimit -s unlimited
