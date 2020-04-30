import os,shutil
from SimEx.Calculators.GAPDPhotonDiffractor import GAPDPhotonDiffractor
from SimEx.Parameters.GAPDPhotonDiffractorParameters import GAPDPhotonDiffractorParameters
from SimEx.Parameters.DetectorGeometry import DetectorGeometry, DetectorPanel
from SimEx.Parameters.PhotonBeamParameters import PhotonBeamParameters
from SimEx.Utilities.Units import meter, electronvolt, joule, radian

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import cm

# Detector setup

detector_panel = DetectorPanel(
            ranges={
                'fast_scan_min': 0,
                'fast_scan_max': 200,
                'slow_scan_min': 0,
                'slow_scan_max': 200
            },
            pixel_size=2200e-6 * meter,
            photon_response=1.0,
            distance_from_interaction_plane=0.25 * meter,
            corners={
                'x': -100,
                'y': -100
            },
        )
detector_geometry = DetectorGeometry(panels=[detector_panel])

# Polychromatic beam setup

beam = './raytracing_out.h5'

# Sample preparation

response = requests.get('https://cdn.rcsb.org/images/rutgers/wu/3wul/3wul.pdb1-500.jpg')

# Diffractor setup

outfile = 'diffr_poly_1.txt'

parameters = GAPDPhotonDiffractorParameters(
            detector_geometry=detector_geometry,
            beam_parameters=beam,
            number_of_spectrum_bins = 100)

diffractor = GAPDPhotonDiffractor(parameters=parameters,
                                          input_path='single-cu.xyz',
                                          output_path=outfile)

diffractor.backengine()

# Plot

plt.figure('Spectrum')
spec = np.loadtxt('spectrum.txt')
plt.plot(spec[:,0],spec[:,1])

data = np.loadtxt(outfile,ndmin=2)
print (data.shape)
fig = plt.figure(figsize=(10,5))
plt.imshow(data,
           vmax = 0.5,
           cmap=cm.jet)
plt.colorbar()

data = np.loadtxt(outfile,ndmin=2)
print (data.shape)
fig = plt.figure(figsize=(10,5))
plt.imshow(data,
           vmax = 0.5,
           cmap=cm.jet,
           norm=colors.LogNorm(vmin=data.min(), vmax=data.max())
          )
plt.colorbar()
plt.show()
