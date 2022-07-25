# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 23:23:48 2021

@author: j23793276
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May 17 15:02:55 2021

@author: j23793276
"""

from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,GT,pair
from charm.toolbox.ABEnc import ABEnc
from charm.toolbox.ABEncMultiAuth import ABEncMultiAuth
import random
import time

X = []
Y = []

class DIPE(ABEncMultiAuth):
    def __init__(self, groupObj, authNum, vecLen, verbose=False):
        ABEnc.__init__(self)
        global group, auth_num, vec_len
        group = groupObj
        auth_num = authNum
        vec_len = vecLen
    
    def setup(self):
        g = group.random(G1)
        g.initPP()
            
            
        pp = {'g':g,'H':group.hash}
        #print(pp)
        return pp
        
    def authsetup(self, pp):
        
        alphaibar = group.random(ZR)
        e_gg_alphaibar = pair(pp['g'],pp['g']) ** alphaibar
        g_alphaibar = pp['g'] ** alphaibar
        
        alpha0i = group.random(ZR)
        g_alpha0i = pp['g'] ** alpha0i
        
        J = []#alpha1i,...,alphali
        g_alphaki = []#g^alphaki,...,g^alphali
        for i in range(vec_len):
            alphaki = group.random(ZR)
            J.append(alphaki)
            g_alphaki.append(pp['g'] ** alphaki)
        
        
        
        pk = {'g^alpha0i':g_alpha0i, 'g^alphaki':g_alphaki,'e_gg^alphaibar':e_gg_alphaibar}
        mk = {'g^alphaibar':g_alphaibar, 'alpha0i':alpha0i}
        for j in range(vec_len):
            string = str(j+1)
            mk['alpha'+string+'i'] = J[j]
        #print(mki)
        return pk, mk
       
    def keygen(self, pp, pk, mk, GID, X, authIndex):
        
        if X[0]==0: 
            print("X[0] can not be 0")
            return
            
        hashInput = [GID, X]
        D_0 = pp['H'](hashInput, G1)
        #print("D_0:",D_0)
        D_1i = mk['g^alphaibar'] * (D_0 ** mk['alpha0i'])
        K_ji = []
        for i in range(vec_len):
            tmp0 = (X[i]/X[0]) * (-1) * mk['alpha1i']
            string = str(i+1)
            tmp1 = D_0 **  mk['alpha'+string+'i']
            K_ji.append((D_0 ** tmp0) * tmp1)
        sk = {'D_0':D_0, 'D_1i':D_1i,'K_ji':K_ji}
        
        return sk
       
    def encrypt(self, pp, pki, M, Y):
        s =  group.random(ZR)
        prod1 = 1
        for i in range(auth_num):
            prod1 = prod1 * (pki[i]['e_gg^alphaibar'])
        E_0 = M * (prod1 ** s)
        
        prod2 = 1
        for i in range(vec_len):
            prod4 = 1
            for j in range(auth_num):
                prod4 = prod4 * pki[j]['g^alphaki'][i]
            prod2 = prod2 * (prod4 ** Y[i])
        
        prod3 = 1
        for i in range(auth_num):
            prod3 = prod3 * pki[i]['g^alpha0i']
            
        
        E_1 = (prod3 * prod2) ** s
        E_2 = pp['g'] ** s
        
        ct = {'E_0':E_0, 'E_1':E_1, 'E_2':E_2}
        return ct
    
    def decrypt(self, pki, ski, ct, Y):
        prodOfD1i = 1
        for i in range(auth_num):
            prodOfD1i = prodOfD1i * (ski[i]['D_1i'])
        
        Kj_yj = []
        for j in range(vec_len):#K_1,...,K_l
            prodOfKji_yj = 1
            for i in range(auth_num):#authority
                prodOfKji_yj = prodOfKji_yj * (ski[i]['K_ji'][j])
                if i == (auth_num - 1): 
                    prodOfKji_yj = prodOfKji_yj ** Y[j]
                    Kj_yj.append(prodOfKji_yj)
                    
        prodOfNumerator = 1
        for i in Kj_yj:
          prodOfNumerator = prodOfNumerator * i
         
        prodOfNumerator = prodOfNumerator * prodOfD1i
         
        numerator = pair(prodOfNumerator, ct['E_2'])
        denominator = pair(ct['E_1'], ski[0]['D_0'])
        
        maskTerm = numerator/denominator
        
        return ct['E_0']/maskTerm
  
def dot(V1,V2):
    if len(V1) != len(V2):
        return -1
    return sum(i[0] * i[1] for i in zip(V1,V2))
      
def main():
    groupObj = PairingGroup('SS512')
    authNum = 1
    vecLen = 10
    dipe = DIPE(groupObj, authNum, vecLen)
        
    startSetup = time.time()
    pp = dipe.setup()
    endSetup = time.time()
    #print("\npki :=>", pki) 
    #print("\nmki :=>", mki)
    pki = []
    mki = []
    authsetupTime = 0
    for i in range(authNum):    
        startAuthsetup = time.time()
        (pk,mk) = dipe.authsetup(pp)
        endAuthsetup = time.time()
        pki.append(pk)
        mki.append(mk)
        authsetupTime = authsetupTime + (endAuthsetup - startAuthsetup)
        
    gidLen = 10
    GID = ""
    for i in range(gidLen):
        GID = GID + str(random.randint(0,1))
    
    
    for i in range(vecLen):
        X.append(group.random(ZR))
        
    keygenTime = 0
    ski = []
    for i in range(authNum):
        pk = pki[i]
        mk = mki[i]
        startKeygen = time.time()
        sk = dipe.keygen(pp, pk, mk, GID, X, i)
        endKeygen = time.time()
        ski.append(sk)
        keygenTime = keygenTime + (endKeygen - startKeygen)
        #print("\nsk[",i,"]:=>", sk)
       
    sum = 0
    for i in range(vecLen-1):
        tmp = group.random(ZR)
        sum = sum + X[i] * tmp
        Y.append(tmp)
    Y.append(-sum/X[vecLen-1])
    #print(dot(X,Y))    
        
    M = groupObj.random(GT)
    print("\nM =>", M)
        
    startEnc = time.time()
    ct = dipe.encrypt(pp, pki, M ,Y)
    endEnc = time.time()
    #print("\nct :=>", ct)
       
    startDec = time.time()
    rec_M = dipe.decrypt(pki,ski,ct,Y)
    endDec = time.time()
    print("\nRec_M =>", rec_M)
        
       
    print("\nSetupTime:",endSetup - startSetup)
    print("AuthsetupTime:",authsetupTime)
    print("KeygenTime:",keygenTime)
    print("EncTime:",endEnc - startEnc)
    print("DecTime:",endDec - startDec) 
    
if __name__ == "__main__":
    main()
