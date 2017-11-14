# use natural language toolkit
import nltk
import os
from nltk.stem.lancaster import LancasterStemmer

# word stemmer
stemmer = LancasterStemmer()
# 3 classes of training data
training_data = []

file_dir = os.path.dirname(__file__)
path = 'data/intent_classification'
abs_file_path = os.path.join(file_dir, path)
f = open(abs_file_path, "r")
num  = 0
filelines = f.read().splitlines()

sentence = ''
sentence_class = ''
for index, line in enumerate(filelines):
    data = ()
    line = line.strip()
    if not line:
        continue
    if line.startswith("#"):
        continue
    if num == 0:
        sentence = line
    elif num == 1:
        sentence_class = line
    elif num == 2:
        training_data.append({"class": sentence_class, "sentence": sentence})
        num = -1
    num += 1

# capture unique stemmed words in the training corpus
corpus_words = {}
class_words = {}
# turn a list into a set (of unique items) and then a list again (this removes duplicates)
classes = list(set([a['class'] for a in training_data]))
for c in classes:
    # prepare a list of words within each class
    class_words[c] = []

# loop through each sentence in our training data
for data in training_data:
    # tokenize each sentence into words
    for word in nltk.word_tokenize(data['sentence']):
        # ignore a some things
        if word not in ["?", "'s"]:
            # stem and lowercase each word
            stemmed_word = stemmer.stem(word.lower())
            # have we not seen this word already?
            if stemmed_word not in corpus_words:
                corpus_words[stemmed_word] = 1
            else:
                corpus_words[stemmed_word] += 1

            # add the word to our words in class list
            class_words[data['class']].extend([stemmed_word])

# we now have each stemmed word and the number of occurances of the word in our training corpus (the word's commonality)
print ("Corpus words and counts: %s \n" % corpus_words)
# also we have all words in each class
print ("Class words: %s" % class_words)


# calculate a score for a given class taking into account word commonality
def calculate_class_score(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with relative weight
            score += (1 / corpus_words[stemmer.stem(word.lower())])

            if show_details:
                print ("   match: %s (%s)" % (stemmer.stem(word.lower()), 1 / corpus_words[stemmer.stem(word.lower())]))
    return score


# sentence = "good day for us to have lunch?"
#
#
# # now we can find the class with the highest score
# for c in class_words.keys():
#     print ("Class: %s  Score: %s \n" % (c, calculate_class_score(sentence, c)))

# return the class with highest score for sentence
def classify(sentence):
    high_class = None
    high_score = 0
    # loop through our classes
    for c in class_words.keys():
        # calculate score of sentence for each class
        score = calculate_class_score(sentence, c, show_details=False)
        # keep track of highest score
        if score > high_score:
            high_class = c
            high_score = score

    return high_class, high_score
