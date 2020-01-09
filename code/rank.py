import xml.etree.cElementTree as ET
import string
from stemming.porter2 import stem
import math


def get_all_docID():
    all_docid = []
    # dict_of_data = {'ID': '', 'Text': ''}
    tree = ET.ElementTree(file='trec.5000.xml')
    root = tree.getroot()

    for i, obj in enumerate(root):

        text_id = obj.find('DOCNO').text.strip()
        all_docid.append(int(text_id))

    #print(all_docid)
    return len(all_docid)


def preprocess(text):

    list1 = []
    list2 = []
    stopwords = []
    stemwords = []
    st = "englishST.txt"
    words = str(text)
    words = words.replace('\n\t', ' ')
    #print('words', words, type(words))

    for c in string.punctuation:
        words = words.replace(c, "")

    list1.append(words)
    #print(len(list1))
    with open(st, 'r', encoding='utf-8') as fin:
        for l in fin.readlines():
            stopwords.append(l.strip('\n'))

        #print(len(stopwords))
    fin.close()
    for lin in list1:
        l = lin.lower()
        word = l.strip().split(' ')
        # print(word)

        for stopword in stopwords:
            for wor in word:
                if str(stopword) == str(wor):
                    word.remove(wor)
        # print(word)
        list2.append(word)
    for li in list2:
        for l in li:
            # print(l)
            stemword = stem(l)
            # print(stemword)
            stemwords.append(stemword)
    # print(stemwords, type(stemwords))
    #print(stemwords,type(stemwords),len(stemwords))
    return stemwords


def read_index():

    with open("index.txt", 'r', encoding='utf-8') as fin:
        index_inf = fin.read()
    index_dict = dict()
    for line in index_inf.split('\n\n')[:-1]:

        term = line.split('\n')[0]
        term = term.replace(':', '').strip()
        #print(term)
        doc_inf = line.split('\n\t\t\t')[1:]

        #print(doc_inf)
        doc_dict = dict()
        for doc in doc_inf:
            docid = int(doc.strip().split(':')[0])
            #print(docid)

            posi = doc.strip().split(':')[1].split(',')
            #posi = list(filter(None, posi))

            posi = map(int, posi)

            posii = list(posi)

            doc_dict[docid] = posii
            index_dict[term] = doc_dict

    #print(index_dict)
    return index_dict


def find_docid(term):
    docID = []
    index_dict = read_index()
    for ind in index_dict:
        for doci in index_dict[ind]:
            if str(ind) == str(term):
                docID.append(doci)
    #print(docID)
    return docID


def find_posiid(term):
    docID = []
    posiID = dict()
    index_dict = read_index()
    #print(index_dict)
    for ind in index_dict:
        for doci in index_dict[ind]:
            if str(ind) == str(term):
                for docidd,  posidd in index_dict[ind].items():
                    #print(docidd, type(docidd))
                    #print("iss", posidd)
                    posiID[docidd] = posidd

                docID.append(doci)

    #print(posiID)
    #print(docID)
    return docID, posiID

    
#output: int
def get_df(term):
    a = find_docid(term)
    #print(a, type(a))
    df = len(a)
    print(df)
    return df

#document:int
#output: int
def get_tf(term, document):
    b = find_posiid(term)
    #print(b, type(b))
    term_doc_poi = b[1]
    #print(term_doc_poi, type(term_doc_poi))
    tf = len(term_doc_poi[document])
    #print(term_doc_poi[document])
    print(tf)
    return tf


def get_weight(term, document):
    N = get_all_docID()
    #print(N)
    tf = get_tf(term, document)
    df = get_df(term)
    w = (1+math.log10(tf))*(math.log10(N/df))
    print(w)
    return w


def rank_in_or():
    with open("queries.ranked.txt", 'r', encoding='utf-8') as fin:
        inf_query_file = fin.read()
        fin.close()
    with open('results.ranked.txt', 'w') as fout:

        for l in inf_query_file.split('\n')[:-1]:
            a, b = l.split(' ', 1)  #split("", split times)
            qid = a

            query = b.split()

            #print(qid, type(qid))
            #print(query)
            new_query = preprocess(query)
            #print(new_query)
            eterm_doc = []
            for each_term in new_query:

                eterm_doc.append(find_docid(each_term))
            new_term_doc = set()
            for e1 in range(len(eterm_doc)):
                eterm_doc[e1] = set(eterm_doc[e1])
                #print(type(eterm_doc[e1]), eterm_doc[e1])
                new_term_doc = new_term_doc | eterm_doc[e1]#find all doc for this query

            union_doc = list(new_term_doc)
            #print(union_doc)#doc并集
            each_doc_score = {}
            for doc2 in union_doc:
                weight = 0
                for small_term in new_query:
                    small_term_doc = find_docid(small_term)
                    if doc2 in small_term_doc:
                        weight += get_weight(small_term, doc2)#sum of score

                each_doc_score[doc2] = weight
                #print(each_doc_score)
            #print("111", each_doc_score)
            #sort by value=score
            sort_each_doc = sorted(each_doc_score.items(), key=lambda x: x[1], reverse=True)
            print(sort_each_doc, type(sort_each_doc))

            for i, index in enumerate(sort_each_doc):
                if i == 1000:
                    break
                fout.write("".join(qid) + '\t' + '0' + '\t' + str(index[0]) + '\t' + '0' + '\t' + str(index[1]) + '\t' + '0' + '\n')


def rank_in_and():
    with open("queries.ranked.txt", 'r', encoding='utf-8') as fin:
        inf_query_file = fin.read()
        fin.close()
    with open('results.ranked.txt', 'w') as fout:

        for l in inf_query_file.split('\n')[:-1]:
            a, b = l.split(' ', 1)  # split("", split times)
            qid = a
            query = b.split()
            print(qid, type(qid))
            print(query)
            new_query = preprocess(query)
            print(new_query)
            eterm_doc = []
            for each_term in new_query:
                eterm_doc.append(find_docid(each_term))
            #new_term_doc = set()
            for e1 in range(len(eterm_doc)):
                eterm_doc[e1] = set(eterm_doc[e1])
                if e1 == 0:
                    new_term_doc = eterm_doc[e1]

                print(type(eterm_doc[e1]), eterm_doc[e1])
                new_term_doc = new_term_doc & eterm_doc[e1]

            union_doc = list(new_term_doc)
            print(union_doc)#docid union set
            each_doc_score = {}
            for doc2 in union_doc:
                weight = 0
                for small_term in new_query:
                    small_term_doc = find_docid(small_term)
                    if doc2 in small_term_doc:
                        weight += get_weight(small_term, doc2) #and set

                each_doc_score[doc2] = weight
                print(each_doc_score)
            print("111", each_doc_score)
            sort_each_doc = sorted(each_doc_score.items(), key=lambda x: x[1], reverse=True)
            print(sort_each_doc, type(sort_each_doc))

            for index in sort_each_doc:
                fout.write("".join(qid) + '\t' + '0' + '\t' + str(index[0]) + '\t' + '0' + '\t' + str(
                    index[1]) + '\t' + '0' + '\n')


def main():
    rank_in_or()
    #rank_in_and()


if __name__ == "__main__":
    main()

