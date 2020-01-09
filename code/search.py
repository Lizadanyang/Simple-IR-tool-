import xml.etree.cElementTree as ET
import string
from stemming.porter2 import stem
import re

#for NOT state
def get_all_docID():
    all_docid = []
    # dict_of_data = {'ID': '', 'Text': ''}
    tree = ET.ElementTree(file='trec.5000.xml')
    root = tree.getroot()

    for i, obj in enumerate(root):

        text_id = obj.find('DOCNO').text.strip()
        all_docid.append(int(text_id))
    #print(all_docid)
    return all_docid


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

    fin.close()
    for lin in list1:
        l = lin.lower()
        word = l.strip().split(' ')
        for stopword in stopwords:
            for wor in word:
                if str(stopword) == str(wor):
                    word.remove(wor)
        list2.append(word)

    for li in list2:
        for l in li:
            stemword = stem(l)
            stemwords.append(stemword)
    #print(stemwords,type(stemwords),len(stemwords))
    return stemwords

#load index.txt as dict()
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
            docid = int(doc.strip().split(':')[0])# docID
            #print(docid)
            posi = doc.strip().split(':')[1].split(',')#position
            #posi = list(filter(None, posi))
            posi = map(int, posi)#str change into int
            posii = list(posi)
            doc_dict[docid] = posii
            index_dict[term] = doc_dict

    #print(index_dict)
    return index_dict

#term:string, one term
#output: list of docID 
def find_docid(term):
    docID = []
    index_dict = read_index()#dict
    for ind in index_dict:
        for doci in index_dict[ind]:
            if str(ind) == str(term):
                docID.append(doci)
    #print(docID)
    return docID

#term:string, one term
#output: list of ([docID1,docID2],{docID1:[posi1,posi2]} 
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

#out: list of "and" docID
#term1 and term2
def merge_and(term1, term2):

    term1_docid = find_docid(term1)
    term2_docid = find_docid(term2)

    i = 0
    j = 0

    result = []
    a = len(term1_docid)
    b = len(term2_docid)

    while i < a and j < b:
        if term1_docid[i] == term2_docid[j]:
            result.append(term1_docid[i])
            i += 1
            j += 1
        elif term1_docid[i] < term2_docid[j]:
            i += 1
        else:
            j += 1
    #print(result)
    return result

#output:list
#term1 or term2
def merge_or(term1, term2):
    term1_docid = find_docid(term1)
    term2_docid = find_docid(term2)
    result = []

    for t1 in term1_docid:
        for t2 in term2_docid:
            if t2 == t1:
                result.append(t2)
            if t2 not in result:
                result.append(t2)
        if t1 not in result:
            result.append(t1)

    #print(result)
    return result


#term1 and not term2
def merge_and_not(term1, term2):
    term1_docid = find_docid(term1)
    term2_docid = find_docid(term2)
    result = []
    term1_set = set(term1_docid)
    term2_set = set(term2_docid)
    result = term1_set-term2_set #set.difference()
    result = list(result)
    print(result)
    return result

#term1 or not term2
#first not term2, then or 
def merge_or_not(term1, term2):
    term1_docid = find_docid(term1)
    term2_docid = find_docid(term2)
    result = []
    term1_set = set(term1_docid)
    term2_set = set(term2_docid)
    all_doc = get_all_docID()
    print(all_doc, type(all_doc))
    not_term2 = set(all_doc) - term2_set
    result = term1_set | not_term2

    result = list(result)
    print(result)
    return result

#for merge to change word
def get_input(word):
    #print(word, type(word))

    iinput = word
    #print(iinput)
    #print(iinput)
    input_change = []
    for li in iinput:
        li = li.lower()
        #print(type(li))
        if li == 'or':
            input_change.append(li)
            #print('ssss', input_change)
            continue
        elif li == 'and':
            input_change.append(li)
            #print('ssss', input_change)
            continue
        elif li == 'not':
            input_change.append(li)
            # print('ssss', input_change)
            continue
        else:
            li = "".join(preprocess(li))
        input_change.append(li)

    #print(input_change)

    return input_change


# input: "income taxes"
# output: docid list
def phrash_search(query):
    input_terms = query.split(' ')
    input_terms[0] ="".join(preprocess(input_terms[0]))
    input_terms[1] ="".join(preprocess(input_terms[1]))
    print(input_terms[0], input_terms[1])
    #find intersection of docIDs for terms
    get_doc_result = merge_and(input_terms[0], input_terms[1])
    if get_doc_result != None:
        list5 = []

        for element in input_terms:
            posidd_list = list(find_posiid(element))#find position of docID

            #print(element, posidd_list, type(posidd_list))
            pos = posidd_list[1]
            #print(pos, type(pos))
            list5.append(pos)
        dic1 = list5[0]#docID
        dic2 = list5[1]#position

        list6 = []
        for key1, value1 in dic1.items():
            #print(key1, value1)
            for key2, value2 in dic2.items():
                if key1 == key2:
                    for v1 in value1:
                        for v2 in value2:
                            if v2-1 == v1:
                                if key1 not in list6:
                                    list6.append(key1)
                                #list6.append(":")
                                #list6.append(v1)

                    #list6.append(key2+":"+dic2[key2].values())
        print("list6", list6)

    else:
        print("NOT A PHRASH!")

    return list6


