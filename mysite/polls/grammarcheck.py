import urllib
import requests
import nltk
import re
from nltk.stem.wordnet import WordNetLemmatizer as wn
from word_forms.word_forms import get_word_forms
import time

def api(s,mode=1,string=""):
    # print(s)
    encoded_query = urllib.parse.quote(s)
    params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3}
    params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
    response = requests.get('https://api.phrasefinder.io/search?' + params)
    assert response.status_code == 200
    if(mode==1):
        if(response.json()['phrases']):
            out = [i['tt'] for i in response.json()['phrases'][0]['tks'] if i['tg']==2 or i['tg']==1]
            return out
        else:
            return []
    else:
        if(response.json()['phrases']):
            out = [j['tt'] for i in response.json()['phrases'] for j in i['tks'] if j['tg']==2 or j['tg']==1]
            res = []
            [res.append(x) for x in out if x not in res]
            if (string in out):
                return []
            return res
        else:
            return []

def options(sent,i,s):
    length = len(sent)
    if(i==0 or (i>0 and not sent[i-1].isalnum())):
        return s+" "+sent[i+1]+' '+sent[i+2]
    elif(i<=length-2 and sent[i+1].isalnum()):
        return sent[i-1]+' '+s+' '+sent[i+1]
    else:
        return sent[i-2]+' '+sent[i-1]+' '+s

auxillary_verbs          =   ['to do', 'do', 'does', 'done', 'did', "didn’t", "doesn’t", 'did not',
                                'be', 'to be', 'been', 'am', 'are', 'is', 'was', 'were', "wasn’t",
                                'was not', "aren’t", 'are not', "weren’t" , 'were not','has', 'have',
                                'having', 'had', " hadn’t", 'had not','can','could','may','might',
                                'must','ought to','shall','should','will','would']
articles                 =   'a/an/the'
demonstrative_pronouns   =   'that/these/those/that'
interrogative_pronouns   =   'what/which/who/whom/whose/why/where'
preposition              =   'in/on/at/below/beside/above/down'
possesives_1             =   'my/mine/our'
possesives_2             =   "your/your's"
possesives_3             =   "its/our/their/their's/whose"
quantifiers              =   'all/every/most/many/much/some/few/little/any/no/very'

def checkgrammar(inp):
    sent = nltk.word_tokenize(inp.lower())
    suggestions = [[word] for word in sent]
    postag = nltk.pos_tag(nltk.word_tokenize(inp))
    # print(postag)
    start = time.time()
    for i in range(len(sent)):
        x = sent[i].lower()
        if(sent[i] in articles.split('/')):
            suggestions[i] = api(options(sent,i,articles)) or [sent[i]]
        elif(sent[i] in demonstrative_pronouns.split('/')):
            suggestions[i] = api(options(sent,i,demonstrative_pronouns)) or [sent[i]]
        elif(sent[i] in preposition.split('/')):
            x = options(sent,i,preposition)
            if(i<len(sent)-2):
                x = x + ' '+sent[i+2]
            suggestions[i] = api(x) or [sent[i]]
        elif(sent[i] in possesives_1.split('/')):
            suggestions[i] = api(options(sent,i,possesives_1),2) or [sent[i]]
        elif(sent[i] in possesives_2.split('/')):
            suggestions[i] = api(options(sent,i,possesives_2),2) or [sent[i]]
        elif(sent[i] in possesives_3.split('/')):
            suggestions[i] = api(options(sent,i,possesives_3),2) or [sent[i]]
        elif(sent[i] in quantifiers.split('/')):
            suggestions[i] = api(options(sent,i,quantifiers),2) or [sent[i]]
        elif(sent[i] in interrogative_pronouns.split('/')):
            suggestions[i] = api(options(sent,i,interrogative_pronouns)) or [sent[i]]
        elif(sent[i] in auxillary_verbs):
            l1 = list(get_word_forms(wn().lemmatize(sent[i],'v'))['v'])
            verbs_combined = '"'+'"/"'.join(word for word in l1)+'"'
            if(l1):
                suggestions[i] = api(options(sent,i,verbs_combined,),2,sent[i]) or [sent[i]]
        elif(postag[i][1].startswith('VB')):
            l1 = list(get_word_forms(wn().lemmatize(sent[i],'v'))['v'])
            verbs_combined = '"'+'"/"'.join(word for word in l1)+'"'
            if(l1):
                suggestions[i] = api(options(sent,i,verbs_combined,),1,sent[i]) or [sent[i]]
        elif(postag[i][1].startswith('NN') or (i<len(sent)-1 and postag[i][1].startswith('JJ') and postag[i+1][1].startswith('NN'))):
            if(i==0):
                suggestions[i] = api(articles+' '+options(sent,i,sent[i])) or [sent[i]]
            else:
                if(postag[i-1][1].startswith('VB')):
                    suggestions[i] = [x+' '+sent[i] for x in api(sent[i-1]+' ? '+sent[i],2)] or [sent[i]]
        sent[i] = suggestions[i][0]
    end = time.time()
    newsent = nltk.word_tokenize(inp)
    for i in range(len(sent)):
        if newsent[i] in suggestions[i]:
            suggestions[i].remove(newsent[i])
    #print(end-start)
    return(suggestions)
