import xml.etree.cElementTree as ET
import string
from stemming.porter2 import stem
#command: python index.py > index.txt
#will get the print version in index.txt


#preprocessing the input text
def preprocess(text):

    list1 = []
    list2 = []
    stopwords = []
    stemwords = []
    st = "englishST.txt"# stop word file
    words = str(text)
    words = words.replace('\n\t', ' ')#to remove the \n\t on each line end
    #print('words', words, type(words))

    for c in string.punctuation:
        words = words.replace(c, ' ')#Tokenisation

    list1.append(words)
    #print(len(list1))
    #read stopword file and into a list
    with open(st, 'r', encoding='utf-8') as fin:
        for l in fin.readlines():
            stopwords.append(l.strip('\n'))

        #print(len(stopwords))
    fin.close()

    for lin in list1:
        l1 = lin.lower()
        word = l1.strip().split(' ')
        # print(word)
        #replace stop word
        for stopword in stopwords:
            for wor in word:
                if str(stopword) == str(wor):
                    word.remove(wor)
        # print(word)
        list2.append(word)

    for li in list2:
        for l2 in li:
            # print(l)
            stemword = stem(l2)
            # print(stemword)
            stemwords.append(stemword)
    # print(stemwords, type(stemwords))
    stemwords.remove('')#can not remove all blank space
    astemwords = list(filter(None, stemwords))# replace all blank space in the term list

    #print(astemwords, type(astemwords), len(astemwords))
    return astemwords


def inverted_index():
    list_dict = []
    #dict_of_data = {'ID': '', 'Text': ''}
    tree = ET.ElementTree(file='trec.5000.xml')
    root = tree.getroot()
#read XML file's ID HEADLINE TEXT
    for i, obj in enumerate(root):
        dict_of_data = {'ID': '', 'Text': ''}
        #separated headline and text by " "
        text = obj.find("HEADLINE").text.strip('\n').strip('\t').strip()+str(" ")+obj.find("TEXT").text.strip('\n').strip('\t').strip()
        text_id = obj.find('DOCNO').text.strip()

        #print("text", text)
        dict_of_data['ID'] = text_id
        #print(i)
        dict_of_data['Text'] = preprocess(text)
        list_dict.append(dict_of_data)

    #print("list_dict:", list_dict)
    #list_dict=list_dict.remove(' ')
    list_term = []
#list_dict: list inclues all docid text
    for li in list_dict:
        #even number of value is docid
        for j, terms in enumerate(li.values()):
            if j % 2 == 0:
                continue
            #remove blank space
            tterms = list(filter(None, terms))
            #print(tterms)
            #count position, use now
            pposi=1
            for term in tterms:
                dict_of_term = {'term': '', 'ID': '','POSI': ''}
                dict_of_term['term'] = term
                dict_of_term['ID'] = li['ID']
                dict_of_term['POSI'] = pposi
                list_term.append(dict_of_term)
                pposi += 1

    e = []
    x = []
    zinver_index = dict()
    ztemp = []
    #count position, not use any more
    for z in list_term:
        e.append(z['ID'])
        if len(e) == 1:
            posi = 1

        else:
            if e[-1] == e[-2]:
                idx = posi+1
                posi = idx
            else:
                posi = 1

        # print('z', z)
        y = z['term']
        if y not in x:
            x.append(y)
            # print('x', x)
        ztemp.append(list())

        for i, j in enumerate(x):
            # print("i", i, "j", j)
            # print(ztemp)

            posi_dict = dict()
            posi_list = []
            if y == j:

                if z['ID'] not in ztemp[i]:

                    if z['POSI'] not in posi_list:
                        posi_list.append(z['POSI'])
                        posi_dict[z['ID']] = z['POSI']
                        ztemp[i].append(posi_dict)
                    # print(ztemp[i])

                        zinver_index[y] = ztemp[i]
                        break

    #print(zinver_index)
    # the zinver_index is invered index result
    sort_index = sorted(zinver_index.items(), key=lambda x: x[0], reverse=False)
    #key=lambda x:x[0] sort by key

    #print(sort_index, type(sort_index))
    return sort_index


def write_index(sort_index):

    for index in sort_index:
        key_idx = 0
        print(index[0], ":", end="")
        for dic_list in index[1]:
            for key_name, value_name in dic_list.items():
                if key_idx == key_name:
                    print(',' + str(value_name), end="")
                else:
                    print('\n' + '\t\t\t' + str(key_name) + ':' + str(value_name), end="")
                    key_idx = key_name
        print('\n')


def main():

    sort_index_result = inverted_index()
    write_index(sort_index_result)


main()


