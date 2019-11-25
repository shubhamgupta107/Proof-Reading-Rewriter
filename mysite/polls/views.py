from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
#from django.template import loader
#from django.views import generic
import nltk
from .models import Sentence
from .forms import HomeForm
from .spellcheck import giveSuggestions
from .grammarcheck import checkgrammar
from .synonym import getSynonyms
from .punctuation import correct_sentence
import string 
num = []
firstgram = []
gramsuggs = []
correctedgrammar = []
firstsym = []
symsuggs = {}
symdic = {}
relist = [",",".","!","?",">","<","/","(",")","[","]","{","}","@","#","$","%","&","*","-","+"]
endlist = [".","?","!"]
spellignore = []
gramignore = []
def removenonalpha(idx,l):
    ansid = idx
    if len(l)>0:
        for i in range(idx+1):
            #print(i)
            #print(len(l))
            if l[i] in relist:
                ansid -= 1
    return(ansid)
#savesen = True
def home(request):
    global symdic
    sentences = Sentence.objects.all()
    #print(len(list(sentences)))
    if request.method == "POST":
        spellignore.clear()
        gramignore.clear()
        sentences.delete()
        homeform =HomeForm(request.POST)
        if homeform.is_valid():
            homeform.save()    
    homeform = HomeForm()
    if num==[]:
        sentenceslist = []
        num.append(1)
    else:
        sentenceslist = list(Sentence.objects.all())
    sen = ""
    if sentenceslist:
        sen = str(sentenceslist[0])
    if request.method == "GET":
        corrs = list(request.GET.items())
        splitsens = sen.split(" ")
        for sugg in corrs:
            corr = sugg[0].split(",")
            if (corr[0]=="spell"):
                for i in range(len(splitsens)):
                    senval = False
                    for elems in nltk.word_tokenize(splitsens[i]):
                        if elems == corr[1]:
                            splitsens[i] = splitsens[i].replace(corr[1],corr[2])
                            senval = True
                            break
                    if senval:
                        break
            elif (corr[0]=="spellignore"):
                spellignore.append(corr[1])
            elif (corr[0]=="gram" and correctedgrammar):
                #print(correctedgrammar)
                corridx = int(corr[1])
                temptoken = nltk.word_tokenize(sen)
                corrid = removenonalpha(corridx,temptoken)
                #print(corrid)
                splitsens[corrid] = splitsens[corrid].replace(corr[2],corr[3])
                #gramsuggs.remove((temptoken[corridx],corridx,correctedgrammar[corridx]))
                correctedgrammar[corridx] = []
                #print(corr[2])
            elif (corr[0]=="gramignore"):
                gramignore.append(corr[1])
            elif (corr[0]=="sym" and symdic):
                for i in range(len(splitsens)):
                    senval = False
                    for elems in nltk.word_tokenize(splitsens[i]):
                        if elems == corr[1]:
                            splitsens[i] = splitsens[i].replace(corr[1],corr[2])
                            print(corr[1])
                            symdic[corr[1]] = []
                            symdic[corr[2]] = []
                            senval = True
                            break
                    if senval:
                        break
        sen = " ".join(splitsens)
        sentences.delete()
        newsentence = Sentence(sen_text=sen)
        newsentence.save()
    newsen = " ".join(sen.split(" "))
    #print(newsen)
    multsentences = [x.strip() for x in nltk.sent_tokenize(newsen)]
    #how are you bc. what is goin on.
    laststop = -1
    for chid in range(len(newsen)-1,-1,-1):
        if newsen[chid] in endlist:
            laststop = chid
            break
    if (laststop!=-1 and newsen[-1] not in endlist):
        multsentences = multsentences[:len(multsentences)-1]
    print(multsentences)
    splitwords = []
    suggs = {}
    if (laststop!=-1):
        for modsen in multsentences:
            splits = modsen.split(" ")
            for word in splits:
                ans = 0
                for ch in nltk.word_tokenize(word):
                    if (ch not in relist):
                        word = ch
                        ans = giveSuggestions(word)
                        break
                if ans and word not in spellignore:
                    suggs[word] = ans
                    splitwords.append((False,False,True,word))
                else:
                    splitwords.append((False,False,False,word))
            splitwords[-1] = (splitwords[-1][0],splitwords[-1][1],splitwords[-1][2],splitwords[-1][3]+".")
        if suggs:
            firstgram.clear()
            gramsuggs.clear()
            correctedgrammar.clear()
    if not(suggs) and laststop!=-1:
        #print("Here")
        #if (savesen):
            #savesen=False
        newsen = correct_sentence(newsen)
           # sentences.delete()
           # newsentence = Sentence(sen_text=newsen)
           # newsentence.save()
        splitwords = []
        gramsuggs.clear()
        senttokenized = nltk.word_tokenize(newsen[:laststop+1])
        if not(firstgram):
            firstgram.append(1)
            cgrammar = checkgrammar(newsen[:laststop+1])
            correctedgrammar.extend(cgrammar)
            print(correctedgrammar)
        nsplitsen = newsen[:laststop+1].split(" ")
        #print(newsen[:laststop])
        #print(senttokenized)
        #print(correctedgrammar)
        for idx in range(len(correctedgrammar)):
            if not(correctedgrammar[idx]==[]) and idx not in gramignore:
                splitwords.append((False,True,True,nsplitsen[removenonalpha(idx,senttokenized)]))
                gramsuggs.append((senttokenized[idx],idx,correctedgrammar[idx]))
            elif senttokenized[idx] not in relist:
                splitwords.append((False,True,False,nsplitsen[removenonalpha(idx,senttokenized)]))
                #print(splitwords)
        if gramsuggs:
            firstsym.clear()
            symsuggs.clear()
    if not(gramsuggs) and not(suggs) and laststop!=-1:
        splitwords = []
        symsuggs.clear()
        senttokenized = nltk.word_tokenize(newsen[:laststop+1])
        if not(firstsym):
            #print("Here")
            symdic = getSynonyms(newsen[:laststop+1])
            print(symdic.keys())
            for sword in senttokenized:
                if sword not in relist and sword not in symdic.keys():
                    symdic[sword] = []
            firstsym.append(1)
        nsplitsen = newsen[:laststop+1].split(" ")
        for sidx in range(len(senttokenized)):
            if senttokenized[sidx] not in relist:
                if symdic[senttokenized[sidx]]:
                    splitwords.append((True,False,True,nsplitsen[removenonalpha(sidx,senttokenized)]))
                    symsuggs[senttokenized[sidx]] = symdic[senttokenized[sidx]]
                else:
                    splitwords.append((True,False,False,nsplitsen[removenonalpha(sidx,senttokenized)]))

    for nwords in newsen[laststop+1:].split(" "):
        splitwords.append((False,True,False,nwords))
    Items = suggs.items()
    context = {'form':homeform, 'sen':sen, 'splitsen':splitwords, 'suggestions':Items, 'gramsuggs':gramsuggs, 'symsuggestions':symsuggs.items()}
    return render(request,'polls/home.html',context)



