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
from nltk.stem.wordnet import WordNetLemmatizer as wn

def correct_sentence(initial):
	s = '';
	initial = initial.lower()
	wordlist = nltk.word_tokenize(initial);
	j=0;
	ques_occur = False;
	another_ques_occur = False;
	x=0;
	ques = False;
	for word in wordlist:
		words = nltk.word_tokenize(word)
		tag = nltk.pos_tag(words)
		#print(tag)
		#print(word)
		if(word=='hey' or word=='hi' or word=='hello'):
			word = word + ','
		if(ques_occur==True and (word=='is' or word=='are' or word=='am') and j==x+1):
			ques=True;
			# print("it is a question")
		if(word=='what' or word=='where' or word=='which' or word == 'who' or word=='how' or word == 'whose' or word=='when'):
			# print("yes found a question")
			ques_occur=True
			x=j;
		if(j==0 and (word=='is' or word=='are' or word=='do' or word=='does' or word=='has' or word=='have' or word=='am')):
			ques=True;
		if(tag[0][0]=='NNP' or j==0 or word=='i' or tag[0][0]=='NNPS'):
			word = word.capitalize()
		if(ques==True):
			if(word=='.' or word=='?' or word=='!'):
				s = s+'? '
				j=-1;
				ques=False
				another_ques_occur=False
				ques_occur=False
		if(ques==False and j!=-1):
			if(word=='.' or word=='?' or word=='!'):
				if(word=='!'):
					s=s+'! '
					j=-1;
				else:
					s=s+'. '
					j=-1;
		if(j==0):
			s = s+word
		elif(not(word=='.'or word=='?' or word=='!')):
			s = s+' '+word
		j=j+1
	return s