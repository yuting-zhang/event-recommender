import metapy

def remove_stopwords(words):
    doc = metapy.index.Document()
    doc.content(' '.join(words))
    tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
    tok = metapy.analyzers.ListFilter(tok, "lemur-stopwords.txt", metapy.analyzers.ListFilter.Type.Reject)
    tok.set_content(doc.content())
    tokens = [token for token in tok]
    return tokens

def stem(words):
    doc = metapy.index.Document()
    doc.content(' '.join(words))
    tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
    tok = metapy.analyzers.Porter2Filter(tok)
    tok.set_content(doc.content())
    tokens = [token for token in tok]
    return tokens
