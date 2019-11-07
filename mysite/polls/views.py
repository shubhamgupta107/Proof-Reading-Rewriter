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
        sentences = []
        num.append(1)
    else:
        sentences = list(Sentence.objects.all())
    sen = ""
    if sentences:
        sen = sentences[0]
    splits = str(sen).split(" ")
    suggs = {}
    for word in splits:
        ans = giveSuggestions(word)
        if ans:
            suggs[word] = ans
    Items = suggs.items()
    context = {'form':homeform, 'sen':sen, 'suggestions':Items}
    return render(request,'polls/home.html',context)



