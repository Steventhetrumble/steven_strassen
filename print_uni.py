import tables
import numpy as np



f = tables.open_file('p1andp2.h5', mode='r')
c = np.array((f.root.data))
print c
f.close
