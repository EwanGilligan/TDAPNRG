from scipy.spatial import distance
cimport cython


def one_skeleton(x, r):
    #n = x.shape[0]
    dm = distance.squareform(distance.pdist(x))
    return one_skeleton_cython(dm, r)

@cython.boundscheck(False)
@cython.wraparound(False)
cdef one_skeleton_cython(double[:,:] dm, float r):
    cdef list simplices = []
    cdef n = dm.shape[0]
    cdef int i, j
    # iterate over upper triangular portion of the matrix.
    for i in range(n-2):
        for j in range(i + 1, n):
            if dm[i, j] <= r:
                # add simplex with time added.
                simplices.append(([i, j], dm[i, j]))
    return simplices





