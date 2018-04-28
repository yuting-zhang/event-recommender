import utility
import csv

col = ['Date', 'Time', 'Location', 'Name', 'Description']
f = open('stemmed-las-train.csv','w')
w = csv.DictWriter(f, col, quoting=csv.QUOTE_ALL)
w.writeheader()

with open('las-train.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        d = {}
        for i in range(len(row)):
            s = [row[i]]
            s = utility.remove_stopwords(s)
            s = utility.stem(s)
            s = ' '.join(s)
            d[col[i]] = s
        w.writerow(d)
