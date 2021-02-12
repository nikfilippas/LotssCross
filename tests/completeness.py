"""
Check completeness functions and optimisations.
"""
import numpy as np

comp_px = comp[np.where(p_map != 0)[0]]
# check if they end strictly at 1
assert (comp_px[:, -1] == 1).all()
# check if they start loosely at 0
assert np.isclose(comp_px[:, 0], 0, atol=1e-6).all()
# check if they are increasing
diffs = np.subtract(comp_px[:, 1:], comp_px[:, :-1])
assert (diffs >= 0).all()





import matplotlib.pyplot as plt
[plt.plot(C, "grey", alpha=0.1) for C in comp_px[::10]]
plt.savefig("completeness.png")
