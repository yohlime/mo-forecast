#!/usr/bin/env python
# coding: utf-8

yyyymmdd = '2021-09-07'
init = '20'
IN_DIR = '/home/modelman/forecast/model/ENSEMBLE'
OUT_DIR = '/home/modelman/forecast/scripts/rainchance/nc'

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patch
import datetime as dt 
from netCDF4 import Dataset
#import cartopy.crs as ccrs

for day in range(1,6):
    var = 24*day
    # open netCDF files and extract variables
    fname = Path(IN_DIR) / f'./mowcr_solar_run1/wrf-day{day}_{yyyymmdd}_{init}PHT.nc'

    d1 = Dataset(fname)
    rain1 = d1.variables[f'p{var}'][:, :]
    lats1 = d1.variables['lat'][:]
    lons1 = d1.variables['lon'][:]

    fname = Path(IN_DIR) / f'./mowcr_solar_run2/wrf-day{day}_{yyyymmdd}_{init}PHT.nc'

    d2 = Dataset(fname)
    rain2 = d2.variables[f'p{var}'][:, :]
    lats2 = d2.variables['lat'][:]
    lons2 = d2.variables['lon'][:]

    fname = Path(IN_DIR) / f'./mowcr_solar_run3/wrf-day{day}_{yyyymmdd}_{init}PHT.nc'

    d3 = Dataset(fname)
    rain3 = d3.variables[f'p{var}'][:, :]
    lats3 = d3.variables['lat'][:]
    lons3 = d3.variables['lon'][:]

    # ncdump function
    def ncdump(nc_fid, verb=True):
        '''
        ncdump outputs dimensions, variables and their attribute information.
        The information is similar to that of NCAR's ncdump utility.
        ncdump requires a valid instance of Dataset.

        Parameters
        ----------
        nc_fid : netCDF4.Dataset
            A netCDF4 dateset object
        verb : Boolean
            whether or not nc_attrs, nc_dims, and nc_vars are printed

        Returns
        -------
        nc_attrs : list
            A Python list of the NetCDF file global attributes
        nc_dims : list
            A Python list of the NetCDF file dimensions
        nc_vars : list
            A Python list of the NetCDF file variables
        '''
        def print_ncattr(key):
            """
            Prints the NetCDF file attributes for a given key

            Parameters
            ----------
            key : unicode
                a valid netCDF4.Dataset.variables key
            """
            try:
                print ("\t\ttype:", repr(nc_fid.variables[key].dtype))
                for ncattr in nc_fid.variables[key].ncattrs():
                    print ('\t\t%s:' % ncattr, repr(nc_fid.variables[key].getncattr(ncattr)))
            except KeyError:
                print ("\t\tWARNING: %s does not contain variable attributes" % key)

        # NetCDF global attributes
        nc_attrs = nc_fid.ncattrs()
        if verb:
            print ("NetCDF Global Attributes:")
            for nc_attr in nc_attrs:
                print ('\t%s:' % nc_attr, repr(nc_fid.getncattr(nc_attr)))
        nc_dims = [dim for dim in nc_fid.dimensions]  # list of nc dimensions
        # Dimension shape information.
        if verb:
            print ("NetCDF dimension information:")
            for dim in nc_dims:
                print ("\tName:", dim )
                print ("\t\tsize:", len(nc_fid.dimensions[dim]))
                print_ncattr(dim)
        # Variable information.
        nc_vars = [var for var in nc_fid.variables]  # list of nc variables
        if verb:
            print ("NetCDF variable information:")
            for var in nc_vars:
                if var not in nc_dims:
                    print ('\tName:', var)
                    print ("\t\tdimensions:", nc_fid.variables[var].dimensions)
                    print ("\t\tsize:", nc_fid.variables[var].size)
                    print_ncattr(var)
        return nc_attrs, nc_dims, nc_vars

    # Get all netCDF atributes, dimensions, variables:
    nc_attrs, nc_dims, nc_vars = ncdump(d1)
    
    #------------------------------------------------#
    #          CHANCE OF RAIN FROM ENSEMBLE          #
    #------------------------------------------------#

    print(f"Getting chance of rain from ensemble day {day}")

    def calculate_chanceofrain(run1,run2,run3):
        chance = run1*0
        # threshold 0.2mm
        locs = np.ma.where(np.ma.logical_and((run1 <= 0.2), (run2 <= 0.2),(run2 <= 0.2))) # no rain
        if len(locs[0]) > 0: 
            chance[locs] = 0
        locs = np.ma.where(np.ma.logical_and((run1 > 0.2), (run2 <= 0.2),(run2 <= 0.2))) # run1 rain
        if len(locs[0]) > 0:
            chance[locs] = 1
        locs = np.ma.where(np.ma.logical_and((run1 <= 0.2), (run2 > 0.2),(run2 <= 0.2))) # run2 rain
        if len(locs[0]) > 0:
            chance[locs] = 1
        locs = np.ma.where(np.ma.logical_and((run1 <= 0.2), (run2 <= 0.2),(run2 > 0.2))) # run3 rain
        if len(locs[0]) > 0:
            chance[locs] = 1
        locs = np.ma.where(np.ma.logical_and((run1 > 0.2), (run2 > 0.2),(run2 <= 0.2))) # run1&2 rain
        if len(locs[0]) > 0:
            chance[locs] = 2
        locs = np.ma.where(np.ma.logical_and((run1 <= 0.2), (run2 > 0.2),(run2 > 0.2))) # run2&3 rain
        if len(locs[0]) > 0:
            chance[locs] = 2
        locs = np.ma.where(np.ma.logical_and((run1 > 0.2), (run2 <= 0.2),(run2 > 0.2))) # run1&3 rain
        if len(locs[0]) > 0:
            chance[locs] = 2
        locs = np.ma.where(np.ma.logical_and((run1 > 0.2), (run2 > 0.2),(run2 > 0.2))) # all rain
        if len(locs[0]) > 0:
            chance[locs] = 3

        return chance

    CHANCE=calculate_chanceofrain(rain1[:,:],rain2[:,:],rain3[:,:])

    # save chance of rain as netCDF file
    print("Saving chance of rain to netCDF file...")
    w_nc_fid = Dataset(Path(OUT_DIR) / f'./rainchance_day{day}_{yyyymmdd}_{init}PHT.nc', 'w', format='NETCDF4')
    w_nc_fid.description = "Chance of rain calculated from 3 WRF ensemble members"
    # Using our previous dimension information, we can create the new dimensions
    data = {}
    for dim in nc_dims:
        w_nc_fid.createDimension(dim, d1.variables[dim].size)
        data[dim] = w_nc_fid.createVariable(dim, d1.variables[dim].dtype, (dim,))
        # You can do this step yourself but someone else did the work for us.
        for ncattr in d1.variables[dim].ncattrs():
            data[dim].setncattr(ncattr, d1.variables[dim].getncattr(ncattr))
    # Assign the dimension data to the new NetCDF file.
    #w_nc_fid.variables['time'][:] = time
    w_nc_fid.variables['lat'][:] = lats1
    w_nc_fid.variables['lon'][:] = lons1

    # Ok, time to create our departure variable
    w_nc_var = w_nc_fid.createVariable('chance', 'f8', ('lat', 'lon'))
    w_nc_var.setncatts({'long_name': u"Chance of Rain (3 WRF ensemble Members)",\
            'units': u"1", 'level_desc': u'Surface',\
            'var_desc': u"Chance of Rain\n"})
    w_nc_fid.variables['chance'][:] = CHANCE
    w_nc_fid.close()  # close the new file

print("Done!")
