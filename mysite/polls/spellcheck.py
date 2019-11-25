import re
from collections import Counter
import time
import urllib
import requests
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
stop_words = set(stopwords.words('english'))
# def words(text): return re.findall(r'\w+', text.lower())
WORDS = {}
f = open("polls/dictionary.txt", "r")
dictionary = f.readlines()
for line in dictionary:
    word,freq = line.split()
    WORDS[word] = int(freq)
# WORDS = Counter(words(open("data.txt").read()))
WORDS['the'] = 23135851162
def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def options(sent,i,s):
    length = len(sent)
    if(i==0 or (i>0 and not sent[i-1].isalnum())):
        return s+" "+sent[i+1]+' '+sent[i+2]
    elif(i<=length-2 and sent[i+1].isalnum()):
        return sent[i-1]+' '+s+' '+sent[i+1]
    else:
        return sent[i-2]+' '+sent[i-1]+' '+s

def candidates(inp):
    sent = word_tokenize(inp.lower())
    "Generate possible spelling corrections for word."
    original = [word for word in sent]
    suggestions = [[word] for word in sent]
    for i in range(len(sent)):
        if(not sent[i].isalnum()):
            continue
        l = []
        temp1 = list(sorted(known([sent[i]]),key=P,reverse=True))
        temp2 = []
        temp3 = []
        contains = False
        if(temp1):
            contains = True
            if(sent[i] not in stop_words):
                if(api(options(sent,i,sent[i]))>500):
                    suggestions[i] = temp1
                    continue
            else:
                continue
        temp2 = list(sorted(known(edits1(sent[i])),key=P,reverse=True))
        temp3 = list(sorted(known(edits2(sent[i])),key=P,reverse=True))
        for item in (temp2+temp3):
            if(item not in l):
                l.append(item)
        number = min(3,len(l))
        l1 = l[:number]
        if(contains):
            words_combined = '"'+'"/"'.join(word for word in l1)+'"'
            suggestions[i] = api(options(sent,i,words_combined),2) or [sent[i]]
        else:
            suggestions[i] = l1
        sent[i] = suggestions[i][0]
    return suggestions

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def api(s,mode=1):
    # print(s)
    encoded_query = urllib.parse.quote(s)
    params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3}
    params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
    response = requests.get('https://api.phrasefinder.io/search?' + params)
    assert response.status_code == 200
    if(mode==1):
        if(response.json()['phrases']):
            out = response.json()['phrases'][0]['mc']
            return out
        else:
            return 0
    else:
        if(response.json()['phrases']):
            out = [j['tt'] for i in response.json()['phrases'] for j in i['tks'] if j['tg']==2 or j['tg']==1]
            res = []
            [res.append(x) for x in out if x not in res]
            return [res[0]]
        else:
            return []

def giveSuggestions(a):
    # print(WORDS['is'])
    start = time.time()
    tempval = candidates(a)
    sent = word_tokenize(a)
    for i in range(len(sent)):
        if sent[i] in tempval[i]:
            tempval[i].remove(sent[i])
    return(tempval)
    #end = time.time()
    #print(end-start)