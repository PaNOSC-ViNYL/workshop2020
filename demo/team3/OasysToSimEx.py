import openpmd_api as api
import time
import datetime
import numpy as np
from numpy.random import random

def saveShadowToHDF(filename='output.h5', oasysRaysObject=in_object_1):
    '''
    Beam.getshonecol(colNo)
    Extract a column from a shadow file (eg. begin.dat) or a Shadow.Beam instance.
    The column are numbered in the fortran convention, i.e. starting from 1.
    It returns a numpy.array filled with the values of the chosen column.

    Inumpy.ts:
       beam     : str instance with the name of the shadow file to be loaded. OR
                  Shadow.Beam initialized instance.
       col      : int for the chosen columns.

    Outputs:
       numpy.array 1-D with length numpy.INT.

    Error:
       if an error occurs an ArgsError is raised.

    Possible choice for col are:
             1   X spatial coordinate [user's unit]
             2   Y spatial coordinate [user's unit]
             3   Z spatial coordinate [user's unit]
             4   Xp direction or divergence [rads]
             5   Yp direction or divergence [rads]
             6   Zp direction or divergence [rads]
             7   X component of the electromagnetic vector (s-polariz)
             8   Y component of the electromagnetic vector (s-polariz)
             9   Z component of the electromagnetic vector (s-polariz)
            10   Lost ray flag
            11   Energy [eV]
            12   Ray index
            13   Optical path length
            14   Phase (s-polarization) in rad
            15   Phase (p-polarization) in rad
            16   X component of the electromagnetic vector (p-polariz)
            17   Y component of the electromagnetic vector (p-polariz)
            18   Z component of the electromagnetic vector (p-polariz)
            19   Wavelength [A]
            20   R= SQRT(X^2+Y^2+Z^2)
            21   angle from Y axis
            22   the magnitude of the Electromagnetic vector
            23   |E|^2 (total intensity)
            24   total intensity for s-polarization
            25   total intensity for p-polarization
            26   K = 2 pi / lambda [A^-1]
            27   K = 2 pi / lambda * col4 [A^-1]
            28   K = 2 pi / lambda * col5 [A^-1]
            29   K = 2 pi / lambda * col6 [A^-1]
            30   S0-stokes = |Es|^2 + |Ep|^2
            31   S1-stokes = |Es|^2 - |Ep|^2
            32   S2-stokes = 2 |Es| |Ep| cos(phase_s-phase_p)
            33   S3-stokes = 2 |Es| |Ep| sin(phase_s-phase_p)
            34   Power = intensity(col 23) * energy (col 11)
            35   Angle-X with Y: |arcsin(X')|
            36   Angle-Z with Y: |arcsin(Z')|
            37   Angle-X with Y: |arcsin(X') - mean(arcsin(X'))|
            38   Angle-Z with Y: |arcsin(Z') - mean(arcsin(Z'))|
    '''

    SCALAR = api.Mesh_Record_Component.SCALAR
    oasysRays = oasysRaysObject._beam
    unit = workspace_units_to_cm # Conversion to cm
       
    #Unit_Dimension: length L, mass M, time T, electric current I, thermodynamic temperature theta, amount of substance N, luminous intensity J
    
    series = api.Series(filename, api.Access_Type.create)
    
    # get date
    dateNow = time.strftime('%Y-%m-%d %H:%M:%S %z', time.localtime())
    
    # default series settings
    print("Default settings:")
    print("basePath: ", series.base_path)
    print("openPMD version: ", series.openPMD)
    print("iteration format: ", series.iteration_format)

    # openPMD standard
    series.set_openPMD("1.1.0")
    series.set_openPMD_extension(0)
    series.set_author("Aljosa Hafner <aljosa.hafner@ceric-eric.eu>")

    series.set_date(dateNow)
    series.set_software("OASYS", "1.2")
    series.set_comment("Example output from ShadowOui widget in OASYS.")

    series.set_particles_path("rays")

    # new iteration
    cur_it = series.iterations[0]

    nRays = oasysRays.nrays()

    rays = cur_it.particles['0']

    # id
    id = oasysRays.getshonecol(12)
    d = api.Dataset(id.dtype, id.shape)
    rays["id"][SCALAR].reset_dataset(d)
    rays["id"][SCALAR].store_chunk(id)

    # Position 
    position_x = oasysRays.getshonecol(1)
    position_y = oasysRays.getshonecol(2)
    position_z = oasysRays.getshonecol(3)
        
    # Position in [m]
    d = api.Dataset(position_x.dtype, position_x.shape)
    rays["position"]["x"].reset_dataset(d)
    rays["position"]["x"].set_unit_SI(unit/1e2)
    rays["position"]["y"].reset_dataset(d)
    rays["position"]["y"].set_unit_SI(unit/1e2)
    rays["position"]["z"].reset_dataset(d)
    rays["position"]["z"].set_unit_SI(unit/1e2)
    rays["position"].set_unit_dimension({api.Unit_Dimension.L: 1.0})
    rays["position"]["x"].store_chunk(position_x)
    rays["position"]["y"].store_chunk(position_y)
    rays["position"]["z"].store_chunk(position_z)

    # Direction
    direction_x = oasysRays.getshonecol(4)
    direction_y = oasysRays.getshonecol(5)
    direction_z = oasysRays.getshonecol(6)

    # Direction in [rad]
    d = api.Dataset(direction_x.dtype, direction_x.shape)
    rays["direction"]["x"].reset_dataset(d)
    rays["direction"]["x"].set_unit_SI(1.0)
    rays["direction"]["y"].reset_dataset(d)
    rays["direction"]["y"].set_unit_SI(1.0)
    rays["direction"]["z"].reset_dataset(d)
    rays["direction"]["z"].set_unit_SI(1.0)
    rays["direction"]["x"].store_chunk(direction_x)
    rays["direction"]["y"].store_chunk(direction_y)
    rays["direction"]["z"].store_chunk(direction_z)

    # Polarization of E-field, S-polarization
    sPol_x = oasysRays.getshonecol(7)
    sPol_y = oasysRays.getshonecol(8)
    sPol_z = oasysRays.getshonecol(9)

    # S-polarization in [unitless]
    d = api.Dataset(sPol_x.dtype, sPol_x.shape)
    rays["eFieldSPolarisation"]["x"].reset_dataset(d)
    rays["eFieldSPolarisation"]["x"].set_unit_SI(1.0)
    rays["eFieldSPolarisation"]["y"].reset_dataset(d)
    rays["eFieldSPolarisation"]["y"].set_unit_SI(1.0)
    rays["eFieldSPolarisation"]["z"].reset_dataset(d)
    rays["eFieldSPolarisation"]["z"].set_unit_SI(1.0)
    rays["eFieldSPolarisation"]["x"].store_chunk(sPol_x)
    rays["eFieldSPolarisation"]["y"].store_chunk(sPol_y)
    rays["eFieldSPolarisation"]["z"].store_chunk(sPol_z)

    # Polarization of E-field, P-polarization
    pPol_x = oasysRays.getshonecol(16)
    pPol_y = oasysRays.getshonecol(17)
    pPol_z = oasysRays.getshonecol(18)

    # P-polarization in [unitless]
    d = api.Dataset(pPol_x.dtype, pPol_x.shape)
    rays["eFieldPPolarisation"]["x"].reset_dataset(d)
    rays["eFieldPPolarisation"]["x"].set_unit_SI(1.0)
    rays["eFieldPPolarisation"]["y"].reset_dataset(d)
    rays["eFieldPPolarisation"]["y"].set_unit_SI(1.0)
    rays["eFieldPPolarisation"]["z"].reset_dataset(d)
    rays["eFieldPPolarisation"]["z"].set_unit_SI(1.0)
    rays["eFieldPPolarisation"]["x"].store_chunk(pPol_x)
    rays["eFieldPPolarisation"]["y"].store_chunk(pPol_y)
    rays["eFieldPPolarisation"]["z"].store_chunk(pPol_z)

    # Photon energy [1.602176634e−19 eV = J = kg m^2 s^-2]
    energy = oasysRays.getshonecol(11)
    d = api.Dataset(energy.dtype, energy.shape)
    rays["photonEnergy"][SCALAR].reset_dataset(d)
    rays["photonEnergy"][SCALAR].set_unit_SI(1.602176634e-19)
    rays["photonEnergy"].set_unit_dimension({api.Unit_Dimension.L: 2.,
                                             api.Unit_Dimension.M: 1.,
                                             api.Unit_Dimension.T: -2.})
    rays["photonEnergy"][SCALAR].store_chunk(energy)

    # Photon wavelength [A]
    wavelength = oasysRays.getshonecol(19)
    d = api.Dataset(wavelength.dtype, wavelength.shape)
    rays["photonWavelength"][SCALAR].reset_dataset(d)
    rays["photonWavelength"][SCALAR].set_unit_SI(1e-10)
    rays["photonWavelength"].set_unit_dimension({api.Unit_Dimension.L: 1.})
    rays["photonWavelength"][SCALAR].store_chunk(wavelength)

    # Phase for S-polarized and P-polarized photons
    phase_sPol_r = oasysRays.getshonecol(14)
    phase_pPol_r = oasysRays.getshonecol(15)

    # Phase [rad]
    d = api.Dataset(phase_sPol_r.dtype, phase_sPol_r.shape)
    rays["phase"]["sPol_r"].reset_dataset(d)
    rays["phase"]["sPol_r"].set_unit_SI(1.0)
    rays["phase"]["pPol_r"].reset_dataset(d)
    rays["phase"]["pPol_r"].set_unit_SI(1.0)
    rays["phase"]["sPol_r"].store_chunk(phase_sPol_r)
    rays["phase"]["pPol_r"].store_chunk(phase_pPol_r)
    
    # Total intensity [unitless]
    intensity = oasysRays.getshonecol(23)
    d = api.Dataset(intensity.dtype, intensity.shape)
    rays["totalIntensity"][SCALAR].reset_dataset(d)
    rays["totalIntensity"][SCALAR].set_unit_SI(1.0)
    rays["totalIntensity"][SCALAR].store_chunk(intensity)
    
    # Lost rays
    lost_ray = oasysRays.getshonecol(10)
    d = api.Dataset(intensity.dtype, intensity.shape)
    rays["lostRay"][SCALAR].reset_dataset(d)
    rays["lostRay"][SCALAR].set_unit_SI(1.0)
    rays["lostRay"][SCALAR].store_chunk(intensity)
    
    series.flush()
        
    del series

saveShadowToHDF()
