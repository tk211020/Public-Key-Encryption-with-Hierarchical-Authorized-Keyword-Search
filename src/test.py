from charm.toolbox.pairinggroup import PairingGroup,G1,pair,ZR
import random
import time
import csv

def main():
    keygensum = []
    authsum = []
    delesum = []
    encsum = []
    tdsum = []
    testsum = []
    round = 25
    for i in range(26):
        keygensum.append(0)
        authsum.append(0)
        delesum.append(0)
        encsum.append(0)
        tdsum.append(0)
        testsum.append(0)
    for r in range(round):
        print("round:",r)
        W = '1'#token vector
        for i in range(25):  
            W_p = W #token vector2
            W_c = W #ciphertext vector
            ell = len(W) 
            n = len(W) * 2
            group = PairingGroup('SS512')
            g = group.random(G1)
            e = group.init(G1) #identity type:pair
            g.initPP()
            N = group.order()
            pp = {'N': N, 'G':group, 'g':g, 'n':n, 'ell':ell, 'e':e}

            startKeyGen = time.time()
            sk = keyGen(pp)['sk']
            pk = keyGen(pp)['pk']
            endKeyGen = time.time() 
            #print("pk is", pk)
            #print("sk is", sk)

            startAuthorize = time.time()
            token_w = authorize(pp, sk, W)
            endAuthorize = time.time() 
            #print("token_w is", token_w)

            startDelegate = time.time()
            #token_w_p = delegate(pp, token_w, W_p)
            endDelegate = time.time() 
            #print("token_w_p is",token_w_p)

            startEncrypt = time.time()
            ct_w = encrypt(pp, pk, W_c)
            endEncrypt = time.time() 
            #print("ct_w is", ct_w)

            startTrapdoor = time.time()
            td_w_p = trapdoor(pp, token_w, W_p)
            endTrapdoor = time.time() 
            #print("td_w_p is", td_w_p)

            #print("W is", W)
            #print("W_p is", W_p)
            #print("W_c is", W_c)

            startTest = time.time()
            print("Testing ct_w & td_w_p result:",test(pp, ct_w, td_w_p))
            endTest = time.time() 

            #print("-----------------------------------")
            
            #print("ell:", ell)
            #print("KeyGen Time:", endKeyGen - startKeyGen)
            #print("Authorize Time:", endAuthorize - startAuthorize)
            #print("Delegate Time:", endDelegate - startDelegate)
            #print("Encrypt Time:", endEncrypt - startEncrypt)
            #print("Trapdoor Time:", endTrapdoor - startTrapdoor)
            print("Test Time:", endTest - startTest) 
            keygensum[ell]=keygensum[ell]+ endKeyGen - startKeyGen
            authsum[ell]=authsum[ell]+ endAuthorize - startAuthorize
            delesum[ell]=delesum[ell]+ endDelegate - startDelegate
            encsum[ell]=encsum[ell]+ endEncrypt - startEncrypt
            tdsum[ell]=tdsum[ell]+ endTrapdoor - startTrapdoor
            testsum[ell]= testsum[ell] +endTest - startTest
            #writer.writerow([ell,endKeyGen - startKeyGen,endAuthorize - startAuthorize,endDelegate - startDelegate,endEncrypt - startEncrypt,endTrapdoor - startTrapdoor,endTest - startTest])
            print( "ell:",ell)
            W=W+str(random.randrange(0,2))
    f = open("data_new2.csv", mode='a', newline='')
    writer = csv.writer(f)
    for i in range(1,26):
        writer.writerow([i,(keygensum[i]/round),(authsum[i]/round),(delesum[i]/round),(encsum[i]/round),(tdsum[i]/round),(testsum[i]/round)])
    f.close
        
def keyGen(pp):
    n = pp['n']
    base_BPair = DOBGen(pp, 2*n+3)
    pk = base_BPair['base_B']
    sk = base_BPair['base_B_star']
    keyPair = {'pk': pk, 'sk': sk}
    return keyPair

