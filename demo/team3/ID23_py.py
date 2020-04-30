#
# Python script to run shadow3. Created automatically with ShadowTools.make_python_script_from_list().
#
import Shadow
import numpy

# write (1) or not (0) SHADOW files start.xx end.xx star.xx
iwrite = 0

#
# initialize shadow3 source (oe0) and beam
#
beam = Shadow.Beam()
oe0 = Shadow.Source()
oe1 = Shadow.OE()
oe2 = Shadow.OE()
oe3 = Shadow.OE()
oe4 = Shadow.OE()
oe5 = Shadow.OE()

#
# Define variables. See meaning of variables in: 
#  https://raw.githubusercontent.com/srio/shadow3/master/docs/source.nml 
#  https://raw.githubusercontent.com/srio/shadow3/master/docs/oe.nml
#

oe0.FDISTR = 3
oe0.F_COLOR = 3
oe0.F_PHOT = 0
oe0.F_POLAR = 0
oe0.HDIV1 = 0.0
oe0.HDIV2 = 0.0
oe0.IDO_VX = 0
oe0.IDO_VZ = 0
oe0.IDO_X_S = 0
oe0.IDO_Y_S = 0
oe0.IDO_Z_S = 0
oe0.ISTAR1 = 5676561
oe0.NPOINT = 500000
oe0.PH1 = 14100.0
oe0.PH2 = 14300.0
oe0.SIGDIX = 9.5e-05
oe0.SIGDIZ = 3.1e-06
oe0.SIGMAX = 6.1e-05
oe0.SIGMAZ = 9e-06
oe0.VDIV1 = 0.0
oe0.VDIV2 = 0.0

oe1.DUMMY = 100.0
oe1.FWRITE = 3
oe1.F_REFRAC = 2
oe1.F_SCREEN = 1
oe1.N_SCREEN = 1
oe1.T_IMAGE = 0.0
oe1.T_INCIDENCE = 0.0
oe1.T_REFLECTION = 180.0
oe1.T_SOURCE = 28.2

oe2.DUMMY = 100.0
oe2.FHIT_C = 1
oe2.FILE_REFL = b'/home/aljosa/Oasys/development_sprint/si5_15.111'
oe2.FWRITE = 1
oe2.F_CENTRAL = 1
oe2.F_CRYSTAL = 1
oe2.PHOT_CENT = 14200.0
oe2.RLEN1 = 0.02
oe2.RLEN2 = 0.02
oe2.RWIDX1 = 0.15
oe2.RWIDX2 = 0.15
oe2.R_LAMBDA = 5000.0
oe2.T_IMAGE = 0.0
oe2.T_INCIDENCE = 81.9952066442
oe2.T_REFLECTION = 81.9952066442
oe2.T_SOURCE = 1.8

oe3.DUMMY = 100.0
oe3.FWRITE = 3
oe3.F_REFRAC = 2
oe3.F_SCREEN = 1
oe3.I_SLIT = numpy.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
oe3.N_SCREEN = 1
oe3.RX_SLIT = numpy.array([0.001, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
oe3.RZ_SLIT = numpy.array([0.0008, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
oe3.T_IMAGE = 0.0
oe3.T_INCIDENCE = 0.0
oe3.T_REFLECTION = 180.0
oe3.T_SOURCE = 10.9

oe4.DUMMY = 100.0
oe4.FCYL = 1
oe4.FHIT_C = 1
oe4.FMIRR = 2
oe4.FWRITE = 3
oe4.F_DEFAULT = 0
oe4.RLEN1 = 0.15
oe4.RLEN2 = 0.15
oe4.RWIDX1 = 0.02
oe4.RWIDX2 = 0.02
oe4.SIMAG = 2.1
oe4.SSOUR = 43.15
oe4.THETA = 89.77654645989898
oe4.T_IMAGE = 0.1
oe4.T_INCIDENCE = 89.77654645989898
oe4.T_REFLECTION = 89.77654645989898
oe4.T_SOURCE = 2.25

oe5.ALPHA = 90.0
oe5.DUMMY = 100.0
oe5.FCYL = 1
oe5.FHIT_C = 1
oe5.FMIRR = 2
oe5.FWRITE = 3
oe5.F_DEFAULT = 0
oe5.RLEN1 = 0.15
oe5.RLEN2 = 0.15
oe5.RWIDX1 = 0.02
oe5.RWIDX2 = 0.02
oe5.SIMAG = 1.9
oe5.SSOUR = 43.35
oe5.THETA = 89.77654645989898
oe5.T_IMAGE = 1.9
oe5.T_INCIDENCE = 89.77654645989898
oe5.T_REFLECTION = 89.77654645989898
oe5.T_SOURCE = 0.1



#Run SHADOW to create the source

if iwrite:
    oe0.write("start.00")

beam.genSource(oe0)

if iwrite:
    oe0.write("end.00")
    beam.write("begin.dat")


#
#run optical element 1
#
print("    Running optical element: %d"%(1))
if iwrite:
    oe1.write("start.01")

beam.traceOE(oe1,1)

if iwrite:
    oe1.write("end.01")
    beam.write("star.01")


#
#run optical element 2
#
print("    Running optical element: %d"%(2))
if iwrite:
    oe2.write("start.02")

beam.traceOE(oe2,2)

if iwrite:
    oe2.write("end.02")
    beam.write("star.02")


#
#run optical element 3
#
print("    Running optical element: %d"%(3))
if iwrite:
    oe3.write("start.03")

beam.traceOE(oe3,3)

if iwrite:
    oe3.write("end.03")
    beam.write("star.03")


#
#run optical element 4
#
print("    Running optical element: %d"%(4))
if iwrite:
    oe4.write("start.04")

beam.traceOE(oe4,4)

if iwrite:
    oe4.write("end.04")
    beam.write("star.04")


#
#run optical element 5
#
print("    Running optical element: %d"%(5))
if iwrite:
    oe5.write("start.05")

beam.traceOE(oe5,5)

if iwrite:
    oe5.write("end.05")
    beam.write("star.05")


Shadow.ShadowTools.plotxy(beam,1,3,nbins=101,nolost=1,title="Real space")
# Shadow.ShadowTools.plotxy(beam,1,4,nbins=101,nolost=1,title="Phase space X")
# Shadow.ShadowTools.plotxy(beam,3,6,nbins=101,nolost=1,title="Phase space Z")
    