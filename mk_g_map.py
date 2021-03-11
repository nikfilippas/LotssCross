"""
Calculate probability map.
"""
import numpy as np
import healpy as hp
from astropy.io import fits
from utils import FluxPDF

# global
hp.disable_warnings()
fname_DR2 = "data/maps/LoTSS/LoTSS_DR2_v100.srl.fits"
fname_flux = "data/nz/skads_flux_counts.result"
nside = 512
npix = hp.nside2npix(nside)

data = fits.open(fname_DR2)[1].data
data = data[data["Total_flux"] >= 2]  # flux cut
ipix = hp.ang2pix(nside, data["RA"], data["DEC"], lonlat=True)

sigmap = np.bincount(ipix, weights=data["Isl_rms"], minlength=npix)
sigmap /= np.bincount(ipix, minlength=npix)
sigmap = np.nan_to_num(sigmap)

# fluxes = np.loadtxt(fname_flux, skiprows=1, delimiter=",")

F = FluxPDF(fname_flux)
p_map = F.compute_p_map(q=5, std_map=sigmap, Imin=2)

ngal = np.bincount(ipix, minlength=npix)

n_mean = np.sum(ngal*p_map) / np.sum(p_map)
ngal = p_map*(ngal/(n_mean*p_map) - 1)
ngal = np.nan_to_num(ngal)
# hp.write_map("data/maps/LoTSS/LoTSS_DR2_pmap.fits", p_map, overwrite=True)
# hp.write_map("data/maps/LoTSS/LoTSS_DR2_Delta_g_map2.fits", ngal, overwrite=True)