def authorize(pp, sk, W):
    N = pp['N']
    n = pp['n']
    ell = pp['ell']

    w = encode_1(W)

    token_w_alpha = []
    token_w_beta = []
    token_w_gamma = []

    # alpha part
    r = random.randint(0,N-1)
    r_i = []
    s_i = []
    t_i = []
    for i in range(0,n):
        r_i.append(random.randint(0,N-1))
        s_i.append([])
        t_i.append([])
        token_w_alpha.append(r_i[i]*w[i])
        token_w_gamma.append([])
    for i in range(0,n):
        token_w_alpha.append(0)
    token_w_alpha.append(1)
    token_w_alpha.append(r)
    token_w_alpha.append(0)

    set_X =[]
    set_Y =[]
    for i in range(0,ell):
        token_w_beta.append([])
        if W[i]=='0':
            set_X.append(i)
        elif W[i]=='1':
            set_Y.append(2*i)
            set_Y.append(2*i+1)
    # beta part
    for i in set_X:
        for j in range(0,n):
            s_i[i].append(random.randint(0,N-1))
            token_w_beta[i].append(s_i[i][j]*w[j])
        for j in range(0,n):
            token_w_beta[i].append(0)
        token_w_beta[i].append(0)
        token_w_beta[i].append(random.randint(0,N-1))
        token_w_beta[i].append(0)
    
    #gamma part
    t = random.randint(0,N-1)
    for i in set_Y:
        for j in range(0,n):
            t_i[i].append(random.randint(0,N-1))
            token_w_gamma[i].append(t_i[i][j]*w[j])
            if i==j :
                token_w_gamma[i][i]= t
        for j in range(0,n):
            token_w_gamma[i].append(0)
        token_w_gamma[i].append(0)
        token_w_gamma[i].append(random.randint(0,N-1))
        token_w_gamma[i].append(0)
    alpha_value=[]
    beta_value = []
    gamma_value = []
    token_w ={'W': W, 'alpha':token_w_alpha, 'beta':token_w_beta, 'gamma':token_w_gamma, 'base':sk}
    #token_w ={'W': W, 'alpha':token_w_alpha, 'beta':token_w_beta, 'gamma':token_w_gamma, 'base':sk, 'alpha_value':alpha_value , 'beta_value':beta_value, 'gamma_value':gamma_value}

    alpha_value =  transform(pp,token_w['alpha'], sk)
    for i in set_X:
        beta_value.append(transform(pp,token_w['beta'][i], sk))
    for i in set_Y:
        gamma_value.append(transform(pp,token_w['gamma'][i], sk))
    #token_w['alpha_value'] = alpha_value
    #token_w['beta_value'] = beta_value
    #token_w['gamma_value'] = gamma_value
    return token_w
    
