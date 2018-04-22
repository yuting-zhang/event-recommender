import csv

class BM25:
    num_docs = 0
    docs_containing_word = {}
    k1 = 1.5
    b = 0.75

    def get_idf(self, query_word):
        return (num_docs-docs_containing_word[query_word]+0.5)/(docs_containing_word[query_word]+0.5)

    def get_score(self, doc, query_vec):
        idf_vec = idf(query_vec)

    def get_score(self, idf_vec, f_vec, doc_len, avg_doc_len):
        return idf_vec*(f_vec*(k1+1))/(f_vec + k1*(1-b+b*doc_len/avg_doc_len))

    def f(self, query_word, doc):
        return doc[query_word]

    def __init__(self, docs):
        num_docs = len(docs)
        docs_containing_word = {}
        for doc in docs:
            for word in doc:
                # compute n(q_i)
                if word in docs_containing_word:
                    docs_containing_word[word] += 1
                else:
                    docs_containing_word[word] = 1
                

if __name__ == "__main__":
    bm25 = BM25()
