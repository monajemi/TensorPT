# KSparseVector.py
#
# This python script uses distributed-memory library
# Elemental.
#
# Copyright 2012, Hatef Monajemi (monajemi@stanford.edu)
# http://www.stanford.edu/~monajemi

def KSparseVector(k,N,field='R'):

# Have the root process (rank=0) broadcast its seed
# Have each process set its seed to the broadcasted value
    j0 = np.random.random_integers(0,N-1,k);

    if(field=='R'):
        coef = El.Matrix()
        El.Gaussian(coef, k, 1 )
        El.EntrywiseMap(coef, lambda x : np.sgn(x) );   # k: -1 or 1 randomly
    
    # Jack:: How can I update entries of x0 to have coef as values?
    x0 = El.DistMultiVec()
    x0.Resize( N, 1 )
    for i in xrange(k):
        x0.Set( j0[i], coef.Get(i,0) )
    else:
        sys.exit('Not Impelemented yet')
    
    return x0

