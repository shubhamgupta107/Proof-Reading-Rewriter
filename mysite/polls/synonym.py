import numpy as np 
import urllib
import time
import re
import csv
import nltk
from nltk.corpus import stopwords ,wordnet
from nltk.tokenize import word_tokenize, sent_tokenize 
import itertools
import requests
import json
from nltk.stem.wordnet import WordNetLemmatizer
from word_forms.word_forms import get_word_forms

stop_words = set(stopwords.words('english'))
iitblingo = {}
iitblingo['bc'] = "branch-change"
iitblingo['rg'] = "relative-grading"
iitblingo['infi'] = "infinite"
iitblingo['machaxx'] = "awesome"
iitblingo['convo'] = "Convocation-hall"
iitblingo['chamkaa'] = "understood"
iitblingo['despo'] = "desperate"
iitblingo['DOSA'] = "Dean-of-Student-Affairs"
iitblingo['freshie'] = "freshman"
iitblingo['HOD'] = "Head-of-Department"
def getSynonyms(p):
	regex = re.compile('[@_!#$%^&*()<>?/}{~:]') 
	j = 0;
	corrections = {}
	wordsLists = nltk.word_tokenize(p);
	for word in wordsLists:
		if(word in iitblingo.keys()):
			corrections[word] = [iitblingo[word]]
		else:
			wordsList = nltk.word_tokenize(word) 
			wordsList = [w for w in wordsList if not w in stop_words]
			tagged = nltk.pos_tag(wordsList)
			if(len(tagged)!=0):
				if(tagged[0][1]=='JJ' or 
					tagged[0][1]=='JJR' or
					tagged[0][1]=='JJS' or
					tagged[0][1]=='RB' or
					tagged[0][1]=='RBR' or
					tagged[0][1]=='RBS' or
					tagged[0][1]=='VB' or
					tagged[0][1]=='VBD' or
					tagged[0][1]=='VBG' or
					tagged[0][1]=='VBN' or tagged[0][1]=='VBZ' ):
					string2 = ' '
					if(j-1>=0 and j+1<len(wordsLists)):
						string2 = wordsLists[j-1] + ' ' + wordsLists[j] + ' ' + wordsLists[j+1];
					num2 = 0;
					syns = wordnet.synsets(WordNetLemmatizer().lemmatize(tagged[0][0],'v'))
					ans = {}
					x=0
					for syn in syns:
						for w in syn.lemmas():
							if (w.name().lower()!=WordNetLemmatizer().lemmatize(tagged[0][0],'v') and regex.search(w.name()) == None):

								verbs_combined=w.name().lower()
								if(tagged[0][1]=='VB' or tagged[0][1]=='VBZ' or tagged[0][1]=='VBD' or tagged[0][1]=='VBG' or tagged[0][1]=='VBN'):
									l1 = list(get_word_forms(WordNetLemmatizer().lemmatize(w.name().lower(),'v'))['v'])
									if(len(l1)==0):
										x+=1;
										continue;
									else:
										verbs_combined = '"'+'"/"'.join(words for words in l1)+'"'
								if(string2!=' ' and string2!=""):
									string2 = wordsLists[j-1] + ' ' + verbs_combined + ' ' + wordsLists[j+1]
								k = w.name()
								if(num2 ==0):
									if(string2!=' ' and string2!=""):
										encoded_query = urllib.parse.quote(string2)
										params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3}
										params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
										response = requests.get('https://api.phrasefinder.io/search?' + params)
										if(len(response.json()['phrases'])!=0):
											# print(response.json())
											num2 = response.json()['phrases'][0]['mc'];
											l = [i['tt'] for i in response.json()['phrases'][0]['tks'] if i['tg']==2]
											# print(num2)
											if(len(l)!=0):
												k=l[0]
								ans[k]=10*num2
								num2=0;
								x+=1
					out = [x[0] for x in sorted(ans.items(), key = lambda x : -1*x[1])[:3]]
					corrections[tagged[0][0]] = out;
					
			j=j+1
	return(corrections)