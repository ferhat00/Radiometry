# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 10:07:43 2017

This is the main code to run for calculating the expected signal from a
target with Lambertian response. Inputs are:
    
planck_source.py - Planck body source assumed. Temperature is set here
imager.py - characteristice of the imager, add inputs and variables here
detector.py - detector characteristic inputs here

This function, radiance.py you input orbital and sun parameters    

@author: fculfaz
"""

import planck_source
import imager
import detector
import math
import numpy as np
import matplotlib.pyplot as plt


solar_solid_angle = 6.80e-05 # Constant - sr

# Mission specific constants one can modify
albedo = 0.8 # constant
latitude = 45 # degrees
LTAN = 10.5 # hours

# Physical Constants
h = planck_source.h()
c = planck_source.c()

# Light source colour temperature, assuming Planck black body source
T = 5770

# - Constants and functions imported from other python files
QE_response_interpolated = detector.QE_response_interpolated()
active_pixel_area = detector.active_pixel_area()
integration_time = imager.integration_time()
full_well_capacity = detector.full_well_capacity()
effective_aperture = imager.effective_aperture()
focal_length = imager.focal_length()
lens_transmission = imager.lens_transmission()
filter_response_interpolated = imager.filter_response_interpolated()
wavelengths = np.arange(400e-9, 1e-6, 1e-9)

# Begin calculating radiometry
solar_spectral_radiance = planck_source.planck(wavelengths, T) * 1e-9 * 0.0001 # W cm-2 sr-1 nm-1
solar_irradiance = solar_solid_angle * solar_spectral_radiance * 1 * 1e6 # (µW.cm-2)
radiance = solar_irradiance * math.cos(latitude*(math.pi/180))*math.cos((12-LTAN)*(math.pi)/12)/math.pi # (µW.cm-2.sr-1)
photon_energy = (h * c / wavelengths) * 1e6 # uJ
photon_radiance = radiance/photon_energy # ph.s-1.cm-2.sr-1
signal = photon_radiance*(active_pixel_area*0.01)*(effective_aperture*0.01)/((focal_length/10)**2)*integration_time*QE_response_interpolated*lens_transmission*filter_response_interpolated
                         
# Plot graphs                         
plt.plot(wavelengths*1e9, signal)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Signal (e-)')
plt.show()                         

# Print out results
total_signal = np.sum(signal)*math.cos(latitude*math.pi/180)/math.pi
percent_FWC = total_signal/full_well_capacity *100                     
print('Total Signal =  {0:.3f}.' .format(total_signal))
print('Full Well Capacity =  {0:.3f}%' .format(percent_FWC))