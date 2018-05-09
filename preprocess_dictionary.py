import utility
import csv

fi = open("dictionary.txt", "r")
fo = open("stemmed_dictionary.txt", "w")

words = fi.readlines()
# Removing '\n'
for i in range(len(words)):
    if words[i][-1] == '\n':
        words[i] = words[i][:-1]
dictionary = set(words)

data_file = ['cs-train.csv', 'las-train.csv']
for fdata in data_file:
    with open(fdata, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            dictionary |= set(row)

dictionary = map(lambda x: x.lower(), dictionary)
dictionary = utility.remove_stopwords(dictionary)
dictionary = utility.stem(dictionary)
dictionary = set(dictionary)

sorted_dictionary = sorted(dictionary)
for word in sorted_dictionary:
    fo.write("%s\n" % word)
