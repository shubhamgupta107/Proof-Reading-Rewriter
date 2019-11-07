import re
from collections import Counter
import time
# def words(text): return re.findall(r'\w+', text.lower())
NUM_SUGGESTIONS = 4
WORDS = {}
f = open("polls/dictionary.txt", "r")
dictionary = f.readlines()
for line in dictionary:
    word,freq = line.split()
    WORDS[word] = int(freq)
# WORDS = Counter(words(open("data.txt").read()))

def P(word, N=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / N

def candidates(word): 
    "Generate possible spelling corrections for word."
    l = []
    temp1 = list(sorted(known([word]),key=P,reverse=True))
    if(temp1):
        return temp1
    temp2 = list(sorted(known(edits1(word)),key=P,reverse=True))
    temp3 = list(sorted(known(edits2(word)),key=P,reverse=True))
    # return (known(edits1(word)) or known(edits2(word)) or [word])
    for item in (temp1+temp2+temp3):
        if(item not in l):
            l.append(item)
    number = min(NUM_SUGGESTIONS,len(l))
    return l[:number]

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
def giveSuggestions(word):
    #a=input()
    #start = time.time()
    #print(candidates(a))
    #end = time.time()
    #print(end-start)
    word = word.lower()
    if word in WORDS.keys() or word == "":
        return []
    else:
        return candidates(word)