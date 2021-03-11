"""Rotate Planck lensing map."""
import healpy as hp

fname = "data/COM_Lensing_Szdeproj_4096_R3.00_TT_dat_klm.fits"

R = hp.rotator.Rotator(coord=["G", "C"])
alm = hp.read_alm(fname)
alm_rot = R.rotate_alm(alm)

hp.write_alm("lensing_szdeproj_alm.fits", alm_rot, overwrite=True)
