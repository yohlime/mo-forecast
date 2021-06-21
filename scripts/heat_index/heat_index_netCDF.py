#!/usr/bin/env python
# coding: utf-8

#get the climatological heat index of MO station (2010-2019)
#change initialization and variables for automation
#yyyymmdd and init are in local time (PHT)
#mm = choose climatological month
yyyymmdd = '2021-06-20'
init = '20'
EXTRACT_DIR = '/home/modelman/forecast/scripts/grads/nc'

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt 
from netCDF4 import Dataset
#import cartopy.crs as ccrs

# open netCDF files and extract variables

fname = Path(EXTRACT_DIR) / f'./wrf-rh_{yyyymmdd}_{init}PHT.nc'

rh2 = Dataset(fname)
rh = rh2.variables['rh'][:, :, :]
lats = rh2.variables['lat'][:]
lons = rh2.variables['lon'][:]

fname = Path(EXTRACT_DIR) / f'./wrf-t2_{yyyymmdd}_{init}PHT.nc'

t2 = Dataset(fname)
tas = t2.variables['t'][:, :, :]
lats = t2.variables['lat'][:]
lons = t2.variables['lon'][:]
time = t2.variables['time'][:]

# convert to celsius
tas = tas -273.15

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

nc_attrs, nc_dims, nc_vars = ncdump(t2)

# Calculate heat index:
print("Calculating heat index...")

def calculate_heat_index(t,rh):
    t_fahrenheit = t * (9./5.) + 32

    heat_index_fahrenheit = -42.379 + (2.04901523 * t_fahrenheit) + (10.14333127 * rh) +         (-0.22475541 * t_fahrenheit * rh) + (-0.006837837 * t_fahrenheit * t_fahrenheit) +         (-0.05481717 * rh * rh) + (0.001228747 * t_fahrenheit * t_fahrenheit * rh) +         (0.00085282 * t_fahrenheit * rh * rh) + (-0.00000199 * t_fahrenheit * t_fahrenheit * rh * rh)
    locs = np.ma.where(np.ma.logical_and((rh < 13), (t_fahrenheit > 80), (t_fahrenheit < 112)))
    if len(locs[0]) > 0:
        heat_index_fahrenheit[locs] = heat_index_fahrenheit[locs] - (((13.- rh[locs]) / 4.) * np.ma.sqrt((17. - np.ma.abs(t_fahrenheit[locs] - 95.)) / 17.))
        locs = np.ma.where(np.ma.logical_and((rh > 85), (t_fahrenheit > 80), (t_fahrenheit < 87)))
    if len(locs[0]) > 0:
        heat_index_fahrenheit[locs] = heat_index_fahrenheit[locs] - (((rh[locs ] - 85) / 10.) * ((87. - t_fahrenheit[locs]) / 5.))
    
    locs = np.ma.where(heat_index_fahrenheit < 80)
    if len(locs[0]) > 0:
        heat_index_fahrenheit[locs] = 0.5 * (t_fahrenheit[locs] + 61. + ((t_fahrenheit[locs] - 68.) * 1.2) + (rh[locs] * 0.094))
 
    heat_index = (heat_index_fahrenheit - 32) / (9./5.)

#    locs = np.ma.where(t < 26.6667) # 80F
#    if len(locs[0]) > 0:
#        heat_index[locs] = -99
#    locs = np.ma.where(rh < 40.0)
#    if len(locs[0]) > 0:
#        heat_index[locs] = -99
    return heat_index

HI=calculate_heat_index(tas[:,:,:],rh[:,:,:])
#HI= np.where(HI== -99., np.nan,HI)

#save heat_index plot as netCDF file
print("Saving heat index to netCDF file...")
w_nc_fid = Dataset(Path(EXTRACT_DIR) / f'./wrf-HI_{yyyymmdd}_{init}PHT.nc', 'w', format='NETCDF4')
w_nc_fid.description = "Heat Index calculated from WRF simulation"
# Using our previous dimension information, we can create the new dimensions
data = {}
for dim in nc_dims:
    w_nc_fid.createDimension(dim, t2.variables[dim].size)
    data[dim] = w_nc_fid.createVariable(dim, t2.variables[dim].dtype, (dim,))
    # You can do this step yourself but someone else did the work for us.
    for ncattr in t2.variables[dim].ncattrs():
        data[dim].setncattr(ncattr, t2.variables[dim].getncattr(ncattr))
# Assign the dimension data to the new NetCDF file.
w_nc_fid.variables['time'][:] = time
w_nc_fid.variables['lat'][:] = lats
w_nc_fid.variables['lon'][:] = lons

# Ok, time to create our departure variable
w_nc_var = w_nc_fid.createVariable('hi', 'f8', ('time', 'lat', 'lon'))
w_nc_var.setncatts({'long_name': u"Heat Index from RH and T2 (WRF)",\
        'units': u"degC", 'level_desc': u'Surface',\
        'var_desc': u"Heat Index\n"})
w_nc_fid.variables['hi'][:] = HI
w_nc_fid.close()  # close the new file

print("Done!")
