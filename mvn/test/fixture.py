#! /usr/bin/env python
"""
************
Test Objects
************
"""

import pickle
import numpy
import os

from mvn import Mvn
from mvn.matrix import Matrix
from helpers import randint

(fileDir, _) = os.path.split(os.path.abspath(__file__))

pickleName =os.path.join(fileDir,'testObjects.pkl')

lookup ={}
try:
    lookup =pickle.load(open(pickleName,"r"))
    locals().update(lookup['last'])
except EOFError:
    pass
except IOError: 
    pass
except ValueError:
    pass
except KeyError:
    pass



def getObjects(values):
    drop = ['new','x','seed']
    frozenValues=frozenset(
        (key,value) 
        for (key,value) in values.__dict__.iteritems() 
        if key not in drop
    )

    objects=None
    if not values.new:
        try:
            objects=lookup[frozenValues]
        except KeyError:
            pass

    if objects is None:
        objects = makeObjects(values.flat,values.ndim,values.seed)
        
    lookup[frozenValues] = objects

    lookup['last']=objects
    globals().update(objects)

    pickle.dump(lookup,open(pickleName,'w'))

    return objects

def makeObjects(flat=None,ndim=None,seed=None):
    randn=numpy.random.randn
    
    if seed is None:
        seed=randint(1,1e6)
    assert isinstance(seed,int)
    numpy.random.seed(seed)


    if ndim is None:
        ndim=randint(0,20)
    assert isinstance(ndim,int),'ndim must be an int'

    shapes={
        None:lambda :randint(-ndim,ndim),
        True:lambda :randint(1,ndim),
        False:lambda :randint(-ndim,0),
    }

    triple=lambda x:[x,x,x]
    
    if hasattr(flat,'__iter__'):
        flat=[f if isinstance(f,int) else shapes[f]() for f in flat]   
    elif flat in shapes:
        flat=[item() for item in triple(shapes[flat])]
    elif isinstance(flat,int):
        flat=triple(flat)
    
    assert all(f<=ndim for f in flat), "flatness can't be larger than ndim"
        

    rvec= lambda n=1,ndim=ndim:Matrix(randn(n,ndim))

    A,B,C=[
        Mvn.rand([ndim-F,ndim])
        for F in flat
    ]


    n=randint(1,2*ndim)
    M=rvec(n).H
    M2=rvec(n).H    

    E=Matrix.eye(ndim)
    
    K1 = (numpy.random.randn())
    K2 = (numpy.random.randn())

    N=randint(-5,5)

    fixture={
        'ndim':ndim,
        'A':A,'B':B,'C':C,
        'M':M,'M2':M2,'E':E,
        'K1':K1,'K2':K2,
        'N':N,
        'seed':seed,
    }
    
    return fixture


