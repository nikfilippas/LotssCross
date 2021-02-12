"""
Check optimization for utils.FluxPDF.compute_p_map.
"""
import numpy as np
from scipy.special import erf
from utils import FluxPDF

# global
F = FluxPDF()
q = 5
Imin = 2
alpha = -0.7
std_map = np.load("sigmas.npz")["sigmas"]
lf = F.log_flux + alpha * np.log10(144. / 1400.)

# old way
Map = np.zeros(len(std_map))
for ip, std in enumerate(std_map):
    if std > 0:
        Ithr = max(q * std, Imin)
        x = (Ithr - 10.**lf) / (np.sqrt(2.) * std)
        comp = 0.5 * (1 - erf(x))
        Map[ip] = np.sum(F.probs * comp)

# optimised way (avoid loop)
Ithr = np.maximum(q*std_map, Imin)
x = np.divide((Ithr[:, None] - 10**lf),
              np.sqrt(2)*std_map[:, None],
              out=np.zeros((len(std_map), len(lf))),
              where=(std_map!=0)[:, None])
comp = 0.5 * (1 - erf(x))
p_map = np.sum(F.probs * comp, axis=1)
p_map[np.isclose(p_map, 0.5)] = 0

assert np.allclose(Map, p_map)

# check whether simps yields similar results
from scipy.integrate import simps
p_map_2 = simps(F.probs*comp)
p_map_2[np.isclose(p_map_2, 0.5)] = 0
assert np.allclose(p_map, p_map_2)
