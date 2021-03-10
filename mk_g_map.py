"""
Calculate probability map.
"""
import numpy as np
import healpy as hp
from astropy.io import fits
from utils import FluxPDF

# global
hp.disable_warnings()
fname_DR2 = "data/LoTSS_DR2_v100.srl.fits"
fname_flux = "data/skads_flux_counts.result"
nside = 256
npix = hp.nside2npix(nside)

data = fits.open(fname_DR2)[1].data
#TODO: remove gals with S<2
ipix = hp.ang2pix(nside, data["RA"], data["DEC"], lonlat=True)

sigmap = np.bincount(ipix, weights=data["Isl_rms"], minlength=npix)
sigmap /= np.bincount(ipix, minlength=npix)
sigmap = np.nan_to_num(sigmap)

fluxes = np.loadtxt(fname_flux, skiprows=1, delimiter=",")

F = FluxPDF()
p_map = F.compute_p_map(q=5, std_map=sigmap, Imin=2)

ngal = np.bincount(ipix, minlength=npix)

n_mean = np.sum(ngal*p_map) / np.sum(p_map)
ngal = p_map*(ngal/(n_mean*p_map) - 1)
ngal = np.nan_to_num(ngal)
# hp.write_map("data/LoTSS_DR2_Delta_g_map.fits", ngal, overwrite=True)
