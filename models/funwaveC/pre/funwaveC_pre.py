"""
Tools to manage funwaveC input

Authors:
--------
Gabriel Garcia Medina (ggarcia@coas.oregonstate.edu)

# Last edit
14 December 2016 - Gabriel Garcia Medina

External dependencies:
  numpy
  scipy
  netCDF4
  time
  sys
  getpass
  os
  collections
  imp

Internal dependencies:
  gsignal
  
"""

from __future__ import division,print_function

__author__ = "Gabriel Garcia Medina"
__email__ = "ggarcia@coas.oregonstate.edu"
__group__="Nearshore Modeling Group"


# Import Modules
import netCDF4
import time
import sys
import getpass
import os
import numpy as np
import pylab as pl
from collections import defaultdict

# Custom paths
import pynmd.physics.waves as gwaves


#===============================================================================
# Pyroms subroutine to write NetCDF fields
#===============================================================================
def create_nc_var(nc, name, dimensions, units=None, longname=None):
    '''
    Not for standalone use
    '''
    nc.createVariable(name, 'f8', dimensions)
    if units is not None:
        nc.variables[name].units = units
    if longname is not None:
        nc.variables[name].long_name = longname    

# Append NetCDF variable        
def append_nc_var(nc,var,name,tstep):
    '''
    Not for standalone use
    '''
    nc.variables[name][tstep,...] = var

# ==================================================================
# Write 1D bathymetry file 
# ==================================================================  
def write_bathy_1d(x,h,path,ncsave=True):
    '''
    
    Parameters:    
    ----------
    x           : 1D array of x coordinates
    h           : Bathymetry
    path        : Full path where the output will be saved
    ncsave      : Save bathy as NetCDF file
    
    Output:
    -------
    depth.txt   : Text file with the depth information for Funwave input.
    depth.nc    : (Optional) NetCDF4 bathymetry file. 
    
    Notes:
    ------
    Variables are assumed to be on a regularly spaced grid.
    
    '''

    # Output the text file -----------------------------------------------------        
    fid = open(path + 'depth.txt','w')
    for aa in range(len(h)):
        fid.write('%12.3f\n' % h[aa])
    fid.close()

    if ncsave:
    
        # Global attributes  
        nc = netCDF4.Dataset(path + 'depth.nc', 'w', format='NETCDF4')
        nc.Description = 'Funwave Bathymetry'
        nc.Author = getpass.getuser()
        nc.Created = time.ctime()
        nc.Owner = 'Nearshore Modeling Group (http://ozkan.oce.orst.edu/nmg)'
        nc.Software = 'Created with Python ' + sys.version
        nc.NetCDF_Lib = str(netCDF4.getlibversion())
        nc.Script = os.path.realpath(__file__)
     
        # Create dimensions
        xi_rho = len(h)
        nc.createDimension('xi_rho', xi_rho)
    
        # Write coordinates and depth to netcdf file
        create_nc_var(nc, 'x_rho',('xi_rho'), 
                     'meter','x-locations of RHO-points')
        nc.variables['x_rho'][:] = x
        create_nc_var(nc,'h',('xi_rho'), 
                     'meter','bathymetry at RHO-points')
        nc.variables['h'][:] = h      
                
        # Close NetCDF file
        nc.close()

    else: 
    
        print("NetCDF file not requested")
        
        

    #===========================================================================
    # Print input file options
    #===========================================================================
    print(' ')
    print('===================================================================')
    print('In your funwaveC init file:')
    print('dimension ' + np.str(len(x)+1) + ' 1 ' +
          np.str(np.abs(x[1] - x[0])) + ' 1')
    print('===================================================================')
    print(' ')
    
    # End of function
    