def delegate(pp, token_w, W_p):
    ell = pp['ell']
    n = pp['n']
    N = pp['N']
    W = token_w['W']
    if (check_subset(W_p, W))!=1 :
        print("W_p must be a subset of W!")
        return 0
    w = encode_1(W)
    w_p = encode_1(W_p)
    
    set_X = []
    set_X_p = []
    set_X_bar = []
    set_X_p_bar = []
    set_Y_p =[]

    for i in range(0,ell):
        if W[i]=='0':
            set_X.append(i)
        elif W[i]=='1':
            set_X_bar.append(i)

    for i in range(0,ell):
        if W_p[i]=='0':
            set_X_p.append(i)
        elif W_p[i]=='1':
            set_X_p_bar.append(i)
            set_Y_p.append(2*i)
            set_Y_p.append(2*i+1)
    alpha_sum_token_w_beta = []
    alpha_sum_token_w_gamma = []
    for i in range(2*n+3):
        alpha_sum_token_w_beta.append(0)
        alpha_sum_token_w_gamma.append(0)
    for i in set_X:
        alpha_sum_token_w_beta = [a + b for a, b in zip(alpha_sum_token_w_beta,token_w['beta'][i])]
        alpha_sum_token_w_beta = [j % (random.randint(0,N-1)) for j in alpha_sum_token_w_beta]
    for i in set_X_bar:
        token_w['gamma'][2*i] = [j * w_p[2*i] for j in token_w['gamma'][2*i]]
        token_w['gamma'][2*i+1] = [j * w_p[2*i+1] for j in token_w['gamma'][2*i+1]]
        alpha_sum_token_w_gamma = [a + b + c for a, b, c in zip(alpha_sum_token_w_gamma, token_w['gamma'][2*i], token_w['gamma'][2*i+1])]
        alpha_sum_token_w_gamma = [j % (random.randint(0,N-1)) for j in alpha_sum_token_w_gamma]
    token_w_p_alpha =[a + b + c for a, b, c in zip(token_w['alpha'], alpha_sum_token_w_beta, alpha_sum_token_w_gamma)]

    beta_sum_token_w_beta = []
    beta_sum_token_w_gamma = []
    token_w_p_beta = []

    for i in range(0,ell):
        beta_sum_token_w_beta.append([])
        beta_sum_token_w_gamma.append([])
        token_w_p_beta.append([])
        for j in range(2*n+3):
            beta_sum_token_w_beta[i].append(0)
            beta_sum_token_w_gamma[i].append(0)
    for i in set_X_p:
        for j in set_X:
            beta_sum_token_w_beta[i] = [a + b for a, b in zip(beta_sum_token_w_beta[i],token_w['beta'][j])]
            beta_sum_token_w_beta[i] = [k % (random.randint(0,N-1)) for k in beta_sum_token_w_beta[i]]
        for j in set_X_bar:
            token_w['gamma'][2*j] = [k * w_p[2*j] for k in token_w['gamma'][2*j]]
            token_w['gamma'][2*j+1] = [k * w_p[2*j+1] for k in token_w['gamma'][2*j+1]]
            beta_sum_token_w_gamma[i] = [a + b + c for a, b, c in zip(beta_sum_token_w_gamma[i], token_w['gamma'][2*j], token_w['gamma'][2*j+1])]
            beta_sum_token_w_gamma[i] = [k % (random.randint(0,N-1)) for k in beta_sum_token_w_gamma[i]]
        token_w_p_beta[i] =[a + b for a, b in zip(beta_sum_token_w_beta[i], beta_sum_token_w_gamma[i])]
        
    gamma_sum_token_w_beta = []
    gamma_sum_token_w_gamma = []
    token_w_p_gamma = []

    for i in range(0,2*ell):
        gamma_sum_token_w_beta.append([])
        gamma_sum_token_w_gamma.append([])
        token_w_p_gamma.append([])
        for j in range(2*n+3):
            gamma_sum_token_w_beta[i].append(0)
            gamma_sum_token_w_gamma[i].append(0)
    for i in set_Y_p:
        for j in set_X:
            gamma_sum_token_w_beta[i] = [a + b for a, b in zip(gamma_sum_token_w_beta[i],token_w['beta'][j])]
            gamma_sum_token_w_beta[i] = [k % (random.randint(0,N-1)) for k in gamma_sum_token_w_beta[i]]
        for j in set_X_bar:
            token_w['gamma'][2*j] = [k * w_p[2*j] for k in token_w['gamma'][2*j]]
            token_w['gamma'][2*j+1] = [k * w_p[2*j+1] for k in token_w['gamma'][2*j+1]]
            gamma_sum_token_w_gamma[i] = [a + b + c for a, b, c in zip(gamma_sum_token_w_gamma[i], token_w['gamma'][2*j], token_w['gamma'][2*j+1])]
            gamma_sum_token_w_gamma[i] = [k % (random.randint(0,N-1)) for k in gamma_sum_token_w_gamma[i]]
        token_w_p_gamma[i] =[a + b + c for a, b, c in zip(token_w['gamma'][i], gamma_sum_token_w_beta[i], gamma_sum_token_w_gamma[i])]
    base = token_w['base']
    token_w_p = {'W': W_p, 'alpha': token_w_p_alpha, 'beta': token_w_p_beta, 'gamma': token_w_p_gamma, 'base': base}

    alpha_value =  transform(pp,token_w_p['alpha'], base)
    beta_value = []
    gamma_value = []
    for i in set_X_p:
        beta_value.append(transform(pp,token_w_p['beta'][i], base))
    for i in set_Y_p:
        gamma_value.append(transform(pp,token_w_p['gamma'][i], base))
    return token_w_p

def encrypt(pp, pk, W):
    N = pp['N']
    n = pp['n']
    base = pk
    w = encode_2(pp, W)
    ct_w1 = []
    sigma = random.randint(0,N-1)
    q = random.randint(0,N-1)
    q_i = []

    for i in range(0,n):
        q_i.append(random.randint(0,N-1))
        ct_w1.append(q_i[i]*w[i])
    for i in range(0,n):
        ct_w1.append(0)
    ct_w1.append(sigma)
    ct_w1.append(0)
    ct_w1.append(q)
    ct_w2 = pair(pp['g'], pp['g']) ** sigma

    ct_w1_value = transform(pp, ct_w1, base)
    ct_w = {'ct_w1':ct_w1, 'ct_w2':ct_w2, 'ct_w1_value': ct_w1_value}

    return ct_w

