# Proof-Reading-Rewriter
This Project aims to develop a Django server backed with python to Proof-Read the given piece of text and suggests spelling corrections. 

### For spelling correction
We have used the idea of Levenshtein distance to measure the similarity between two strings. More details can be found [here](https://norvig.com/spell-correct.html). 

### For grammer correction 
We have made use of [api](https://phrasefinder.io/) to find the words that are suitable with respect to the contextual meaning of the sentence and then giving them in form of suggestions. 

### For Punctuation correction
We have used rules of English Language to some extent. Most punctuation can be correctly placed with this.

### For synonym suggestions
We have used the NLTK Library to find the suggestion and then with the help of context we are finding the one which suits there best.

Overall the conversion rate was quite good and it was able to convert most of the sentences correct.
### To RUN Follow the steps
- Install the needed Libraries like NLTK.
```
python3 mysite/manage.py runserver
```
- Go to this [link](http://127.0.0.1:8000/) and happy editing/
