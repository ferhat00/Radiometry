# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 10:48:12 2017

Detector inputs for use in radiance.py
QE response file imported from csv file

@author: fculfaz
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d

# Assumes Mikrtotron MC1302 detector Contsants inputted here

_pixel_size = 0.012 # mm
_pixel_area = _pixel_size * _pixel_size
fill_factor = 0.4 # constant
_active_pixel_area = _pixel_area*fill_factor

_full_well_capacity = 63000

def active_pixel_area():
    return _active_pixel_area

def full_well_capacity():
    return _full_well_capacity

def pixel_size():
    return _pixel_size


"""
Now determine the QE response of the detector, based on discrete 
inputs that are imported from the csv file, 'QE_response.csv'. Then
interpolate this to get it in 1nm steps and input interpolated result into
an array.

 """
 
wavelengths = np.arange(400e-9, 1e-6, 1e-9)
QE_response= pd.read_csv('detector_QE.csv',encoding = "ISO-8859-1")
f = interp1d(QE_response['Wavelength'], QE_response['Response'])
f2 = interp1d(QE_response['Wavelength'], QE_response['Response'], kind='cubic')
xnew = np.arange(400, 1000, 1)

# Plot the QE response
plt.plot(QE_response['Wavelength'], QE_response['Response'], 'o', xnew, f(xnew), '-', xnew, f2(xnew), '--')
plt.legend(['data', 'linear', 'cubic'], loc='best')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Detector QE Response')
plt.show()
_QE_response_interpolated = f2(wavelengths*1e9)

def QE_response_interpolated():
    return _QE_response_interpolated
