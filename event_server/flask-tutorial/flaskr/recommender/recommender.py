import csv
from flaskr.recommender.bm25 import BM25
from operator import itemgetter

UNK = "__UNKNOWN_WORD_TOKEN__"

pathname = "flaskr/recommender/"

class Recommender:

    def __init__(self, train_ratio = 0.8):
        self.init_docs_data(train_ratio)
        self.init_dict_data()
        self.init_user_data()
        self.bm25 = BM25(self.train_docs_stemmed)

    def init_docs_data(self, train_ratio):
        # load data
        cs_docs = self.load_docs_data(pathname+"cs-train.csv")
        cs_docs_stemmed = self.load_docs_data(pathname+"stemmed-cs-train.csv")

        if len(cs_docs) != len(cs_docs_stemmed):
            raise Exception("cs-train.csv and stemmed-cs-train.csv have " +
                            "different length")

        las_docs = self.load_docs_data(pathname+"las-train.csv")
        las_docs_stemmed = self.load_docs_data(pathname+"stemmed-las-train.csv")

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
        with open(pathname+"stemmed_dictionary.txt", "r") as dict_file:
            for word in dict_file:
                self.dictionary.add(word.strip())

    '''           
    user-list.csv stores a list of usernames
    user-data.csv stores user vectors
    '''
    def init_user_data(self):
        self.user_data = {}
        try:
            with open(pathname+"user-data.csv", "r") as data_csv,\
                 open(pathname+"user-list.csv", "r") as user_csv:
                data_reader = csv.DictReader(data_csv)
                for username, data in zip(user_csv, data_reader):
                    for key in data:
                        data[key] = float(data[key])
                    self.user_data[username.strip()] = data
        except IOError:
            print("Cannot find user data. Assume empty database.")

    '''
    add a new user with username
    '''
    def add_new_user(self, username):
        if username in self.user_data:
            print("Username already been used")
            return
        vector = {}
        for word in self.dictionary:
            vector[word] = 0.0
        vector[UNK] = 0.0
        self.user_data[username] = vector

    '''
    CALL THIS BEFORE EXIT
    save current user data to disk
    '''
    def save_user_data(self):
        fieldnames = [UNK] + list(self.dictionary)
        with open(pathname+"user-data.csv", "w") as data_csv,\
             open(pathname+"user-list.csv", "w") as user_csv:
            data_writer = csv.DictWriter(data_csv, fieldnames=fieldnames)
            data_writer.writeheader()

            for username in self.user_data:
                data_writer.writerow(self.user_data[username])
                user_csv.write(username + "\n")
                
    '''
    get a list of recommended events for the given user
    '''
    def get_events(self, username):
        if not username in self.user_data:
            print("No such user")
            return

        scores = []
        for idx in range(len(self.test_docs_stemmed)):
            doc = self.test_docs_stemmed[idx]
            # currently treat all fields as the same
            doc_dict = {}
            for field in doc:
                for word in field.split():
                    if not word in self.dictionary:
                        word = UNK
                    if word in doc_dict:
                        doc_dict[word] += 1.0
                    else:
                        doc_dict[word] = 1.0

            score = self.bm25.get_score(doc_dict, self.user_data[username])
            scores.append([idx, score])

        scores = sorted(scores, key=itemgetter(1), reverse=True)
        print(scores[:5])

        indices = [cell[0] for cell in scores[:5]]
        events = [self.test_docs[index] for index in indices]
        for event in events:
            print(event)
        return events


if __name__ == "__main__":
    rec = Recommender()
    rec.add_new_user("yuting")
    rec.user_data["yuting"]["music"] = 5.0
    rec.user_data["yuting"]["ICPC"] = 10.0
    rec.user_data["yuting"]["secur"] = 5.0
    rec.get_events("yuting")
    rec.save_user_data()
