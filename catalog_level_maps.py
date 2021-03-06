import numpy as np
from astropy.io import fits
import healpy as hp
import os
import matplotlib.pyplot as plt

from utils import plot_lotss_map, Pointings

# Read catalog
cat = fits.open("data/radio_catalog.fits")[1].data

nside = 256
npix = hp.nside2npix(nside)
ipix = hp.ang2pix(nside, np.radians(90-cat['DEC']), np.radians(cat['RA']))


# Number counts map
if not os.path.isfile(f"outputs/map_n_{nside}.fits"):
    map_n = np.bincount(ipix, minlength=npix)
    hp.write_map(f"outputs/map_n_{nside}.fits", map_n, overwrite=True)
else:
    map_n = hp.read_map(f"outputs/map_n_{nside}.fits", verbose=False)


# Low-res masks
pt = Pointings()
msk_pt = np.zeros(npix, dtype=bool)
msk_p = np.zeros(npix, dtype=bool)
msk_d = np.zeros(npix, dtype=bool)
for p in pt.pointings:
    v = hp.ang2vec(p['RA'], p['DEC'], lonlat=True)
    pix = hp.query_disc(nside=nside, vec=v, radius=np.radians(1.7))
    msk_pt[pix] = 1
    if p['name'] not in pt.bad_pointings['name']:
        msk_p[pix] = 1
msk_d = msk_p & (map_n > 5)
hp.write_map(f"outputs/mask_pt_{nside}.fits", msk_pt, overwrite=True)
hp.write_map(f"outputs/mask_p_{nside}.fits", msk_p, overwrite=True)
hp.write_map(f"outputs/mask_d_{nside}.fits", msk_d, overwrite=True)


# RMS noise and error maps
if not os.path.isfile(f"outputs/map_rms_median_{nside}.fits"):
    mean_error = np.zeros(npix)
    median_error = np.zeros(npix)
    mean_rms = np.zeros(npix)
    median_rms = np.zeros(npix)
    pix_unique = np.unique(ipix)
    for i, ip in enumerate(pix_unique):
        if i % 100 == 0:
            print(i, len(pix_unique), ip)
        sc = cat[ipix == ip]
        mean_error[ip] = np.mean(sc['E_Peak_flux'])
        median_error[ip] = np.median(sc['E_Peak_flux'])
        mean_rms[ip] = np.mean(sc['Isl_rms'])
        median_rms[ip] = np.median(sc['Isl_rms'])
    hp.write_map(f"outputs/map_rms_mean_{nside}.fits", mean_rms,
                 overwrite=True)
    hp.write_map(f"outputs/map_rms_median_{nside}.fits", median_rms,
                 overwrite=True)
    hp.write_map(f"outputs/map_error_mean_{nside}.fits", mean_error,
                 overwrite=True)
    hp.write_map(f"outputs/map_error_median_{nside}.fits", median_error,
                 overwrite=True)
else:
    mean_rms = hp.read_map(f"outputs/map_rms_mean_{nside}.fits",
                           verbose=False)
    median_rms = hp.read_map(f"outputs/map_rms_median_{nside}.fits",
                             verbose=False)
    mean_error = hp.read_map(f"outputs/map_error_mean_{nside}.fits",
                             verbose=False)
    median_error = hp.read_map(f"outputs/map_error_median_{nside}.fits",
                               verbose=False)


plot_lotss_map(map_n, title="Counts")
plot_lotss_map(msk_pt*1.+msk_p*1.+msk_d*1., title="Low-res masks")
plot_lotss_map(mean_error, title='Error mean',
               max=0.35, unit='mJy/beam')
plot_lotss_map(median_error, title='Error median',
               max=0.35, unit='mJy/beam')
plot_lotss_map(mean_rms, title='RMS mean',
               max=0.35, unit='mJy/beam')
plot_lotss_map(median_rms, title='RMS median',
               max=0.35, unit='mJy/beam')

plt.show()
