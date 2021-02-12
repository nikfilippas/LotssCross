"""
Save time brute-forcing by using numpy.bincount.

# integer binning: should get the average of the y-vals of [1, 1.2]
>>> x = [1, 1.2, 5, 6]
>>> y = [0, 0.5, 7, 8]
>>> np.bincount(x, weights=y, minlength=4)/np.bincount(x, minlength=4)
numpy.array([ nan, 0.25,  nan,  nan,  nan, 7.  , 8.])
"""
import numpy as np

f = np.load("sigma_test.npz")
assert np.allclose(f["brute_force"], f["bincount"], atol=0)

"""
# code to reproduce loaded arrays
import healpy as hp
from astropy.io import fits
nside = 256
npix = hp.nside2npix(nside)
data = fits.open("<fname_here>")[1].data
ipix = hp.ang2pix(nside, data["RA"], data["DEC"], lonlat=True)
# numpy.bincount method
sigmap = np.bincount(ipix, weights=data["Isl_rms"], minlength=npix)
sigmap /= np.bincount(ipix, minlength=npix)
sigmap = np.nan_to_num(sigmap)
# brute force method
st = np.zeros(ipix.size)
for i in range(ipix.min(), ipix.max()+1):
    if i % 1000 == 0:
        print(i)
    if not i in ipix:
        continue
    idx = np.where(ipix == i)[0]
    st[i] = (np.average(data["Isl_rms"][idx]))
"""
