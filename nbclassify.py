import os
import sys
import glob
from math import log10

emails = {}
classification = {}
spam_class = []
ham_class = []

data_directory = sys.argv[1]
for root, directories, files in os.walk(data_directory):
    for directory in directories:
        txtpath = os.path.join(root, directory)
        for textfile in glob.glob(os.path.join(txtpath, '*.txt')):
            text = open(textfile, "r", encoding="latin1").read()
            emails[textfile] = text.lower()

file_object = open("nbmodel.txt", "r").readlines()
class_probability = eval(file_object[0])
word_given_class_probability = eval(file_object[1])

def prediction(path, msg):
    prb_msg_spam = 0.0
    prb_msg_ham = 0.0
    for word in msg.split():
        if word in word_given_class_probability:
            prb_msg_spam += word_given_class_probability[word][0]
            prb_msg_ham += word_given_class_probability[word][1]
    probability_spam_given_msg = (class_probability[0] + prb_msg_spam) - ((prb_msg_spam + class_probability[0]) + (prb_msg_ham + class_probability[1]))
    probability_ham_given_msg = (class_probability[1] + prb_msg_ham) - ((prb_msg_spam + class_probability[0]) + (prb_msg_ham + class_probability[1]))
    if probability_ham_given_msg > probability_spam_given_msg:
        classification[path] = "ham"
    else:
        classification[path] = "spam"

for path in emails:
    prediction(path, emails[path])

file_object = open("nboutput.txt", "w")
for email in classification:
    if classification[email] == "spam":
        file_object.write("SPAM " + str(email) + "\n")
    if classification[email] == "ham":
        file_object.write("HAM " + str(email) + "\n")
file_object.close()

'''
for root, directories, files in os.walk(data_directory):
    for directory in directories:
        if directory == "spam" or directory == "ham":
            txtpath = os.path.join(root, directory)
            for textfile in glob.glob(os.path.join(txtpath, '*.txt')):
                if directory == "spam":
                    spam_class.append(textfile)
                if directory == "ham":
                    ham_class.append(textfile)

def accuracy(spam_class = [], ham_class = [], classification = {}):
    correctly_classified_count = 0
    for email in classification:
        if classification[email] == "spam" and email in spam_class:
            correctly_classified_count += 1
        if classification[email] == "ham" and email in ham_class:
            correctly_classified_count += 1
    accuracy = correctly_classified_count/len(emails)
    print("Accuracy: " + str(accuracy))

accuracy(spam_class, ham_class, classification)

def precision_recall_fscore(class_name, kclass = [], classification = {}):
    classified_count =  0
    correctly_classified_count = 0
    for textfile in classification:
        if classification[textfile] == class_name:
            classified_count += 1
            if textfile in kclass:
                correctly_classified_count += 1
    class_precision = correctly_classified_count/classified_count
    print("Precision("+class_name+")" +": "+ str(class_precision))
    class_recall = correctly_classified_count/len(kclass)
    print("Recall("+class_name+")" +": "+ str(class_recall))
    fscore = (2*class_precision*class_recall)/(class_precision+class_recall)
    print("F_Score("+class_name+")" +": "+ str(fscore))

precision_recall_fscore("spam", spam_class, classification)
precision_recall_fscore("ham", ham_class, classification)
'''