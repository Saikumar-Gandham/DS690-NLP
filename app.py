from flask import Flask, render_template, url_for, request
from pprint import pprint
import simplejson as json
import sys 
from nltk.corpus import brown
from nltk.corpus import reuters
import nltk
from nltk.corpus import PlaintextCorpusReader
from textblob import TextBlob
from model import gf
app = Flask(__name__)

## Lets Mention the required functions here :

def get_trigram_freq(tokens):
	tgs = list(nltk.trigrams(tokens))
	a,b,c = list(zip(*tgs))
	bgs = list(zip(a,b))
	return nltk.ConditionalFreqDist(list(zip(bgs, c)))

def get_bigram_freq(tokens):
	bgs = list(nltk.bigrams(tokens))
	return nltk.ConditionalFreqDist(bgs)

def appendwithcheck(preds, to_append):
    for pred in preds:
        if pred[0] == to_append[0]:
            return
    preds.append(to_append)


def incomplete_pred(words, n):
    all_succeeding = bgs_freq[(words[n-2])].most_common()
    preds = []
    number = 0
    
    # Check words that start with the same prefix
    for pred in all_succeeding:
        if pred[0].startswith(words[n-1]):
            appendwithcheck(preds, pred)
            number += 1  # Ensure this line is indented correctly
        if number == 3:  # This line should align with `if`
            return preds  # Proper indentation

    # If fewer than 3 predictions were found
    if len(preds) < 3:
        med = []
        for pred in all_succeeding:
            med.append((pred[0], nltk.edit_distance(pred[0], words[n-1], transpositions=True)))

        # Sort by edit distance
        med.sort(key=lambda x: x[1])

        index = 0
        # Continue until there are at least 3 predictions
        while len(preds) < 3:
            print (index, len(med))
            if index < len(med):
                if med[index][1] > 0:
                    appendwithcheck(preds, med[index])
                index += 1
            if index>=len(preds):  # If we've run out of elements in `med`
                return preds 
# If we've run out of elements in `med`
                  # Avoid potential infinite loop
  # Ensure this line is correctly aligned with the initial `if`



new_corpus = PlaintextCorpusReader('./','.*')
tokens = brown.words() + new_corpus.words('combined_cleaned.txt')

bgs_freq = get_bigram_freq(tokens)
tgs_freq = get_trigram_freq(tokens)


###########################################
@app.route('/')
def index():
	return render_template("index.html")

@app.route('/index1')
def index1():
     return render_template("index1.html")

@app.route('/predict', methods=['GET','POST'])
def predict_page():
    if request.method == "POST":
        enter = request.form['text'].strip()  # Get text input and trim whitespace
        string = enter
        words = string.split()  # Split input into words
        n = len(words)  # Get word count
        work = "pred"
        last_word = words[-1]  # Get the last word in the input
        print(last_word)
        #Check if the last word has any bigram frequency data
        if last_word in bgs_freq:  # Step 1: Ensure the last word is a recognized bigram
            if len(bgs_freq[last_word].most_common()) == 0:
                # No common bigrams for this word, treat it as incomplete
                inc = incomplete_pred(words, n)  # Step 9: Incomplete prediction
                print("inc ->", inc)
                  # Exit after printing incomplete predictions
            else:
                # Recognized word, follow normal prediction path
                work = "pred"
        else:
            # If it's not in the bigram frequency distribution, treat it as incomplete
            inc = incomplete_pred(words, n)
            print("inc ->", inc)
              # Exit after printing incomplete predictions
        
        # Normal prediction mode for complete words
        if work == "pred":  # Prediction mode
            if n == 1:
                bgs = bgs_freq[(string)].most_common(5)  # Bigram-based prediction
                b = [i[0] for i in bgs]
                print("bgs ->", bgs)
            elif n > 1:
                tgs = tgs_freq[(words[n-2], words[n-1])].most_common(5)  # Trigram-based prediction
                pred = [i[0] for i in tgs]
                print(pred)
        if n == 1:
            p = b
        else:
            p = pred
	# return pred 
    return render_template("index.html", s= enter, t = p)
@app.route('/predict1', methods=['GET','POST'])
def predict_page1():
        if request.method == "POST":
            enter = request.form['text'].strip()  # Get text input and trim whitespace
        string = enter
        blob = TextBlob(string)
        corrected_sentence = blob.correct()
        corrected_sentence = str(corrected_sentence)
        corrections = gf.correct(corrected_sentence)
	# return pred 
        return render_template("index1.html", s= enter, t = corrections)

if __name__ == '__main__':
	app.run(debug=True)