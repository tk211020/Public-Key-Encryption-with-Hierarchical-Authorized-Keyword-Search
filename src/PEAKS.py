from charm.toolbox.pairinggroup import PairingGroup,G1,pair,ZR,hashPair
import random
import time
import csv

def main():
    group = PairingGroup('SS512')
    g = group.random(G1)
    g.initPP()
    z = group.random(ZR)
    #N = group.order()
    authsum=[]
    encsum=[]
    tdsum=[]
    testsum=[]
    s= time.time()
    t=exp(g,z,3)
    e= time.time()
    print((e-s))
    for i in range(101):
        authsum.append(0)
        encsum.append(0)
        tdsum.append(0)
        testsum.append(0)
    for round in range(10):
        for ell in range(1,101):  
            startAuthorize = time.time()
            a=exp(g,z,3)
            b=hash(group,z,1)
            endAuthorize = time.time() 

            startEncrypt = time.time()
            a=exp(g,z,(ell+2))
            c=mod(z,(ell-1))
            endEncrypt = time.time() 

            startTrapdoor = time.time()
            a=exp(g,z,(2*ell+1))
            c=mod(z,(2*ell-2))
            endTrapdoor = time.time() 

            startTest = time.time()
            d=cpair(g,5)
            b=hash(group,z,1)
            endTest = time.time() 

            authsum[ell]=authsum[ell]+ endAuthorize - startAuthorize
            encsum[ell]=encsum[ell]+ endEncrypt - startEncrypt
            tdsum[ell]=tdsum[ell]+ endTrapdoor - startTrapdoor
            testsum[ell]= testsum[ell] +endTest - startTest
    f = open("data_PEAKS.csv", mode='a', newline='')
    writer = csv.writer(f)
    for i in range(1,101):
        writer.writerow([i,(authsum[i]/10),(encsum[i]/10),(tdsum[i]/10),(testsum[i]/10)])
    f.close
def exp(g,z,n):
    for i in range(n):
        output = g**(z)
    return 1
def mod(z,n):
    for i in range(n):
        output = z*(z)
    return 1
def cpair(g,n):
    for i in range(n):
        output = pair(g,g)
    return 1
def hash(group,z,n):
    for i in range(n):
        output = group.hash(z,G1)
    return 1
if __name__ == "__main__":
    main()