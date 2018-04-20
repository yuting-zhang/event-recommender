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

with open('cs-train.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        dictionary |= set(row)

dictionary = utility.remove_stopwords(dictionary)
dictionary = utility.stem(dictionary)

for word in dictionary:
    fo.write("%s\n" % word)
