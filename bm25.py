import csv
import math

class BM25:
    num_docs = 0
    docs_containing_word = {}
    avg_doc_len = 0
    k = 1.5
    b = 0.75

    def get_score(self, doc, query_vec):
        res = 0
        doc_len = 0
        for word in doc:
            doc_len += doc[word]
        for word in query_vec:
            if word in doc:
                res += query_vec[word]*((k+1)*doc[word])*math.log((num_docs+1)/docs_containing_word[word])/(doc[word]+k*(1-b+b*doc_len/avg_doc_len))
        return res

    def __init__(self, docs):
        num_docs = len(docs)
        docs_containing_word = {}
        avg_doc_len = 0
        for doc in docs:
            for word in doc:
                avg_doc_len += doc[word]
                # compute n(q_i)
                if word in docs_containing_word:
                    docs_containing_word[word] += 1
                else:
                    docs_containing_word[word] = 1
        avg_doc_len /= num_docs


"""
if __name__ == "__main__":
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
    bm25 = BM25()
    """
