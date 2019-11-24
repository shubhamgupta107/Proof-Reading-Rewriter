import urllib
import requests
import nltk
import re
from nltk.stem.wordnet import WordNetLemmatizer as wn
from word_forms.word_forms import get_word_forms
# from threading import Thread
# from multiprocessing.pool import ThreadPool
import time
# class ThreadWithReturnValue(Thread):
#     def __init__(self, group=None, target=None, name=None,
#                  args=(), kwargs={}, Verbose=None):
#         Thread.__init__(self, group, target, name, args, kwargs)
#         self._return = None
#     def run(self):
#         print(type(self._target))
#         if self._target is not None:
#             self._return = self._target(*self._args,
#                                                 **self._kwargs)
#     def join(self, *args):
#         Thread.join(self, *args)
#         return self._return
# from pattern.en import lexeme
def api(s,mode=1):
    encoded_query = urllib.parse.quote(s)
    params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 4}
    params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
    response = requests.get('https://api.phrasefinder.io/search?' + params)
    assert response.status_code == 200
    if(mode==1):
        if(response.json()['phrases']):
            # print(response.json()['phrases'][0]['tks'])
            out = [i['tt'] for i in response.json()['phrases'][0]['tks'] if i['tg']==2]
            return out
        else:
            return []
    else:
        # print("hi")
        if(response.json()['phrases']):
            out = [j['tt'] for i in response.json()['phrases'] for j in i['tks'] if j['tg']==2 or j['tg']==1]
            # print(out)
            res = [] 
            [res.append(x) for x in out if x not in res]
            # print(res) 
            return res
        else:
            return []

def options(sent,i,s):
    length = len(sent)
    if(i==0):
        return s+" "+sent[i+1]+' '+sent[i+2]
    elif(i<=length-2):
        return sent[i-1]+' '+s+' '+sent[i+1]
    else:
        return sent[i-2]+' '+sent[i-1]+' '+s

# auxillary_verbs          =   ['to do', 'do', 'does', 'done', 'did', "didn’t", "doesn’t", 'did not',
#                                 'be', 'to be', 'been', 'am', 'are', 'is', 'was', 'were', "wasn’t",
#                                 'was not', "aren’t", 'are not', "weren’t" , 'were not','has', 'have',
#                                 'having', 'had', " hadn’t", 'had not','can','could','may','might',
#                                 'must','ought to','shall','should','will','would']
articles                 =   'a/an/the'
demonstrative_pronouns   =   'that/these/those/that'
interrogative_pronouns   =   'what/which/who/whom/whose/why'
preposition              =   'in/on/at'
possesives               =   'my/your/his/her/its/our/their/mine'
quantifiers              =   'all/every/most/many/much/some/few/little/any/no'

while True:
    inp = input()
    sent = nltk.word_tokenize(inp)
    suggestions = [[word] for word in sent]
    postag = nltk.pos_tag(nltk.word_tokenize(inp))
    start = time.time()
    for i in range(len(sent)):
        x = sent[i].lower()
        if(sent[i] in articles.split('/')):
            suggestions[i] = api(options(sent,i,articles)) or [sent[i]]
        elif(sent[i] in demonstrative_pronouns.split('/')):
            suggestions[i] = api(options(sent,i,demonstrative_pronouns)) or [sent[i]]
        elif(sent[i] in preposition.split('/')):
            suggestions[i] = api(options(sent,i,preposition)) or [sent[i]]
        elif(sent[i] in possesives.split('/')):
            suggestions[i] = api(options(sent,i,possesives)) or [sent[i]]
        elif(sent[i] in quantifiers.split('/')):
            suggestions[i] = api(options(sent,i,quantifiers)) or [sent[i]]
        elif(sent[i] in interrogative_pronouns.split('/')):
            suggestions[i] = api(options(sent,i,interrogative_pronouns)) or [sent[i]]
        elif(postag[i][1].startswith('VB')):
            l1 = list(get_word_forms(wn().lemmatize(sent[i],'v'))['v'])
            verbs_combined = '"'+'"/"'.join(word for word in l1)+'"'
            # print(verbs_combined)
            if(l1):
                suggestions[i] = api(options(sent,i,verbs_combined)) or [sent[i]]
        sent[i] = suggestions[i][0]
    end = time.time()
    print(end-start)
    print(suggestions)
    # print(' '.join(word for word in suggestions))4

            # l1 = ['a','an','the']
            # l2 = []
            # for j in l1:
            #     t = ThreadWithReturnValue(target=api,args=(options(sent,i,j),))
            #     t.start()
            #     l2.append(t.join())
            # l2 = [api(options(sent,i,j)) for j in articles]
            # print(api(options(sent,i,articles)))