# input: #10(income, taxes)
# output: docid list
def proximity_search(query):
    a = re.search(r'#(\d+)\((.*?),(.*?)\)', query)
    numb = int(a.group(1))
    print(numb)
    term1 = a.group(2)
    term2 = a.group(3)
    term1 = preprocess(term1)
    term1 = ''.join(term1)
    term2 = preprocess(term2)
    term2 = ''.join(term2)

    get_doc_result = merge_and(term1, term2)

    if get_doc_result != None:

        dic1 = find_posiid(term1)[1]
        dic2 = find_posiid(term2)[1]
        list7 = []
        for key1, value1 in dic1.items():

            for key2, value2 in dic2.items():
                if key1 == key2:
                    for v1 in value1:
                        for v2 in value2:
                            if 0 < v2 - v1 < (numb+1) or 0 < v1-v2 < (numb+1):
                                if key1 not in list7:
                                    list7.append(key1)

        print("list7", list7)

    else:
        print("DON'T HAVE SUCH A DOC!")
    return list7


#search query one by one
def search():
    with open("queries.boolean.txt", 'r', encoding='utf-8') as fin:
        inf_query_file = fin.read()
        fin.close()
    with open('results.boolean.txt', 'w') as fout:

        for l in inf_query_file.split('\n')[:-1]:
            a, b = l.split(' ', 1)  #split("", split times)
            qid = list(a)
            query = b.split()

            print(qid)
            print(query)

            if len(query) == 1:
                x = preprocess(query[0])
                print(x, type(x))
                result_doc_id = find_docid(x[0])
                print(result_doc_id)

            elif len(query) == 2:
                if '#' in query[0]:
                    input2 = "".join(query)
                    print(input2)
                    result_doc_id = proximity_search(input2)
                    print(result_doc_id)
                if '"' in query[0]:
                    input2 = " ".join(query)
                    print(input2)
                    result_doc_id = phrash_search(input2)
                    print(result_doc_id)
            elif len(query) == 3:
                input1 = get_input(query)
                print(input1)

                if input1[1] == "and":
                    result_doc_id = merge_and(input1[0], input1[2])
                if input1[1] == 'or':
                    result_doc_id = merge_or(input1[0], input1[2])
                print(result_doc_id)

            elif len(query) == 4:
                if '"' in query[0]:
                    input3 = " ".join(query[i] for i in range(2))
                    print(input3)
                    term11 = phrash_search(input3)
                    print("term1", term11)
                    query4 = ''.join(preprocess(query[3]))
                    query4_doc = find_docid(query4)
                    print("query4_doc", query4_doc)
                    result_doc_id = list(set(term11) & set(query4_doc))
                    print(result_doc_id)
                else:
                    input4 = get_input(query)
                    print(input4)

                    if input4[2] == "not":

                        if input4[1] == 'and':
                            result_doc_id = merge_and_not(input4[0], input4[3])
                        if input4[1] == 'or':
                            result_doc_id = merge_or_not(input4[0], input4[3])
                    print(result_doc_id)
            elif len(query) == 5:
                if '"' in query[0]:
                    input5 = " ".join(query[i] for i in range(2))
                    print(input5)
                    term111 = phrash_search(input5)
                    print("term111", term111)

                    if query[3] == "NOT":
                        print(query[3])
                        query5 = "".join(preprocess(query[4]))
                        query5_doc = find_docid(query5)
                        result_doc_id = set(term111) - set(query5_doc)
                        print(result_doc_id)
                    else:
                        print(query)
                        input6 = " ".join(query[i] for i in range(3, 5))
                        print("input6", input6)
                        term22 = phrash_search(input6)
                        print("term22", term22)
                        result_doc_id = set(term111) & set(term22)
                        print(result_doc_id)

            for d in result_doc_id:
                fout.write("".join(qid) + '\t' + '0' + '\t' + str(d) + '\t\t' + '0' + '\t' + '1' + '\t' + '0' + '\n')
                #fout.write(str(qid) + '\t\t' + '0' + '\t\t' + str(d) + ' 0 1 0' + '\n')


def main():
    search()


if __name__ == "__main__":
    main()

