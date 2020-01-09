import string
import math
import numpy as np


#read qrels.txt return a dic
def read_qrels():
    #read qrels,txt
    with open("systems/qrels.txt", 'r', encoding='utf-8') as fin:
        input_qrels = fin.read()
        fin.close()

    dic_input_qrels = {}
    for l in input_qrels.split('\n')[:-1]:
        a, b = l.split(' ', 1)  # split("", split times)
        qid = int(a.replace(":", "")) #int

        qrel = b.split() #str->list
        list2 = []

        for i in range(len(qrel)):
            list1 = qrel[i].split(",")
            docID = int(list1[0].replace("(", ""))
            rel_value = int(list1[1].replace(")", ""))

            list1 = [docID, rel_value]
            list2.append(list1)

        dic_input_qrels[qid] = list2

    print(dic_input_qrels)
    return dic_input_qrels  # format: {1: [[9090, 3], [6850, 2], [9574, 2], [8709, 1], [9684, 1], [5011, 1]], 2: [[5715, 2]...}


#read SX.results with rank k , return a list
def read_S_results(k):
    with open("systems/S6.results", 'r', encoding='utf-8') as fin:
        sresults = fin.read()

    list2 = []
    for l in sresults.split('\n')[:-1]:
        list1 = l.split()
        for i in range(len(list1)):
            list1[i] = float(list1[i])

        if list1[0] == 1.0:# query ID = 1
            if list1[3]<= float(k):
                list2.append(list1)
        if list1[0] == 2.0:# query ID = 2
            if list1[3]<= float(k):
                list2.append(list1)
        if list1[0] == 3.0:# query ID = 3
            if list1[3]<= float(k):
                list2.append(list1)
        if list1[0] == 4.0:# query ID = 4
            if list1[3]<= float(k):
                list2.append(list1)
        if list1[0] == 5.0:# query ID = 5
            if list1[3]<= float(k):
                list2.append(list1)
        if list1[0] == 6.0:# query ID = 6
            if list1[3]<= float(k):
                list2.append(list1)
        if list1[0] == 7.0:# query ID = 7
            if list1[3]<= float(k):
                list2.append(list1)
        if list1[0] == 8.0:# query ID = 8
            if list1[3]<= float(k):
                list2.append(list1)
        if list1[0] == 9.0:# query ID = 9
            if list1[3]<= float(k):
                list2.append(list1)
        if list1[0] == 10.0:# query ID = 10
            if list1[3]<= float(k):
                list2.append(list1)


    print(list2)
    return list2 #[[1.0, 0.0, 9684.0, 1.0, 5.0743, 0.0], [1.0, 0.0, 9574.0, 2.0, 4.4829, 0.0], ...]

#Find precision with rank k, return a list
def precision(k):
    read_from_results = read_S_results(k)#read SX.results
    print(read_from_results)
    read_from_qrels = read_qrels()#read qrel.txt
    print(read_from_qrels)

    prec_k_list = []
    for qid, docid in read_from_qrels.items():

        for i in range(1, len(read_from_qrels)+1):#find match
            TP = 0
            if qid == i:
                print("qid", qid)
                for li in docid:
                    for li1 in read_from_results:
                        if li1[0] == float(i):
                            if li[0] == int(li1[2]):
                                print(li[0])
                                TP = TP+1
                prec_k = TP / 10
                prec_k = ("%.3f" % prec_k)
                #print(prec_k)
                prec_k_list.append(prec_k)

    print(prec_k_list)
    return prec_k_list

#Find recall with rank k, return a list
def recall(k):
    read_from_results = read_S_results(k)
    print(read_from_results)
    read_from_qrels = read_qrels()
    print(read_from_qrels)


    recall_k_list = []
    for qid, docid in read_from_qrels.items():

        for i in range(1, len(read_from_qrels) + 1):
            TP = 0
            if qid == i:
                for li in docid:
                    for li1 in read_from_results:
                        if li1[0] == float(i):
                            if li[0] == int(li1[2]):
                                TP = TP + 1
                #print(TP)
                recall_k = TP / len(docid)# /relevant doc
                #print(len(docid))
                recall_k = ("%.3f" % recall_k)
                #print(type(recall_k))
                recall_k_list.append(recall_k)

    print(recall_k_list)
    return recall_k_list


