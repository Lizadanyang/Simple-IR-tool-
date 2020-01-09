import re
import string
import random
from stemming.porter2 import stem
#from nltk.corpus import stopwords

def preprocess(text):
    results = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.S)
    result = results.sub("", text)
    #print(result)

    for c in string.punctuation:
        if c != "#":
            result = result.replace(c, ' ')# Tokenisation

    result2 = result.replace("…", ' ')
    result3 = result2.replace("’", ' ')

    word = result3.split(" ")
    for li2 in word:
        if '#' in li2:
            word.append(li2.replace('#', ''))
    list3 = []
    stopwords = []
    with open("englishST.txt", 'r', encoding='utf-8') as fin:
        for l in fin.readlines():
            stopwords.append(l.strip('\n'))

    fin.close()
    for lin in word:
        l1 = lin.lower()
        if l1 not in stopwords:
            list3.append(l1)

    aresult = list(filter(None, list3))
    stemwords = []
    for li in aresult:

        stemword = stem(li)
        # print(stemword)
        stemwords.append(stemword)
    #print(stemwords)
    return stemwords


def give_term_id():
    term_list = []
    with open("tweetsclassification/Tweets.14cat.train", 'r', encoding='Windows-1252') as fin:
        for l in fin.readlines():
            #print(l)
            lin = l.split("\t")
            #print(lin)
            newtweet = preprocess(lin[1])
            term_list = term_list+newtweet
            #print(newtweet)
        fin.close()
    print(term_list)

    new_term_list = []
    for i in term_list:
        if i not in new_term_list:
            new_term_list.append(i)
    print(new_term_list)

    with open('feats1.dic', 'w') as fout:
        for j in range(len(new_term_list)):

            fout.write(str(j+1) + '\t' + new_term_list[j] + '\n')

def match_class_term():
    #get classid in a dic
    class_id_dic = {}
    with open("classIDs.txt", 'r', encoding='utf-8') as f1:
        for l in f1.readlines():
            lin = l.split("\t")
            n = lin[1].replace('\n', '')
            class_id_dic[int(n)] = lin[0]

        f1.close()
    print(class_id_dic)

    term_id_dic = {}
    with open("feats1.dic", 'r', encoding='utf-8') as f2:
        for l in f2.readlines():
            lin = l.split("\t")
            term1 = lin[1].replace('\n', '')
            term_id_dic[int(lin[0])] = term1

        f2.close()
    print(term_id_dic)

    total_dic = {}
    with open("tweetsclassification/Tweets.14cat.test", 'r', encoding='Windows-1252') as fin:
        for l in fin.readlines():
            lin = l.split("\t")
            newtweet = preprocess(lin[1])
            #print(newtweet)
            classid_termid = []
            etweet_list = []# 一行tweet
            for te in newtweet:
                for key, val in term_id_dic.items():

                    if te == val:
                        #print(key, val)
                        etweet_list.append(key)
            #print("each tw", etweet_list)
            etweet_list.sort()

            new_etweet_list = []
            for i in etweet_list:
                if i not in new_etweet_list:
                    new_etweet_list.append(i)

            each_t_class = 0
            class_name = lin[2].replace("\n", '')
            for keyc, valc in class_id_dic.items():
                if class_name == valc:
                    each_t_class = keyc
            classid_termid = [each_t_class, new_etweet_list]

            total_dic[int(lin[0])] = classid_termid

        fin.close()
    print(total_dic)


    with open('feats1.test', 'w') as fout:
        for keyt, valt in total_dic.items():

            fout.write(str(valt[0]) + '\t')
            for y in range(len(valt[1])):
                fout.write(str(valt[1][y]) + ':' + "1" + '\t')
            fout.write("#" + str(keyt) + '\n')


def add_random_label():

    with open('feats.train', 'a') as fout2:
       for i in range(10):
            fout2.write(str(random.randint(20, 100)) + '\t' + str(random.randint(10, 10000)) + ":" + "1" + '\t' + str(random.randint(10, 10000)) + ":" + "1" + '\t' + str(random.randint(10, 10000)) + ":" + "1" + '\t' + str(random.randint(10, 10000)) + ":" + "1")
            fout2.write("\t" + "#unknown_label" + "\n")


def evaluation():
    pred_list = []
    with open("pred3.out", 'r', encoding='utf-8') as f4:
        for l in f4.readlines():
            lin = l.split(" ")
            pred_list.append(lin[0])
    print(pred_list)

    feats_list = []
    with open("feats1.test", 'r', encoding='utf-8') as f5:
        for l1 in f5.readlines():
            lin1 = l1.split("\t")
            feats_list.append(lin1[0])
    print(feats_list)


    p_list = []
    r_list = []
    f_list = []

    #pred_list = ['7', '8', '9', '1', '4', '1', '6', '4', '5', '5', '6']
    #feats_list = ['11', '8', '9', '1', '12', '1', '6', '5', '5', '5', '5']
    TP = 0
    for i in range(len(pred_list)):
        if pred_list[i] == feats_list[i]:
            TP = TP + 1
    accuracy = TP / len(pred_list)
    print(accuracy)


    pre_list2 = []
    fea_list3 = []


    for b in range(1, 15):
        list1 = []
        for a in range(len(pred_list)):
            if int(pred_list[a]) == b:
                list1.append(a+1)
        pre_list2.append(list1)
    print(pre_list2)

    for b in range(1, 15):
        list1 = []
        for a in range(len(feats_list)):
            if int(feats_list[a]) == b:
                list1.append(a + 1)
        fea_list3.append(list1)

    print(fea_list3)

    pred_dic = {}
    for c in range(14):
        pred_dic[c+1] = pre_list2[c]
    print(pred_dic)

    feats_dic = {}
    for c in range(14):
        feats_dic[c+1] = fea_list3[c]
    print(feats_dic)

    for d in range(1, 15):
        tp = 0
        p = 0
        r = 0
        f = 0
        for e in feats_dic[d]:
            for g in pred_dic[d]:
                if e == g:
                    tp = tp + 1

        if len(pred_dic[d]) != 0:
            p = tp/len(pred_dic[d])
        if len(feats_dic[d])!= 0:
            r = tp/len(feats_dic[d])
        if p+r != 0:
            f = 2 * ((p * r) / (p + r))

        p_list.append(p)
        r_list.append(r)
        f_list.append(f)

    print(p_list)
    print(r_list)
    print(f_list)

    macro_f1 = sum(f_list)/14
    print(macro_f1)

    with open('Eval3.txt', 'w') as fout1:
        fout1.write("Accuracy ="+'\t' + ("%.3f" % accuracy) + "\n")
        fout1.write("Macro-F1 =" + '\t' + ("%.3f" % macro_f1) + "\n")
        fout1.write("Results per class:" + "\n")
        for u in range(14):
            fout1.write(str(u+1) + ":" + '\t' + "P=" + ("%.3f" % p_list[u]) + '\t' + "R=" + ("%.3f" % r_list[u]) + '\t' + "F=" + ("%.3f" % f_list[u]) + '\n')


def main():
    #give_term_id()
    #preprocess("RT @rundat_9: @mynameisjsmith: Migos Be Like #migos #revine #wednesday #turnup ???????? https://t.co/2bYTLlWnCS")
    #match_class_term()
    #add_random_label()
    evaluation()


if __name__ == "__main__":
    main()
