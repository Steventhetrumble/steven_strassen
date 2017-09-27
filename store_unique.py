import tables
import numpy as np

filename = 'outarray.h5'
ROW_SIZE = 2
NUM_COLUMNS = 7
x = np.array([[10, 9], [13, 13], [0, 5], [7, 7], [3, 15], [4, 1], [14, 2]])
y = np.array([[13, 12], [14, 1], [7, 6], [8, 8], [2, 5], [1, 15], [4, 2]])

f = tables.open_file(filename, mode='w')
atom = tables.Float64Atom()

array_c = f.create_earray(f.root, 'data', atom, (0, ROW_SIZE))

array_c.append(x)
f.close()

'''
f = tables.open_file(filename, mode='a')
f.root.data.append(x)'''


f = tables.open_file(filename, mode='r')
c = np.array((f.root.data[0:,0:])) # e.g. read from disk only this part of the dataset
idx = np.where(abs((c[:,np.newaxis,:] - y)).sum(axis=2)==0)
print idx

f.close()