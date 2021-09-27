module purge
module use /opt/intel/oneapi/modulefiles
module load mpi compiler

export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so
export I_MPI_CC=icc
export I_MPI_CXX=icpc
export I_MPI_FC=ifort
export I_MPI_F77=ifort
export I_MPI_F90=ifort

export OMP_NUM_THREADS=$SLURM_WRF_CPUS_PER_TASK

spack env deactivate
spack env activate intel
spack load netcdf-fortran %intel
spack load parallel-netcdf %intel
spack load jasper %intel

ulimit -s unlimited