#Find r-precision with rank k, return a list
def r_precision():

    read_from_qrels = read_qrels()#read qrel.txt
    print(read_from_qrels)

    rprec_k_list = []

    for qid, docid in read_from_qrels.items():#for each query with different r=k

        for i in range(1, len(read_from_qrels)+1):
            TP = 0
            if qid == i:
                k = len(docid)# r = k
                read_from_results = read_S_results(k)
                for li in docid:

                    for li1 in read_from_results:
                        if li1[0] == float(i):
                            if li[0] == int(li1[2]):
                                TP = TP+1
                rprec_k = TP / k #retrieved doc
                rprec_k = ("%.3f" % rprec_k)
                print(rprec_k)
                rprec_k_list.append(rprec_k)

    print("rrrrr",rprec_k_list)
    return rprec_k_list

#Find read whole result from result file, return a list
def read_whole_s_results():
    with open("systems/S6.results", 'r', encoding='utf-8') as fin:
        sresults = fin.read()

    list2 = []
    for l in sresults.split('\n')[:-1]:
        list1 = l.split()
        for i in range(len(list1)):
            list1[i] = float(list1[i])
        list2.append(list1)
    print(len(list2))
    return list2


#Find AP, return a list
def MAP():

    read_from_qrels = read_qrels()
    print(read_from_qrels)


    read_from_results = read_whole_s_results()#read whole retrieved doc
    ap_list = []
    for qid, docid in read_from_qrels.items():
        sumap = 0
        for i in range(1, len(read_from_qrels) + 1):

            if qid == i:
                list3 = []
                sumsap = 0
                for li in docid:
                    for li1 in read_from_results:

                        if li1[0] == float(i):
                            if li[0] == int(li1[2]):
                                list3.append(li1[3])
                list3.sort() #sort the list
                #print(list3)
                for x, v in enumerate(list3):
                    sap = (x+1)/v #1/rank1, 2/rank2, 3/rank3
                    #print(sap)
                    sumsap = sumsap+sap

                ap = sumsap/len(docid)# / relevant doc
                print("ap", ap)
                ap = ("%.3f" % ap)
                ap_list.append(ap)

    print(ap_list)
    return ap_list


#Find nDCG at rank k, return a list
def nDCG(k):
    read_from_qrels = read_qrels()
    print(read_from_qrels)

    read_from_results = read_S_results(k)#read result with k
#DCG @ k
    DG_list = []

    for qid, docid in read_from_qrels.items():

        for i in range(1, len(read_from_qrels) + 1):

            if qid == i:
                print("qid", qid)
                list3 = []
                DCG=0
                for li in docid:
                    for li1 in read_from_results:

                        if li1[0] == float(i):
                            if li[0] == int(li1[2]):
                                if li1[3] == 1.0:#first rel:  add
                                    DCG = DCG + li[1]
                                    print(li[1])
                                else:
                                    DG = li[1]*(1/math.log(li1[3], 2))
                                    print(DG)
                                    DCG = DCG + DG

                DCG = ("%.3f" % DCG)
                DG_list.append(DCG)
    print(DG_list)


#iDCG @ k
    iDG_list = []
    for qid, docid in read_from_qrels.items():

        for i in range(1, len(read_from_qrels) + 1):
            if qid == i:
                print("qid", qid)
                iDCG = 0
                count = 1
                for q, li in enumerate(docid):
                    if q == k:
                        break
                    if count == 1:
                        iDCG = iDCG + li[1]
                        print("idcg", iDCG)
                        count = count + 1
                    else:
                        iDCG = iDCG + li[1] * (1 / math.log(count, 2))
                        print("idcg", iDCG)
                        count = count + 1

                iDCG = ("%.3f" % iDCG)
                iDG_list.append(iDCG)
    print(iDG_list)

#nDCG@k = DCG@k / iDCG@k
    nDCG_list=[]
    for j in range(len(iDG_list)):
        if float(iDG_list[j]) == 0.0:
            nDCG=0
        else:
            nDCG = float(DG_list[j])/float(iDG_list[j])

        nDCG = ("%.3f" % nDCG)
        nDCG_list.append(nDCG)
    print(nDCG_list)

    return nDCG_list

#write SX.eval
def write_result():
    p_10 = precision(10)
    r_50 = recall(50)
    r_p = r_precision()
    Map = MAP()
    nDCG_10 = nDCG(10)
    nDCG_20 = nDCG(20)




