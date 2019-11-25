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
## Loading the dictionary frequency wise
# TRIGRAMS = {}
# f = open("w3_.txt", "r")
# dictionary = f.readlines()
# for line in dictionary:
#     freq,word1,word2,word3 = line.split()
#     trigram = word1 + ' ' + word2 + ' ' + word3
#     TRIGRAMS[trigram] = int(freq)

iitblingo = {}
iitblingo['bc'] = "branch change"
iitblingo['rg'] = "relative grading"
iitblingo['infi'] = "infinite"
iitblingo['machaxx'] = "awesome"
iitblingo['convo'] = "Convocation hall"
iitblingo['chamkaa'] = "understood"
iitblingo['despo'] = "desperate"
iitblingo['DOSA'] = "Dean of Student Affairs"
iitblingo['freshie'] = "freshman"
iitblingo['HOD'] = "Head of Department"
p = input();
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
		#print(tagged)
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
				# print(wordsLists[j])
				# string1 = ' '
				string2 = ' '
				# string3 = ' '
				# if(j-2>=0):
				# 	string1 = wordsLists[j-2] + ' ' + wordsLists[j-1] + ' ' + wordsLists[j];
				if(j-1>=0 and j+1<len(wordsLists)):
					string2 = wordsLists[j-1] + ' ' + wordsLists[j] + ' ' + wordsLists[j+1];
				# if(j+2<len(wordsLists)):
				# 	string3 = wordsLists[j] + ' ' + wordsLists[j+1] + ' ' + wordsLists[j+2];
				# num1 = 0;
				num2 = 0;
				# num3 = 0;
				# if(string1!=' '):
				# 	try:
				# 		num1 = TRIGRAMS[string1]
				# 	except:
				# 		num1=0
				# if(string2!=' '):
				# 	try:
				# 		num2 = TRIGRAMS[string2]
				# 	except:
				# 		num2=0
				# if(string3!=' '):
				# 	try:
				# 		num3 = TRIGRAMS[string3]
				# 	except:
				# 		num3=0
				syns = wordnet.synsets(WordNetLemmatizer().lemmatize(tagged[0][0],'v'))
				ans = {}
				x=0
				for syn in syns:
					for w in syn.lemmas():
						if (w.name().lower()!=WordNetLemmatizer().lemmatize(tagged[0][0],'v') and regex.search(w.name()) == None):
							# print(w.name().lower())
							verbs_combined=w.name().lower()
							if(tagged[0][1]=='VB' or tagged[0][1]=='VBZ' or tagged[0][1]=='VBD' or tagged[0][1]=='VBG' or tagged[0][1]=='VBN'):
								l1 = list(get_word_forms(WordNetLemmatizer().lemmatize(w.name().lower(),'v'))['v'])
								if(len(l1)==0):
									x+=1;
									continue;
								else:
									verbs_combined = '"'+'"/"'.join(words for words in l1)+'"'
							# print(verbs_combined)
							
							# if(string1!=' 'and string1!=""):
							# 	string1 = wordsLists[j-2] + ' ' + wordsLists[j-1] + ' ' + verbs_combined
							if(string2!=' ' and string2!=""):
								string2 = wordsLists[j-1] + ' ' + verbs_combined + ' ' + wordsLists[j+1]
							# if(string3!=' ' and string3!=""):
							# 	string3 = verbs_combined + ' ' + wordsLists[j+1] + ' ' + wordsLists[j+2]
							# if(num1!=0):
							# 	try:
							# 		num1 = TRIGRAMS[string1]
							# 	except:
							# 		num1=0
							# if(num2!=0):
							# 	try:
							# 		num2 = TRIGRAMS[string2]
							# 	except:
							# 		num2=0
							# if(num3!=0):
							# 	try:
							# 		num3 = TRIGRAMS[string3]
							# 	except:
							# 		num3=0
							k = w.name()
							if(num2 ==0):
								# if(string1!=' ' and string1!=""):
								# 	encoded_query = urllib.parse.quote(string1)
								# 	params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3}
								# 	params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
								# 	response = requests.get('https://api.phrasefinder.io/search?' + params)
								# 	if(len(response.json()['phrases'])!=0):
								# 		# print(response.json())
								# 		num1 = response.json()['phrases'][0]['mc']
								# 		l = [i['tt'] for i in response.json()['phrases'][0]['tks'] if i['tg']==2]
								# 		if(len(l)!=0):
								# 			k=l[0]
										# print(num1)
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
								# if(string3!=' ' and string3!=""):
								# 	encoded_query = urllib.parse.quote(string3)
								# 	params = {'corpus': 'eng-us', 'query': encoded_query, 'topk': 3}
								# 	params = '&'.join('{}={}'.format(name, value) for name, value in params.items())
								# 	response = requests.get('https://api.phrasefinder.io/search?' + params)
								# 	if(len(response.json()['phrases'])!=0):
								# 		# print(response.json())
								# 		num3 = response.json()['phrases'][0]['mc'];
								# 		l = [i['tt'] for i in response.json()['phrases'][0]['tks'] if i['tg']==2]
								# 		if(num3>10*num2 and num3>num1 and len(l)!=0):
								# 			k=l[0]
										# print(num3)
							ans[k]=10*num2
							num2=0;
							x+=1
				out = [x[0] for x in sorted(ans.items(), key = lambda x : -1*x[1])[:3]]
				corrections[tagged[0][0]] = out;
				
		j=j+1

print(str(corrections))
