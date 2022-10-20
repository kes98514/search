#정보검색 과제 2017113376 이지호

import re
import math
from konlpy.tag import Okt

print("문서파일을 읽어옵니다.")

readFile = open("full_corpus.txt", 'r', encoding='UTF-8')

lines = readFile.readlines()

korea = Okt()

korean_preprocessor = re.compile('[^ ㄱ-ㅣ가-힣0-9]+')

title_list = []
term_dict = {}

docNumber = -1;

for line in lines:
    if(line.find("<title>") != -1):
        temp = line.replace("<title>","")
        temp = temp.replace("</title>","")
        title_list.append(temp)
        docNumber = docNumber +1
    else:
        korean_line = korean_preprocessor.sub('',line)
        
        if(korean_line != "" or korean_line != ' '):
            word_list = korea.pos(korean_line)
            
            josa_delete_list = []
            for word in word_list:
                if word[1] != 'Josa':
                    josa_delete_list.append(word[0])
            
            for word in josa_delete_list:
                if word not in term_dict:
                    term_dict[word] = {docNumber : 1}
                else:
                    if docNumber not in term_dict[word]:
                        term_dict[word][docNumber] = 1
                    else:
                        term_dict[word][docNumber] = term_dict[word][docNumber]+1              

document_size = len(title_list)
tf_idf_weight_dict = {}

for term in term_dict:
    doc_freq = len(term_dict[term])
    
    for document_number in term_dict[term]:
        document_count = term_dict[term][document_number]

        if term not in tf_idf_weight_dict:
            tf_idf_weight_dict[term] = {}

        tf_idf_weight_dict[term][document_number] = (1 + math.log10(document_count)) * math.log10(document_size/doc_freq)

doc_length_list = list(0 for i in range(0,100))

for term in tf_idf_weight_dict:
    
    for document_number in tf_idf_weight_dict[term]:
        doc_length_list[document_number] += tf_idf_weight_dict[term][document_number] * tf_idf_weight_dict[term][document_number]

for i in range (0, len(doc_length_list)):
    doc_length_list[i] = math.sqrt(doc_length_list[i])

for term in tf_idf_weight_dict:
    for document_number in tf_idf_weight_dict[term]:
        tf_idf_weight_dict[term].update({document_number : tf_idf_weight_dict[term][document_number] / doc_length_list[document_number]})

readFile.close()

print("문서 전처리를 완료했습니다!")

answer_dict = {}

for i in range(0,100):
    answer_dict[i] = 0

query_str = input("질의어를 입력해주세요 : ")

preprocess_query = korea.pos(query_str)
query = []
for word in preprocess_query:
    if word[1] != 'Josa':
        query.append(word[0])

print(f"입력된 질의어 : {query}")

for word in query:
    if word in tf_idf_weight_dict:
        for document_number in tf_idf_weight_dict[word]:
            answer_dict[document_number] += tf_idf_weight_dict[word][document_number]

sorted_answer_dict = sorted(answer_dict.items(), key=lambda x: x[1], reverse=True)

for i in range(0,5):
    print(f"{title_list[sorted_answer_dict[i][0]]}유사도 : {round((sorted_answer_dict[i][1]*100), 2)}%")