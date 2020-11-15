from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re

from bktreespellchecker import BKTree
from underthesea import word_tokenize as word_token_VN
from nltk import word_tokenize as word_token_EN
from bktreespellchecker.distance import damerau_levenshtein_distance

TEST = False
IS_DL = True
DELTA = 1

# Create BK Tree from dictionary
dict_path_VN = 'spellcheckapp\static/vn-test-dict.txt' if TEST else 'spellcheckapp\static/vnese_dict.txt'
vn_words = [w.strip() for w in open(dict_path_VN, encoding='utf-8').readlines()]
bkt_VN = BKTree.from_file(dict_path_VN, distance_func=damerau_levenshtein_distance if IS_DL else None)

dict_path_EN = 'spellcheckapp\static\en-test-dict.txt' if TEST else 'spellcheckapp\static/en_dict.txt'
en_words = [w.strip() for w in open(dict_path_EN , encoding='utf-8').readlines()]
bkt_EN = BKTree.from_file(dict_path_EN, distance_func=damerau_levenshtein_distance if IS_DL else None)

# Create your views here.
def index(request):
    return render(request, 'index.html')

# remove puncctuation from string
def remove_punct(s):
    return re.sub(r'[^\w\s]','',s)

#Input: Text need to check | Output: dictionary with keys is word need to be changed
#                                   value is suggested words
def spell_check(sentence, is_VN):
    if(is_VN == 'true'):
        bkt = bkt_VN
        sentence = remove_punct(sentence).lower()
        words_lst = word_token_VN(sentence)
        corrected_lst = {}
        for word in words_lst:
            if word in vn_words:
                continue
            if len(word) == 1:
                continue
            corrected_word = bkt.search(word, DELTA)
            if corrected_word != []:
                for i in corrected_word:
                    if word in corrected_lst:
                        corrected_lst[word].append(i[1])
                    else: corrected_lst[word] = [i[1]]
    else:
        bkt = bkt_EN
        sentence = remove_punct(sentence).lower()
        words_lst = word_token_EN(sentence)
        corrected_lst = {}
        for word in words_lst:
            if word in en_words:
                continue
            if len(word) == 1:
                continue
            corrected_word = bkt.search(word, 2)
            if corrected_word != []:
                for i in corrected_word:
                    if word in corrected_lst:
                        corrected_lst[word].append(i[1])
                    else: corrected_lst[word] = [i[1]]
    return corrected_lst # {'anh': ['ảnh', 'ánh']}

@csrf_exempt
def submitquery(request):
    if request.method == 'POST':
        mytextarea = request.POST.get('mytextarea')
        is_VN = request.POST.get('is_VN')
        response_data = spell_check(mytextarea, is_VN)
        return HttpResponse(json.dumps(response_data), content_type="application/json")

