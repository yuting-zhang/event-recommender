import csv

class BM25:
    num_docs = 0
    docs_containing_word = {}
    k1 = 1.5
    b = 0.75

    def get_idf(self, query_word):
        return (num_docs-docs_containing_word[query_word]+0.5)/(docs_containing_word[query_word]+0.5)

    def get_score_single(self, f, query_word, doc_len, avg_doc_len):
        idf = get_idf(query_word)
        return idf*(f*(k1+1))/(f+k1*(1-b+b*doc_len/avg_doc_len))

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
            # each doc has a few fields, like title, time, location, description
            for fields in doc:
                for word in fields.split():
                    # compute n(q_i)
                    if word in docs_containing_word:
                        docs_containing_word[word] += 1
                    else:
                        docs_containing_word[word] = 1
                

if __name__ == "__main__":
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
    bm25 = BM25()