#mean
    with open('S6.eval', 'w') as fout:
        fout.write( '\t' + "P@10" + '\t' + "R@50" + '\t'+"r-Precision" + '\t' + "AP" + '\t' + "nDCG@10"+'\t'+ "nDCG@20"+'\n')
        for i in range(10):
            fout.write(str(i+1) + '\t' + str(p_10[i]) + '\t' + str(r_50[i]) + '\t' + str(r_p[i]) + '\t' + str(Map[i]) + '\t' + str(nDCG_10[i]) + '\t' + str(nDCG_20[i]) + '\n')
        fout.close()

    for a in range(len(p_10)):
        p_10[a] = float(p_10[a])

    p_10_mean = np.mean(p_10)
    p_10_mean = ("%.3f" % p_10_mean)
    print(p_10_mean)

    for b in range(len(r_50)):
        r_50[b] = float(r_50[b])

    r_50_mean = np.mean(r_50)
    r_50_mean = ("%.3f" % r_50_mean)
    print(r_50_mean)

    for c in range(len(r_p)):
        r_p[c] = float(r_p[c])

    r_p_mean = np.mean(r_p)
    r_p_mean = ("%.3f" % r_p_mean)
    print(r_p_mean)

    for d in range(len(Map)):
        Map[d] = float(Map[d])

    Map_mean = np.mean(Map)
    Map_mean = ("%.3f" % Map_mean)
    print(Map_mean)

    for f in range(len(nDCG_10)):
        nDCG_10[f] = float(nDCG_10[f])

    nDCG_10_mean = np.mean(nDCG_10)
    nDCG_10_mean = ("%.3f" % nDCG_10_mean)
    print(nDCG_10_mean)

    for f in range(len(nDCG_20)):
        nDCG_20[f] = float(nDCG_20[f])

    nDCG_20_mean = np.mean(nDCG_20)
    nDCG_20_mean = ("%.3f" % nDCG_20_mean)
    print(nDCG_20_mean)

    with open('S6.eval', 'a') as fout:
        fout.write("mean" + '\t' + str(p_10_mean) + '\t' + str(r_50_mean) + '\t' + str(r_p_mean) + '\t' + str(
            Map_mean) + '\t' + str(nDCG_10_mean) + '\t' + str(nDCG_20_mean) + '\n')

#Write All.eval
def write_all_mean():
    with open("S1.eval", 'r', encoding='utf-8') as fin:
        lin1 = fin.readlines()
        mean1 = lin1[-1].split('\t')
        fin.close()
    with open("S2.eval", 'r', encoding='utf-8') as fin:
        lin1 = fin.readlines()
        mean2 = lin1[-1].split('\t')
        fin.close()
    with open("S3.eval", 'r', encoding='utf-8') as fin:
        lin1 = fin.readlines()
        mean3 = lin1[-1].split('\t')
        fin.close()
    with open("S4.eval", 'r', encoding='utf-8') as fin:
        lin1 = fin.readlines()
        mean4 = lin1[-1].split('\t')
        fin.close()
    with open("S5.eval", 'r', encoding='utf-8') as fin:
        lin1 = fin.readlines()
        mean5 = lin1[-1].split('\t')
        fin.close()
    with open("S6.eval", 'r', encoding='utf-8') as fin:
        lin1 = fin.readlines()
        mean6 = lin1[-1].split('\t')
        fin.close()

    print(mean1)
    print(type(mean1))
    all_mean=[]
    all_mean.append(mean1)
    all_mean.append(mean2)
    all_mean.append(mean3)
    all_mean.append(mean4)
    all_mean.append(mean5)
    all_mean.append(mean6)
    print(all_mean)

    with open('All12.eval', 'w') as fout:
        fout.write(
             '\t' + "P@10" + '\t' + "R@50" + '\t' + "r-Precision" + '\t' + "AP" + '\t' + "nDCG@10" + '\t' + "nDCG@20" + '\n')
        for i in range(6):
            fout.write("S" + str(i + 1))
            for j in range(6):
                fout.write( '\t'+str(all_mean[i][j+1]))
            #fout.write('\n')

        fout.close()


def main():
    #read_qrels()
    #read_S_results(10)
    #precision(10)
    #recall(10)
    #r_precision()
    #read_whole_s_results()
    #MAP()
    #nDCG(10)



    write_result()# write S1-S6.eval
    #write_all_mean() #write All.eval

if __name__ == "__main__":
    main()

