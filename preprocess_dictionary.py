import utility

fi = open("dictionary.txt", "r")
fo = open("stemmed_dictionary.txt", "w")

words = fi.readlines()
# Removing '\n'
for i in range(len(words)):
    if words[-1] == '\n':
        words[i] = words[i][:-1]

words = utility.remove_stopwords(words)
words = utility.stem(words)

for word in words:
    fo.write("%s\n" % word)
