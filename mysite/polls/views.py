from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render,redirect
#from django.template import loader
#from django.views import generic
from .models import Sentence
from .forms import HomeForm
from .spellcheck import giveSuggestions
num = []

def home(request):
    sentences = Sentence.objects.all()
    #print(len(list(sentences)))
    if request.method == "POST":
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
        for sugg in corrs:
            corr = sugg[0].split(",")
            sen = sen.replace(corr[0],corr[1])
        sentences.delete()
        newsentence = Sentence(sen_text=sen)
        newsentence.save()
    splits = sen.split(" ")
    suggs = {}
    for word in splits:
        ans = giveSuggestions(word)
        if ans:
            suggs[word] = ans
    Items = suggs.items()
    context = {'form':homeform, 'sen':sen, 'suggestions':Items}
    return render(request,'polls/home.html',context)



