import os
import sys
import glob
import collections
from math import log10

data_directory = ""
spamlist = []
hamlist = []
vocabulary = []
spam_word_count = {}
ham_word_count = {}
word_given_spam = {}
word_given_ham = {}
probability_of_spam = 0
probability_of_ham = 0

data_directory = sys.argv[1]
for root, directories, files in os.walk(data_directory):
    for directory in directories:
        if directory == "spam" or directory == "ham":
            txtpath = os.path.join(root, directory)
            for textfile in glob.glob(os.path.join(txtpath, '*.txt')):
                text = open(textfile, "r", encoding="latin1").read()
                if directory == "spam":
                    probability_of_spam += 1
                    for word in text.split():
                        word = word.lower()
                        spamlist.append(word)
                elif directory == "ham":
                    probability_of_ham += 1
                    for word in text.split():
                        word = word.lower()
                        hamlist.append(word)

total_mails = probability_of_spam + probability_of_ham
probability_of_spam = probability_of_spam/total_mails
probability_of_ham = probability_of_ham/total_mails

def union(a = [], b = []):
    return list(set(a)|set(b))

vocabulary = union(spamlist, hamlist)

def word_count(lst = []):
    return collections.Counter(lst)

spam_word_count = word_count(spamlist)
ham_word_count = word_count(hamlist)

def calculate_probability(total_words, vocabulary = [], count_dict = {}):
    pdict = {}
    denominator = log10(total_words + len(vocabulary))
    for word in vocabulary:
        if word in count_dict:
            pdict[word] = log10(count_dict[word]+1) - denominator
        else:
            pdict[word] = log10(1) - denominator
    return pdict

word_given_spam = calculate_probability(len(spamlist), vocabulary, spam_word_count)
word_given_ham = calculate_probability(len(hamlist),vocabulary, ham_word_count)

model = {}
for word in vocabulary:
    model[word] = [word_given_spam[word], word_given_ham[word]]

def create_nbmodel(pdict = {}):
    file_object = open("nbmodel.txt", "w")
    file_object.write(str([probability_of_spam, probability_of_ham]) + "\n")
    file_object.write(str(pdict))
    file_object.close()

create_nbmodel(model)