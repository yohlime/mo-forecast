module purge
module load intel

spack env deactivate
spack env activate parallel-openmpi-slurm
spack load netcdf-fortran %intel
spack load parallel-netcdf %intel

export WRFIO_NCD_LARGE_FILE_SUPPORT=1
ulimit -s unlimited
