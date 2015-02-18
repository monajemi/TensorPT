# buildCSMatrix.py
# This python script uses distributed-memory library
# Elemental.
#
# Copyright 2012, Hatef Monajemi (monajemi@stanford.edu)
# http://www.stanford.edu/~monajemi

def buildCSMatrix(n, N, projectCode, fieldCode, operatorCode, ncells);
    

    if (projectCode=='TFUSE'):
        A = buildTFUSE(n,N,fieldCode, ncells)

    return A