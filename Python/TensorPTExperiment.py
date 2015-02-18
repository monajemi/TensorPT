# TensorPTExperiment.py
# A script to test the phase transiion hypothesis
# for Tensor Compressed Sensing
#
# This python script uses distributed-memory interior point
# solver Elemental to solve noiseless CS problem.
#
# Copyright 2012, Hatef Monajemi (monajemi@stanford.edu)
# http://www.stanford.edu/~monajemi
#
# ADD PATH TO DEP FOR LOCAL USE (DOES NOT NEEDED IF CLUSTERJOB USED)
import sys
sys.path.append('DEP')

import El
import numpy as np;
import csv;


projectCode       = 'TFUSE'
fieldCode       = 'Pos'
solverCode      = 'El'
SUID            = 'monajemi'
operatorCode    = 0
qRegular        = 1
nMonte          = 10
ncells          = [384,384]
eList           = np.linspace(0.005,0.1,10);
delta           = 0.5


#########    NO CHANGE BELOW THIS LINE ########
worldRank = El.mpi.WorldRank()

# ADD A SEED HERE FOR REPRODUCIBILITY

N               = np.prod(ncells)
n               = int(delta * N)
kList           = [np.floor(x * N) for x in eList]

if(N < 1):
    sys.exit()


# build distributed CS matrix
A = buildCSMatrix(n, N,projectCode, fieldCode, operatorCode, ncells);


err_thresh = 0.001;

# solve for each k, nMonte times! May be use MPI to distributed for K's (?JACK)
for ic in range(len(kList)):
    k   = kList[ic]
    monteCount = 0
    for m in range(nMonte):
        # build a Reg or irReg kSparseVector
        if(qRegular == 1):
            x0 = RegkSparseVector(k,N,fieldCode)
        else:
            x0 = kSparseVector(k,N,fieldCode)
        # generate instance data
        y  = MatMult(A,x0);   #El.

        # solve
        itr = 0;
        val = float('nan');
        while( np.isnan(val) && itr < nMonte+50):
            [x1,val] = SolveInstance(A,y,fieldCode, solverCode) # this must call El.BP
            itr = itr + 1
        if( not np.isnan(val) ):
            obj0 = np.divide(np.linalg.norm(x0, 'fro'), np.sqrt(len(x0)) , dtype=float)
            err0 = np.divide(np.linalg.norm(x1-x0, 'fro'), np.sqrt(len(x0)) , dtype=float)
            err1 = (np.divide(err0,obj0, dtype=float) < err_thresh) * 1 ;
            err2 = np.mean( np.abs( x1 - x0) < err_thresh );
            res[monteCount]  = [err0, err1, err2]
            monteCount = monteCount+1


    results(ic,:) = [n, N , k , nex , Nex , kex , nMonte , mean(res) ];
    np.save(SUID+'_results.npy', results)


    with open(SUID+'_results.csv', 'wb') as csvfile:
        resultswriter = csv.writer(csvfile, delimiter=',')
        resultswriter.writerow([projectCode, fieldCode, solverCode, qRegular,SUID, n, N , kex, nMonte, success.rate, success, failure, delta, rho, eps])



El.Finalize()
