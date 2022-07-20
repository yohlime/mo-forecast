#!/usr/bin/env bash

module purge
module use /opt/intel/oneapi/modulefiles
module load mpi compiler

export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so
export I_MPI_CC=icc
export I_MPI_CXX=icpc
export I_MPI_FC=ifort
export I_MPI_F77=ifort
export I_MPI_F90=ifort

spack env deactivate
spack env activate intel
spack load netcdf-fortran %intel
spack load parallel-netcdf %intel

export WRFIO_NCD_LARGE_FILE_SUPPORT=1

PNG=$(spack location -i libpng %intel)
ZLIB=$(spack location -i zlib %intel)
HDF5=$(spack location -i hdf5 %intel)
NETCDF=$(spack location -i netcdf-fortran %intel)
PNETCDF=$(spack location -i parallel-netcdf %intel)

export PNG
export ZLIB
export HDF5
export NETCDF
export PNETCDF

JASPERLIB="$(spack location -i jasper %intel)/lib -L${PNG}/lib -L${ZLIB}/lib"
JASPERINC="$(spack location -i jasper %intel)/include -I${PNG}/include -I${ZLIB}/include"

export JASPERLIB
export JASPERINC
