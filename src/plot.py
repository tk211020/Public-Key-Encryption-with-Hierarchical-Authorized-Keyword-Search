from asyncore import read
import csv
import matplotlib.pyplot as plt

def main():
    f = open('data_new1.csv')
    reader = csv.reader(f)
    next(reader, None)
    datalist_ours = list(reader)
    f.close()

    f = open('data_PEAKS.csv')
    reader = csv.reader(f)
    next(reader, None)
    datalist = list(reader)
    f.close()

    keygen_ours = []
    auth_ours = []
    dele_ours = []
    enc_ours = [] 
    trapdoor_ours = []
    test_ours = []
    ell = []

    auth = []
    enc = [] 
    trapdoor = []
    test = []
    for i in range(25):
        ell.append(i+1)
        keygen_ours.append(float((datalist_ours[i][1])))
        auth_ours.append(float((datalist_ours[i][2])))
        dele_ours.append(float((datalist_ours[i][3])))
        enc_ours.append(float((datalist_ours[i][4])))
        trapdoor_ours.append(float((datalist_ours[i][5])))
        test_ours.append(float((datalist_ours[i][6])))
        
        auth.append(float((datalist[i][1])))
        enc.append(float((datalist[i][2])))
        trapdoor.append(float((datalist[i][3])))
        test.append(float((datalist[i][4])))
    
    
    
    lines1 = plt.plot(ell,test_ours,label='ours', color='black')
    lines2 = plt.plot(ell,test,label='JMG+16' ,color='black')
    plt.ylabel('time cost of Test algorithm (s)')
    #fixed
    plt.grid(color=(205/255, 205/255, 205/255))
    plt.setp(lines1,marker = "o") 
    plt.setp(lines2,marker = "s") 
    plt.xlabel('size of the set of keywords')
    plt.legend()
    plt.savefig('test1.png')

if __name__ == "__main__":
    main()