def trapdoor(pp, token_w, W_p):

    N = pp['N']
    ell = pp['ell']
    n = pp['n']
    W = token_w['W']


    if (check_subset(W_p, W))!=1 :
        print("W_p must be a subset of W!")
        return 0

    w_p = encode_3(W_p)
    set_X = []
    set_X_bar = []

    for i in range(0,ell):
        if W[i]=='0':
            set_X.append(i)
        elif W[i]=='1':
            set_X_bar.append(i)
    sum_token_w_beta = []
    sum_token_w_gamma = []
    for i in range(2*n+3):
        sum_token_w_beta.append(0)
        sum_token_w_gamma.append(0)
    for i in set_X:
        sum_token_w_beta = [a + b for a, b in zip(sum_token_w_beta,token_w['beta'][i])]
        sum_token_w_beta = [j % (random.randint(0,N-1)) for j in sum_token_w_beta]
   
    for i in set_X_bar:
        token_w['gamma'][2*i] = [j * w_p[2*i] for j in token_w['gamma'][2*i]]
        token_w['gamma'][2*i+1] = [j * w_p[2*i+1] for j in token_w['gamma'][2*i+1]]
        sum_token_w_gamma = [a + b + c for a, b, c in zip(sum_token_w_gamma, token_w['gamma'][2*i], token_w['gamma'][2*i+1])]
        sum_token_w_gamma = [j % (random.randint(0,N-1)) for j in sum_token_w_gamma]
    vector =[a + b + c for a, b, c in zip(token_w['alpha'], sum_token_w_beta, sum_token_w_gamma)]
    base = token_w['base']
    value =  transform(pp, vector, base)
    td_w_p = {'W_p':W_p, 'td':vector, 'value':value}
    return td_w_p

def test(pp, ct_w ,td_w_p):
    ct_w1 = ct_w['ct_w1']
    ct_w2 = ct_w['ct_w2']
    ct_w1_value = ct_w['ct_w1_value']
    td_w_p_value = td_w_p['value']
    td_w_p_vector = td_w_p['td']
    a = dpvs_pair(ct_w1_value, td_w_p_value)
    if vector_pair(pp, ct_w1, td_w_p_vector) == ct_w2 :
        return 1
    else :
        return 0
def dpvs_pair(v1_value, v2_value):
    
    product = pair(v1_value[0],v2_value[0])
    for i in range(1,len(v1_value)):
        product = product * pair(v1_value[i],v2_value[i])
    return product

def DOBGen(pp, n):
    g = pp['g']
    group = pp['G']
    r = []
    r_star = []
    for i in range(0,n):
        r.append([])
        r_star.append([])
        for j in range(0,n):
            r[i].append(0)
            r_star[i].append(0)
    

    for i in range(0,n):
        for j in range(0,n):
            r_i = group.random(ZR)
            r[i][j]=(int(r_i))
            r_star[j][i]=(int(1/r_i))
    base_B = []
    base_B_star = []
    for i in range(0,n):
        base_B.append([])
        base_B_star.append([])
        for j in range(0,n):
           base_B[i].append(g**r[i][j])
           base_B_star[i].append(g**(int(r_star[i][j])))
    base_B_pair = {'base_B':base_B, 'base_B_star':base_B_star}
    return base_B_pair

def transform(pp, vector_represent, base):
    e = pp['e']
    vector = []
    for i in range(len(vector_represent)):
        vector.append(e)
        for j in range(len(base[i])):
            base[i][j] = base[i][j]**vector_represent[i]
        vector = [a+b for a, b in zip(vector, base[i])]
    return vector

def getBase_A(pp):
    n = pp['n']
    g = pp['g']
    e = pp['e']
    base_length = 2*n+3
    base_A = []
    for i in range(0,base_length):
        base_A.append([])
        for j in range(0,base_length):
            if i==j:
                base_A[i].append(g)
            else:
                base_A[i].append(e)
    return base_A

def encode_1(W):
    result_w=[]
    for i in range(0,len(W)):
        if W[i]=='1':
            result_w.append(0)
            result_w.append(0)
        else :
            result_w.append(1)
            result_w.append(0)
    return result_w

def encode_2(pp, W):
    N = pp['N']
    result_w=[]
    for i in range(0,len(W)):
        if W[i]=='1':
            result_w.append(0)
            result_w.append(0)
        else :
            result_w.append(0)
            result_w.append(random.randint(0,N-1))
    return result_w

def encode_3(W):
    result_w=[]
    for i in range(0,len(W)):
        if W[i]=='1':
            result_w.append(1)
            result_w.append(1)
        else :
            result_w.append(1)
            result_w.append(0)
    return result_w

def vector_pair(pp, vector_x, vector_y):
    dot = 0
    for i in range(0,len(vector_x)):
        dot = dot + vector_x[i]*vector_y[i]
    return pair(pp['g'],pp['g']) ** dot

def check_subset(W_p, W):
    if (len(W_p)!=len(W)):
            return 0
    for i in range(len(W)):
        if W[i]=='0' and W_p[i]=='1':
            return 0
    return 1

if __name__ == "__main__":
    main()