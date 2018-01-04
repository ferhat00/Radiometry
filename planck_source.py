# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 08:19:01 2017

@author: fculfaz
"""

import matplotlib.pyplot as plt
import numpy as np

_h = 6.626e-34
_c = 3.0e+8
_k = 1.38e-23

def h():
    return _h

def c():
    return _c

def k():
    return _k


def planck(wav, T):
    a = 2.0*_h*_c**2
    b = _h*_c/(wav*_k*T)
    intensity = a/ ( (wav**5) * (np.exp(b) - 1.0) )
    return intensity

# generate x-axis in increments from 1nm to 3 micrometer in 1 nm increments
# starting at 1 nm to avoid wav = 0, which would result in division by zero.
wavelengths = np.arange(400e-9, 1e-6, 1e-9) 

# intensity at 4000K, 5000K, 6000K, 7000K
intensity4000 = planck(wavelengths, 4000.)
intensity5000 = planck(wavelengths, 5000.)
intensity6000 = planck(wavelengths, 6000.)
intensity7000 = planck(wavelengths, 7000.)

plt.hold(True) # doesn't erase plots on subsequent calls of plt.plot()
plt.plot(wavelengths*1e9, intensity4000*1e-9*0.0001, 'r-', label="4000K") # plot intensity4000 versus wavelength in nm as a red line
plt.plot(wavelengths*1e9, intensity5000*1e-9*0.0001, 'g-', label="5000K") # 5000K green line
plt.plot(wavelengths*1e9, intensity6000*1e-9*0.0001, 'b-', label="6000K") # 6000K blue line
plt.plot(wavelengths*1e9, intensity7000*1e-9*0.0001, 'k-', label="7000K") # 7000K black line
plt.xlabel('Wavelength (nm)')
plt.ylabel('Spectral Radiance (W cm-2 sr-1 nm-1)')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

# show the plot
plt.show()