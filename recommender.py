import csv
from bm25 import BM25

UNK = "__UNKNOWN_WORD_TOKEN__"

class Recommender:

    def __init__(self, train_ratio = 0.8):
        self.init_docs_data(train_ratio)
        self.init_dict_data()
        self.init_user_data()
        self.bm25 = BM25(self.train_docs)

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
                self.dictionary.add(word.strip())

    '''           
    user-list.csv stores a list of usernames
    user-data.csv stores user vectors
    '''
    def init_user_data(self):
        self.user_data = {}
        try:
            with open("user-data.csv", "r") as data_csv,\
                 open("user-list.csv", "r") as user_csv:
                data_reader = csv.DictReader(data_csv)
                for username, data in zip(user_csv, data_reader):
                    self.user_data[username.strip()] = data
        except IOError:
            print("Cannot find user data. Assume empty database.")

    '''
    add a new user with username
    '''
    def add_new_user(self, username):
        vector = {}
        for word in self.dictionary:
            vector[word] = 0
        vector[UNK] = 0
        self.user_data[username] = vector

    '''
    CALL THIS BEFORE EXIT
    save current user data to disk
    '''
    def save_user_data(self):
        fieldnames = [UNK] + list(self.dictionary)
        with open("user-data.csv", "w") as data_csv,\
             open("user-list.csv", "w") as user_csv:
            data_writer = csv.DictWriter(data_csv, fieldnames=fieldnames)
            data_writer.writeheader()

            for username in self.user_data:
                data_writer.writerow(self.user_data[username])
                user_csv.write(username + "\n")
                
    '''
    get a list of recommended events for the given user
    '''
    def get_events(username):
        scores = []
        for idx in len(self.test_docs_stemmed):
            doc = self.test_docs_stemmed[idx]
            # currently treat all fields as the same
            query = {}
            for field in doc:
                for word in field.split():
                    if not word in self.dictionary:
                        word = UNK
                    if word in query:
                        query[word] += 1
                    else:
                        query[word] = 0


if __name__ == "__main__":
    rec = Recommender()
    rec.save_user_data()
