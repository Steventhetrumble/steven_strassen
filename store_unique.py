import tables
import numpy as np
import os.path


def check_and_write(array, filename, NUM_ENTRIES):
    if not os.path.isfile(filename):
        f = tables.open_file(filename, mode='w')
        atom = tables.Float64Atom()
        array_c = f.create_earray(f.root, 'data', atom, (0,2))
        array_c.append(x)
        f.close()
        return
    f = tables.open_file(filename, mode='r')
    i = 0
    check = False
    for item in f.root.data[0]:
        c = np.array((f.root.data[i:i+NUM_ENTRIES,0:]))
        print c
        idx = np.where(abs((c[:,np.newaxis,:] - y)).sum(axis=2)==0)
        i = i + NUM_ENTRIES 
        if len(idx[0]) == NUM_ENTRIES:
            check =True
            break
    f.close()


    if check:
        print "Duplicate Solution"
    else:
        print "Unique Solution"
        f = tables.open_file(filename, mode='a')
        f.root.data.append(y)
        f.close()
if __name__ == "__main__":

    filename = 'outarray.h5'
    NUM_ENTRIES = 7
    x = np.array([[10, 9], [13, 13], [0, 5], [7, 7], [3, 15], [4, 1], [14, 2]])
    y = np.array([[13, 12], [14, 1], [7, 6], [8, 8], [2, 5], [1, 15], [4, 2]])