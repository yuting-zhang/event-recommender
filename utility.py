import metapy

# Concatenate a list of words to a string
def join_words(words):
    doc = ""
    for word in words:
        doc += word
        doc += " "
    doc = doc[:-1]
    return doc

# Remove <s> and <\s> from list
def remove_tags(tokens):
    if "<s>" in tokens:
        tokens.remove("<s>")
    if "</s>" in tokens:
        tokens.remove("</s>")
    return tokens

def remove_stopwords(words):
    doc = metapy.index.Document()
    doc.content(join_words(words))
    tok = metapy.analyzers.ICUTokenizer()
    tok = metapy.analyzers.ListFilter(tok, "lemur-stopwords.txt", metapy.analyzers.ListFilter.Type.Reject)
    tok.set_content(doc.content())
    tokens = [token for token in tok]
    return remove_tags(tokens)

def stem(words):
    doc = metapy.index.Document()
    doc.content(join_words(words))
    tok = metapy.analyzers.ICUTokenizer()
    tok = metapy.analyzers.Porter2Filter(tok)
    tok.set_content(doc.content())
    tokens = [token for token in tok]
    return remove_tags(tokens)
