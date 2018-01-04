# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 10:52:42 2017

Imager characteristice is put here. Imports filter response from csv file.
Outputs to radiance.py.

@author: fculfaz
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d
import detector

# Fixed physical constants
earth_radius = 6378135 # m
G = 6.67e-11 # m3.kg-1.s-2 - Gravitational Constant
M = 5.97e24 # kg - Mass of Earth
inclination = 98.131 # degrees



# Constants to manipulate here
aperture_diameter = 2.07 # mm
_focal_length = 12 # mm
_effective_aperture = (math.pi / 4) * (aperture_diameter**2) # mm2
_lens_transmission = 0.8
_integration_time = 0.005 #s

# Not used here, but can bet if simulate imaging earth:
pixel_size = detector.pixel_size()    
orbit_height = 350000 # m
gsd = ((pixel_size/1000)*orbit_height)/(_focal_length/1000) # m
orbit_period = 2*math.pi*math.sqrt((earth_radius+orbit_height)**3/(G*M))
ground_velocity = 2*math.pi*(earth_radius/orbit_period)+((2*math.pi*earth_radius/(24*60*60))*math.sin((inclination-90)*(math.pi)/180)) # s
_integration_time_fly = gsd/ground_velocity
    

def effective_aperture():
    return _effective_aperture

def focal_length():
    return _focal_length

def lens_transmission():
    return _lens_transmission

def integration_time():
    return _integration_time

def integration_time_fly():
    return _integration_time_fly

f_number = _focal_length/aperture_diameter # Not used here

"""
Now determine the filter response on the camera or lens, based on discrete 
inputs that are imported from the csv file, 'filter_response.csv'. Then
interpolate this to get it in 1nm steps and input interpolated result into
an array.

 """

wavelengths = np.arange(400e-9, 1e-6, 1e-9)
filter_response= pd.read_csv('filter_response.csv',encoding = "ISO-8859-1")
f = interp1d(filter_response['Wavelength'], filter_response['Response'])
f2 = interp1d(filter_response['Wavelength'], filter_response['Response'], kind='cubic')
xnew = np.arange(400, 1000, 1)

# Plot the filter response
plt.plot(filter_response['Wavelength'], filter_response['Response'], 'o', xnew, f(xnew), '-', xnew, f2(xnew), '--')
plt.legend(['data', 'linear', 'cubic'], loc='best')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Filter Response')
plt.show()
_filter_response_interpolated = f2(wavelengths*1e9)

def filter_response_interpolated():
    return _filter_response_interpolated