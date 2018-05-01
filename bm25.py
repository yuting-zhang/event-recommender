import csv
import math

class BM25:

    def get_score(self, doc, query_vec):
        res = 0
        doc_len = 0
        for word in doc:
            doc_len += doc[word]
        for word in query_vec:
            if word in doc and word in self.docs_containing_word:
                res += query_vec[word]*((self.k+1)*doc[word])*\
                math.log((self.num_docs+1)/self.docs_containing_word[word])/\
                (doc[word]+self.k*(1-self.b+self.b*doc_len/self.avg_doc_len))
        return res

    def __init__(self, docs):
        self.k = 1.5
        self.b = 0.75
        self.num_docs = len(docs)
        self.docs_containing_word = {}
        self.avg_doc_len = 0
        for doc in docs:
            for field in doc:
                for word in field.split():
                    self.avg_doc_len += 1
                    # compute n(q_i)
                    if word in self.docs_containing_word:
                        self.docs_containing_word[word] += 1
                    else:
                        self.docs_containing_word[word] = 1
        self.avg_doc_len /= self.num_docs


"""
if __name__ == "__main__":
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
    bm25 = BM25()
    """
