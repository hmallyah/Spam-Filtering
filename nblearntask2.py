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
spam_emails_path = []
ham_emails_path = []

data_directory = sys.argv[1]
for root, directories, files in os.walk(data_directory):
    for directory in directories:
        if directory == "spam" or directory == "ham":
            txtpath = os.path.join(root, directory)
            for textfile in glob.glob(os.path.join(txtpath, '*.txt')):
                if directory == "spam":
                    spam_emails_path.append(textfile)
                elif directory == "ham":
                    ham_emails_path.append(textfile)

number_of_emails = int((len(ham_emails_path)+len(spam_emails_path))/10)

for i in range(0, int(number_of_emails/2)):
    text1 = open(spam_emails_path[i], "r", encoding="latin1").read()
    text1 = text1.lower()
    for word1 in text1.split():
        spamlist.append(word1)
    text2 = open(ham_emails_path[i], "r", encoding="latin1").read()
    text2 = text2.lower()
    for word2 in text2.split():
        hamlist.append(word2)


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
    file_object = open("nbmodeltask2.txt", "w")
    file_object.write(str([0.5, 0.5]) + "\n")
    file_object.write(str(pdict))
    file_object.close()

create_nbmodel(model)