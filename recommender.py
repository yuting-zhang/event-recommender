import csv
import bm25

UNK = "__UNKNOWN_WORD_TOKEN__"

class Recommender:

    def __init__(self, train_ratio = 0.8):
        self.init_docs_data(train_ratio)
        self.init_dict_data()
        self.init_user_data()

    def init_docs_data(self, train_ratio):
        # load data
        cs_docs = self.load_docs_data("cs-train.csv")
        cs_docs_stemmed = self.load_docs_data("stemmed-cs-train.csv")

        if len(cs_docs) != len(cs_docs_stemmed):
            raise Exception("cs-train.csv and stemmed-cs-train.csv have " +
                            "different length")

        las_docs = self.load_docs_data("las-train.csv")
        las_docs_stemmed = self.load_docs_data("stemmed-las-train.csv")

        if len(las_docs) != len(las_docs_stemmed):
            raise Exception("las-train.csv and stemmed-las-train.csv have " +
                            "different length")

        # split data into train, test based on train_ratio
        cs_index = int(len(cs_docs) * train_ratio)
        las_index = int(len(las_docs) * train_ratio)

        self.train_docs = cs_docs[:cs_index] + las_docs[:las_index]
        self.train_docs_stemmed = cs_docs_stemmed[:cs_index] +\
                                  las_docs_stemmed[:las_index]
        self.test_docs = cs_docs[cs_index:] + las_docs[las_index:]
        self.test_docs_stemmed = cs_docs_stemmed[cs_index:] +\
                                 las_docs_stemmed[las_index:]

    def load_docs_data(self, path):
        docs = []
        with open(path, "r") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=",")
            for row in csv_reader:
                docs.append(row)
        return docs

    def init_dict_data(self):
        # words not in dictionary will be treated as unknown
        self.dictionary = set()
        with open("stemmed_dictionary.txt", "r") as dict_file:
            for word in dict_file:
                self.dictionary.add(word)
                
    def init_user_data(self):
        self.user_data = {}
        with open("user-data.csv", "r") as data_csv,\
             open("user-list.csv", "r") as user_csv:
            data_reader = csv.DictReader(data_csv)
            for username, data in zip(user_csv, data_reader):
                self.user_data[username.strip()] = data

if __name__ == "__main__":
    rec = Recommender()
