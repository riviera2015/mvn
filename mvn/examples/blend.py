#! /usr/bin/env python
"""
demonstration of bayseian inference between two mvn's
aka "covariance intersection" 

.. plot:: ./examples/blend.py main
"""

import pylab



from mvn import Mvn

def main():
    """
    demonstrate the `covariance intersection algorithm
    <http://en.wikipedia.org/wiki/Kalman_filter#Update>`_ 
    """
    pylab.figure(1, figsize=(5,5))
    
    red  = Mvn.rand(shape=2)    
    blue = Mvn.rand(shape=2)
    
    magenta = red & blue
    
    red.plot(    facecolor = 'r')
    blue.plot(   facecolor = 'b')
    magenta.plot(facecolor = 'm')   
    
    pylab.xlabel('Magenta = Red & Blue')    
    pylab.show()

if __name__ == '__main__':
    main()
