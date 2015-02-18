# buildTFUSE.py
# This python function uses distributed-memory library
# Elemental.
#
# Copyright 2012, Hatef Monajemi (monajemi@stanford.edu)
# http://www.stanford.edu/~monajemi
import El
import numpy as np

def buildTFUSE(k,N,fieldCode, ncells)

    delta = np.divide(n,N, dtype=float)
    N_sub = ncells[0]
    n_sub = np.floor(delta * N_sub)

    A_sub = El.DistSparseMatrix()
    A_sub.Resize(n_sub,N_sub)

    if fieldCode in ('R', 'Pos'):
        El.Gaussian(A_sub , n_sub, N_sub) #should be El.USE(A, n_sub, N_sub) later on (OK for now)
    elif fieldCode == 'C':
        #Jack:: How would you define a complex Gaussian?
        El.Gaussian.Complex(A_sub , n_sub, N_sub)
    else:
        sys.exit('fieldCode Not Recognized')


    A = El.DistSparseMatrix()
    A.Resize(n,N)
    # Perform Kronecker product to get block diagonal A
    # MATLAB: A = kron(speye(ncells(2),ncells(2)),A_sub)
    # Jack:: Does El support kronecker product?

    I   = El.DistSparseMatrix();
    El.Identity(I, ncells[1], ncells[1]);
    A   = El.Kron(I , A_sub);

    return A;

