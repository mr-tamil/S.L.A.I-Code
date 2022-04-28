import datetime
import os
import sys
import time
from io import StringIO
from contextlib import contextmanager

import numpy
import numpy as np
import pandas

import database
import filehandler

from PIL import Image
import matplotlib.pyplot as plt


def name_time(nid):
    name = nid[1]
    timestamp = float(nid[2:])
    time_ = datetime.datetime.fromtimestamp(timestamp)
    return [nid, name, timestamp, time_]


def get_nids_details(table):
    db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
    db = database.Database(db_path)

    get_data = db.table_data(table)
    details = []
    for i in get_data:
        if "." in i[1]:
            details.append(name_time(i[1]))
    return details


def get_index_value(arr, index):
    data = []
    for i in index[0]:
        data.append(arr[i])
    data = np.array(data)
    return data


def open_research_module():
    db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
    db = database.Database(db_path)

    dir__ = os.path.join(os.path.dirname(os.path.realpath(__file__)), "researchFile.json")
    research_file = filehandler.FileHandler(dir__)

    neurons = get_nids_details("neurons")
    subverdet = db.table_data("subverdet")
    verbs = get_nids_details("verbs")

    memories = get_nids_details("memories")
    history_neurons = get_nids_details("history_neurons")

    neurons_data = np.array(neurons)
    subverdet_data = np.array(subverdet)
    verbs_count = len(db.table_data("verbs"))

    NL = np.array(history_neurons)
    NM = np.array(memories)
    NS = get_index_value(neurons_data, np.where(neurons_data == "S"))
    NV = get_index_value(neurons_data, np.where(neurons_data == "V"))
    NO = get_index_value(neurons_data, np.where(neurons_data == "O"))
    ND = get_index_value(neurons_data, np.where(neurons_data == "D"))
    NP = get_index_value(neurons_data, np.where(neurons_data == "P"))

    len_svd_sub = len(get_index_value(subverdet_data, np.where(subverdet_data == "sub")))
    len_svd_ver = len(get_index_value(subverdet_data, np.where(subverdet_data == "ver")))
    len_NL = len(NL)
    len_NM = len(NM)
    len_NS = len(NS)
    len_NV = len(NV)
    len_NO = len(NO)
    len_ND = len(ND)
    len_NP = len(NP)

    path_ = os.path.join(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Report"))
    if not os.path.exists(path_):
        os.mkdir(path_)
    save_path = os.path.join(path_, "Images")
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    else:
        for i in os.listdir(save_path):
            del_file = os.path.join(save_path, i)
            os.remove(del_file)
    def Test1():
        myexplode = [0.1] * 7
        data = np.array([len_NS, len_NV, len_NO, len_NL, len_ND, len_NP, len_NM])
        total = np.sum(data)
        labels = [f"{round((data[0] / total) * 100, 2)}% Subjetcs", f"{round((data[1] / total) * 100, 2)}% Verbs",
                  f"{round((data[2] / total) * 100, 2)}% Objects", f"{round((data[3] / total) * 100, 2)}% Learnings",
                  f"{round((data[4] / total) * 100, 2)}& Descriptions", f"{round((data[5] / total) * 100, 2)}% Processes",
                  f"{round((data[6] / total) * 100, 2)}% Memories"]
        plt.pie(data, labels=labels, startangle=90, explode=myexplode, shadow=False)
        plt.title("Neurons Division", loc='left')
        plt.title(f"1% = {total / 100} neurons", loc="right")
        plt.gcf().canvas.set_window_title("Report 1")
        plt.savefig(os.path.join(save_path, "report_1.jpg"))
        plt.show()


    def Test2():
        pre_value_sub = 41
        pre_value_ver = 4
        X = ["Subjects", "Verbs"]
        X_axis = np.arange(len(X))
        plt.bar(X_axis - 0.2, [pre_value_sub, pre_value_ver], 0.4, label = 'Previous')
        plt.bar(X_axis + 0.2, [len_svd_sub, len_svd_ver], 0.4, label = 'Current')

        plt.xticks(X_axis, X)
        plt.ylabel("Neurons (in Numbers)")
        plt.grid(axis='y', color='green', linestyle='--')
        plt.title("Subject Verb Details ", loc='left')
        plt.legend(["Pre-build", "With Learned"])
        plt.gcf().canvas.set_window_title("Report 2")
        plt.savefig(os.path.join(save_path, "report_2.jpg"))
        plt.show()

    def Test3():
        data = np.array(research_file.read()["runtime"])
        runcount = research_file.read()["runcount"]
        date, runtime = [int(i[-2:]) for i in data[:, 0]], [float(i) / 60 for i in data[:, 1]]
        date_time_from = datetime.datetime.strptime(data[0][0], "%Y-%m-%d")
        date_time_to = datetime.datetime.strptime(data[-1][0], "%Y-%m-%d")
        plt.bar(date, runtime)
        plt.ylabel("Time (in Minutes)")
        plt.xlabel(
            f"Date ({date_time_from.strftime('%b')} {date_time_from.strftime('%d')} - {date_time_to.strftime('%b')} {date_time_to.strftime('%d')})")
        plt.grid(axis='y', color='green', linestyle='--')
        plt.title(f"SLAi-Code Runtime Details:\nrun count: {runcount} times", loc='left')
        plt.gcf().canvas.set_window_title("Report 3")
        plt.savefig(os.path.join(save_path, "report_3.jpg"))
        plt.show()


    def Test4():
        data = np.array(research_file.read()["database_size"])
        date, size = [(i[-2:]) for i in data[:, 0]], [int(i) / 1024 for i in data[:, 1]]

        date_time_from = datetime.datetime.strptime(data[0][0], "%Y-%m-%d")
        date_time_to = datetime.datetime.strptime(data[-1][0], "%Y-%m-%d")

        plt.plot(date, size, ls='-', marker="o")
        plt.xlabel(
            f"Date ({date_time_from.strftime('%b')} {date_time_from.strftime('%d')} - {date_time_to.strftime('%b')} {date_time_to.strftime('%d')})")
        plt.ylabel("Size (in KB)")
        plt.title("Database Size", loc='left')
        plt.grid(axis='y', color='green', linestyle='--')
        plt.grid(axis='x', color='green', linestyle='--')
        plt.gcf().canvas.set_window_title("Report 4")
        plt.savefig(os.path.join(save_path, "report_4.jpg"))
        plt.show()


    def Test5():
        myexplode = [0.1] * 3
        asked = np.array(research_file.read()["asked"])
        answered = np.array(research_file.read()["answered"])
        opened = np.array(research_file.read()["opened"])
        unanswered = asked - answered
        data = [answered, unanswered, asked]
        plt.pie(data, labels=[f"Answered {answered} questions", f"Unanswered {unanswered} questions",
                              f"Received {asked} questions"], startangle=120, explode=myexplode)
        plt.title(f"Learned Information of SLAI-Code:\nCode Opened {opened} times", loc='left')
        plt.gcf().canvas.set_window_title("Report 5")
        plt.savefig(os.path.join(save_path, "report_5.jpg"))
        plt.show()


    def Test6():
        date_, time_ = [], []
        for i in NS:
            date__, time__ = i[3].date(), i[3].time()
            date_.append(date__.day)
            time_.append((time__.hour * 3600 + time__.minute * 60 + time__.second) / 3600)
        plt.scatter(date_, time_)

        date_, time_ = [], []
        for i in NV:
            date__, time__ = i[3].date(), i[3].time()
            date_.append(date__.day + 0.15)
            time_.append((time__.hour * 3600 + time__.minute * 60 + time__.second) / 3600)
        plt.scatter(date_, time_)

        date_, time_ = [], []
        for i in NO:
            date__, time__ = i[3].date(), i[3].time()
            date_.append(date__.day + 0.3)
            time_.append((time__.hour * 3600 + time__.minute * 60 + time__.second) / 3600)
        plt.scatter(date_, time_)

        date_, time_ = [], []
        for i in ND:
            date__, time__ = i[3].date(), i[3].time()
            date_.append(date__.day + 0.45)
            time_.append((time__.hour * 3600 + time__.minute * 60 + time__.second) / 3600)
        plt.scatter(date_, time_)

        date_, time_ = [], []
        for i in NP:
            date__, time__ = i[3].date(), i[3].time()
            date_.append(date__.day + 0.6)
            time_.append((time__.hour * 3600 + time__.minute * 60 + time__.second) / 3600)
        plt.scatter(date_, time_)

        date_, time_ = [], []
        for i in NL:
            date__, time__ = i[3].date(), i[3].time()
            date_.append(date__.day + 0.75)
            time_.append((time__.hour * 3600 + time__.minute * 60 + time__.second) / 3600)
        plt.scatter(date_, time_)

        date_, time_ = [], []
        for i in NM:
            date__, time__ = i[3].date(), i[3].time()
            date_.append(date__.day + 0.9)
            time_.append((time__.hour * 3600 + time__.minute * 60 + time__.second) / 3600)
        plt.scatter(date_, time_)

        plt.xlabel("Date")
        plt.ylabel("Time (in Hours)")
        plt.title("Neurons Created History")
        plt.grid(axis='y', color='green', linestyle='--')
        plt.grid(axis='x', color='green', linestyle='--')

        plt.legend(["Subjects", "Verbs", "Objects", "Descriptions", "Processes", "Learnings", "Memories"])
        plt.savefig(os.path.join(save_path, "report_6.jpg"))
        plt.gcf().canvas.set_window_title("Report 6")
        plt.show()

    def Test7():
        X = ["Verbs", "Neurons", "Memories", "History", "Subverdet"]
        X_axis = np.arange(len(X))
        plt.bar(X_axis - 0.2, [2, 13, 0, 2, 45], 0.4, label = 'Previous')
        plt.bar(X_axis + 0.2, [verbs_count, len(neurons_data), len(memories), len(history_neurons), len(subverdet_data)], 0.4, label = 'Current')

        plt.xticks(X_axis, X)
        plt.ylabel("Counts (in Numbers)")
        plt.grid(axis='y', color='green', linestyle='--')
        plt.title(f"Previous and Current Number of Neurons in Database Tables\ntill now ({datetime.datetime.today().strftime('%b %d')})")
        plt.legend(["Previous", "Current"])
        plt.gcf().canvas.set_window_title("Report 7")
        plt.savefig(os.path.join(save_path, "report_7.jpg"))
        plt.show()

    def save_pdf():
        save_report_path = os.path.join(path_, "Doc")
        if not os.path.exists(save_report_path):
            os.mkdir(save_report_path)

        image_list = []
        for i in os.listdir(save_path):
            image = Image.open(os.path.join(save_path, i))
            image_list.append(image.convert('RGB'))
        d = datetime.datetime.today()
        file_name = d.strftime("%Y_%m_%d_%H_%M_%S.pdf")
        image_list[0].save(os.path.join(save_report_path, file_name), save_all=True, append_images=image_list[1:])
    Test1()
    Test2()
    Test3()
    Test4()
    Test5()
    Test6()
    Test7()
    save_pdf()


@contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

# Execute File
def execute_file(file_path):
    with stdoutIO() as s:
        with open(file_path, 'rb') as file:
            ff = compile(file.read(), 'exx.py', 'exec')
            exec(ff, locals())
            if 'result' in locals():
                sys.stdout.write(locals().get('result'))
    return s.getvalue()[:-1]

def create_file(dir_, code):
    file = filehandler.FileHandler(dir_)
    file.write(code.encode())


# word availability
def wordsUnavailability(words):
    db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
    db = database.Database(db_path)
    output_false = []
    for word in words:
        get_ = db.table_data("neurons", search=["name", f"'{word}'"], like='=')
        if not get_:
            output_false.append(word)
    return output_false


def nid_string(nid):
    db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
    db = database.Database(db_path)
    get_ = db.table_data("neurons", search=["nid", f"'{nid}'"], like='=')
    return get_[0][4]


def str2list(string_):
    l = string_.strip("[]").split(", ")
    return l


# most frequent
def most_frequent(List):
    get_ = []
    count = 0
    for i in List:
        current_frequent = List.count(i)
        if current_frequent > count:
            count = current_frequent
    for i in List:
        current_frequent = List.count(i)
        if current_frequent == count:
            if i not in get_:
                get_.append(i)
    return get_


# ranking algorithm
def rankning(ids):
    global result
    db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
    db = database.Database(db_path)

    final = []
    for q_word in ids:
        output = db.table_data("history_neurons", search=[["questions", f"'%{q_word}%'"]], like=["LIKE"])
        if output:
            for i in range(len(output)):
                final.append(output[i][1])

    final = most_frequent(final)
    print(final, "final")
    if final:
        return final[-1]
        # new = []
        # for i in final:
        #     if i.issubset(ids):
        #         new.append(i)
        # if new:
        #     return new[0]
    else:
        return False


# create id
def create_id(type_):
    id_ = type_ + str(time.time())
    return id_


# verbs
def verbs(name):
    db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
    db = database.Database(db_path)
    get_ = db.table_data("neurons", search=[["name", f"'{name}'"], ["type", "'verb'"]], condition=["AND"],
                         like=["=", "="])
    if not get_:
        id_ = create_id("NV")
        db.insert("neurons", [id_, name, "verb", ""])
        return True
    else:
        return False

# add_verb
def add_verb(names):
    db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
    db = database.Database(db_path)
    get_ = db.table_data("verbs", search=[["present", f"'{names[0]}'"]], like=["="])
    if not get_:
        db.insert("verbs", [names[0], names[2], names[1]])
        return True
    else:
        return False

# subject
def subject(name):
    db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
    db = database.Database(db_path)
    get_ = db.table_data("neurons", search=[["name", f"'{name}'"], ["type", "'subject'"]], condition=["AND"],
                         like=["=", "="])

    if not get_:
        id_ = create_id("NS")
        db.insert("neurons", [id_, name, "subject", ""])
        return True
    else:
        return False


# object
def object_(name):
    db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
    db = database.Database(db_path)
    get_ = db.table_data("neurons", search=[["name", f"'{name}'"], ["type", "'object'"]], condition=["AND"],
                         like=["=", "="])

    if not get_:
        id_ = create_id("NO")
        db.insert("neurons", [id_, name, "object", ""])
        return True
    else:
        return False


# history of the brain
def store_learnings(question, answer, subject_, verb, original_question):
    db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
    db = database.Database(db_path)
    get_ = db.table_data("history_neurons", search=[["questions", f"'{question}'"]], like=["="])

    if not get_:
        id_ = create_id("NL")
        db.insert("history_neurons", [id_, question, answer, subject_, verb, original_question])


def process(name, data):
    db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
    db = database.Database(db_path)
    get_ = db.table_data("neurons", search=[["name", f"'{name}'"], ["type", "'process'"]], condition=["AND"],
                         like=["=", "="])
    if get_:
        db.update_table("neurons", from_= ["'nid'", f"'{get_[1]}'"], to= ["'data'", f"'{data}'"])
    else:
        db.insert("neurons", [create_id("NP"), name, "process", data])

def split_quoted(text):
    split_chr = "\'"
    if "\"" in text:
        split_chr = "\""
    text = text.strip()
    splitted = text.split(split_chr)
    print(splitted)
    if len(splitted) == 2:
        value = [i.strip() for i in splitted[0].split()]
    if len(splitted) == 3:
        value = [i.strip() for i in splitted[0].split()]
        value.append(splitted[1])
        value.extend([i.strip() for i in splitted[2].split()])

    return value


# Tense
class Tense:
    def __init__(self, sentence):
        self.answer = ""
        self.sentence = sentence
        self.auxiliary = None
        self.verb = None
        self.tense = "present"
        self.subject = None
        self.get_what = False
        self.changeable_pronoun = ["i", "you", "your", "my"]

        db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
        self.db = database.Database(db_path)

        self.ddd = ["do", "did", "does"]
        h_verb_what = ["will", "shall", "am", "is", "are", "were", "was", "do", "did", "does"]
        h_verb_present = ["am", "is", "are", "be", "do", "does"]
        h_verb_past = ["were", "was", "did"]
        h_verb_future = ["will", "shall"]
        subjects = ["i", "you", "your", "my"]
        what = ["what", "when", "where", "who", "whom", "which", "whose", "why", "how"]
        pronouns = ["your", "you", "my", "i"]
        pronouns = ["my", "i", "your", "you"]
        verbs = []
        try:
            if "did" in self.sentence[0] or "did" in self.sentence[1]:
                verbs = ["does", "do"]
                h_verb_present.remove("does")
                h_verb_present.remove("do")
        except:
            pass

        if "do" in self.sentence[0] or "do" in self.sentence[0]:
            verbs = ["does", "did"]
            h_verb_past.remove("did")
            h_verb_present.remove("does")

        if "does" in self.sentence[0] or "does" in self.sentence[0]:
            verbs = ["did", "do"]
            h_verb_past.remove("did")
            h_verb_present.remove("do")

        for word in sentence:
            if word in h_verb_present:
                self.auxiliary = word
                self.tense = "present"
            elif word in h_verb_past:
                self.auxiliary = word
                self.tense = "past"
            elif word in h_verb_future:
                self.auxiliary = word
                self.tense = "future"

            sub = self.db.table_data(table= "neurons", search= [["name", f"'{word}'"],["type", "'subject'"]], like= ["=", "="], condition= ["AND"])
            if sub or word in subjects:
                self.subject = word

            if not self.get_what:
                if word in what:
                    self.stype = "question"
                    self.get_what = True
                else:
                    self.stype = "sentence"

            ver = self.db.table_data("neurons", search= [["name", f"'{word}'"],["type", "'verb'"]], like= ["=", "="], condition= ["AND"])
            if ver:
                self.verb = word
            elif verbs:
                if word in verbs:
                    self.verb = word

        if self.sentence[0] in h_verb_what:
            self.stype = "question-yn"

        if self.tense == "past":
            self.past()
        if self.tense == "future":
            self.future()
        if self.tense == "present":
            self.present()
        print(self.get_answer())

    def present(self):
        if self.stype == "question":
            if self.subject is not None:
                if self.subject in self.changeable_pronoun:
                    self.subject = self.change_pronoun()
                self.answer += f"{self.subject} "
            if self.verb is not None:  #
                self.answer += f"{self.verb} "
            if self.auxiliary is not None:
                if self.subject == "i":
                    self.auxiliary = "am"
                self.answer += f"{self.auxiliary}"
        elif self.stype == "question-yn":
            if self.subject is not None:
                if self.subject in self.changeable_pronoun:
                    self.subject = self.change_pronoun()
                self.answer += f"{self.subject} "
                try:
                    if self.sentence[0] in self.ddd and self.verb is not None:
                        self.answer += self.verbPluS()
                except:
                    print("The verb: {self.verb} details is not there in the database.")

            else:
                if self.subject != "i":
                    if self.auxiliary is not None:
                        self.answer += f"{self.auxiliary} "
                try:
                    if self.verb is not None:
                        self.answer += self.verbPluS()
                except:
                    print("The verb: {self.verb} details is not there in the database.")

    def past(self):
        if self.stype == "question":
            if self.subject is not None:
                if self.subject in self.changeable_pronoun:
                    self.subject = self.change_pronoun()
                self.answer += f"{self.subject} "
            if self.sentence[1] in self.ddd:
                try:
                    if self.verb is not None:
                        self.answer += f"{self.present2past()}, "
                except:
                    print("The verb: {self.verb} details is not there in the database.")

            else:
                if self.verb is not None:
                    self.answer += f"{self.verb} "
                if self.auxiliary is not None:
                    self.answer += f"{self.auxiliary} "
        elif self.stype == "question-yn":
            if self.subject is not None:
                if self.subject in self.changeable_pronoun:
                    self.subject = self.change_pronoun()
                self.answer += f"{self.subject} "
            if self.sentence[0] == "did":
                try:
                    if self.verb is not None:
                        self.answer += f"{self.present2past()}, "
                except:
                    print("The verb: {self.verb} details is not there in the database.")

            else:
                if self.auxiliary is not None:
                    self.answer += f"{self.auxiliary}"
                if self.verb is not None:
                    self.answer += f"{self.verb} "

    def future(self):
        if self.stype == "question":
            if self.subject is not None:
                if self.subject in self.changeable_pronoun:
                    self.subject = self.change_pronoun()
                self.answer += f"{self.subject} "
            if self.auxiliary is not None:
                self.answer += f"{self.auxiliary} "
            if self.verb is not None:
                self.answer += f"{self.verb} "
        elif self.stype == "question-yn":
            if self.subject is not None:
                if self.subject in self.changeable_pronoun:
                    self.subject = self.change_pronoun()
                self.answer += f"{self.subject} "
            if self.auxiliary is not None:
                self.answer += f"{self.auxiliary} "
            if self.verb is not None:
                self.answer += f"{self.verb} "
        else:
            self.change_pronoun()

    def present2past(self):
        db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
        db = database.Database(db_path)
        get_ = db.table_data("verbs", search=[["present", f"'{self.verb}'"]], like=["="])
        return get_[0][2]

    def verbPluS(self):
        db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
        db = database.Database(db_path)
        get_ = db.table_data("verbs", search=[["present", f"'{self.verb}'"]], like=["="])
        return get_[0][3]

    def change_pronoun(self):
        if self.subject == "you":
            return "i"
        if self.subject == "i":
            return "you"
        if self.subject == "your":
            return "my"
        if self.subject == "my":
            return "your"

    def get_answer(self):
        print([self.answer, [self.subject, self.verb, self.tense, self.sentence]])
        return [self.answer, [self.subject, self.verb, self.tense, self.sentence]]


class Engine:
    def __init__(self, pre_data, ins, ids):
        self.done = False
        self.opened_what_content = False
        self.what = False
        self.past_verb = "accessed"
        self.answer_content = None
        self.control = None
        self.ins = ins
        dir__ = os.path.join(os.path.dirname(os.path.realpath(__file__)), "researchFile.json")
        self.research_file = filehandler.FileHandler(dir__)

        if pre_data:
            print("Old Data")
            print(ids)
            self.question = ids[0][2]
            self.answer = ids[0][3]
            self.subject = ids[0][4]
            self.verb = ids[0][5]
            db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
            db = database.Database(db_path)

            try:
                print(ids)
                available = db.table_data(table="memories", search= [["subjects", f"'{self.subject}'"], ["verbs", f"'{self.verb}'"]], condition= ['AND'], like=['=', '='])
                print(available, 123)
                if available:
                    self.answer = self.answer.replace("_ans_", available[-1][4])
                else:
                    print("Don't know can you tell me?")
            except:
                pass
            self.ins.activate(12, self.answer)
            self.research_file.append({"answered": self.research_file.read()["answered"] + 1})
            self.done = True

        else:
            print("New Data")
            print(ids)
            self.subject = ids[1][0]
            self.verb = ids[1][1]
            self.tense = ids[1][2]
            self.sentence = ids[1][3]
            self.answer = ids[0].strip()
            self.get_answer = False
            what_type = False
            what = ["what", "when", "where", "who", "whom", "which", "whose", "why", "how"]
            h_verb_tence = ["will", "is", "are", "were", "was"]

            db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
            db = database.Database(db_path)

            # if self.sentence[0] in h_verb_what:
            #     what_type = True

            for w in self.sentence:
                if w in ["desc", "description", "meaning", "explain"]:
                    self.what = True

                if w in what:
                    what_type = True

                if w in h_verb_tence:
                    self.get_answer = True
            print(self.get_answer, self.verb, self.subject, 0)
            if what_type:
                print("What type---")
                if self.what:
                    try:
                        print("what ---")
                        word = self.sentence[-1]
                        status = db.table_data(table= "neurons", search= [["type", "'desc'"], ["name", f"'{word}'"]], like= ['=', '='], condition= ["AND"])
                        if status:
                            self.answer = f"The word '{status[0][2]}' is {status[0][4]}"
                        else:
                            self.answer = "Don't know, can you tell me or complete the question?"
                        self.done = True

                    except:
                        self.answer = "Don't know, can you tell me or complete the question?"

                elif self.subject is not None and self.verb is not None:
                    print("Entered Asking Q---")
                    # try:
                    # if self.subject in ["you", "i", "your", "my"]:
                    #     changed_subject = self.change_pronoun(self.subject)
                    available = db.table_data(table="memories", search= [["subjects", f"'{self.subject}'"], ["verbs", f"'{self.verb}'"]], condition= ['AND'], like=['=', '='])
                    sorted_ = list(self.sentence)
                    sorted_.sort()
                    print(self.subject, self.verb, 90)
                    question_ = " ".join(sorted_).strip()
                    if available:
                        question__ = " ".join(self.sentence).strip() + "?"
                        if self.answer:
                            self.answer_to_save = self.answer + " _ans_"
                            self.answer += f" {available[0][4]}"
                            store_learnings(question_, self.answer_to_save, self.subject, self.verb, question__)
                        else:
                            self.answer_to_save = self.answer + "_ans_"
                            self.answer += f"{available[4]}"
                            store_learnings(question_, self.answer_to_save, self.subject, self.verb, question__)
                        self.done = True
                        self.ins.activate(12, self.answer)
                        self.research_file.append({"answered": self.research_file.read()["answered"] + 1})

                    else:
                        self.ins.activate(12, "Don't know can you tell me?")
                        self.ins.activate(37, "Don't know can you tell me?")
                else:
                    self.ins.activate(12, "Don't know can you tell me?")
                    self.ins.activate(37, "Don't know can you tell me?")

            else:
                if self.get_answer and self.verb is not None and self.subject is not None:
                    print("Adding Answer---")
                    available = db.table_data(table="memories", search= [["subjects", f"'{self.subject}'"], ["verbs", f"'{self.verb}'"]], condition= ['AND'], like=['=', '='])
                    ans = self.sentence[0]
                    self.subject = self.change_pronoun(self.subject)
                    print(ans, self.subject, self.verb, 10100101)
                    print(available, "0001")
                    if available:
                        print(self.subject, 10)
                        db.query(f"""UPDATE memories SET answer = '{ans}' WHERE subjects = '{self.subject}' AND verbs = '{self.verb}'""")
                        db.close()

                    else:
                        print(self.subject, 111)
                        id_ = create_id("NM")
                        db.insert("memories", [f"{id_}", f"{self.subject}", f"{self.verb}", f"{ans}"])
                        self.ins.activate(12, "Ok.")
                        self.research_file.append({"answered": self.research_file.read()["answered"] + 1})
                    self.done = True
                else:
                    try:
                        if self.subject is not None and self.tense == "present":
                            print("subject and present---")
                            get_ = db.table_data("subverdet", search=[["words", f"'{self.subject}'"], ["sv", "'sub'"]],
                                                 condition=["AND"],
                                                 like=["=", "="])
                            self.control = get_[0][2]
                    except:
                        self.ins.activate(12, "Connect the subject with controlling unit")
                        self.ins.activate(37, "Connect the subject with controlling unit")

                    if self.verb is not None:
                        print("verb---")
                        get_ = db.table_data("subverdet", search=[["words", f"'{self.verb}'"], ["sv", "'ver'"]],
                                             condition=["AND"],
                                             like=["=", "="])
                        dim_ = np.array(get_)
                        if dim_.ndim == 2:
                            self.activity = get_[0][2]
                        else:
                            self.activity = "activate"

                        get_ = db.table_data("verbs", search=[["present", f"'{self.verb}'"]], like=["="])
                        if get_:
                            self.past_verb = get_[0][2]

                    else:
                        self.activity = "activate"

                    if self.tense == "present" and self.subject is not None:
                        print("present and subject---")
                        inputs = ["c8", "c12", "c36", "c37", "c38"]
                        activation = ["c2", "c3", "c4", "c5", "c6", "c7", "c11", "c13", "c34", "c35"]
                        deactivation = ["c9", "c10"]

                        activate = ["c39", "c32", "c30", "c28", "c0", "c14", "c16", "c18", "c20", "c22", "c24"]
                        deactivate = ["c40", "c33", "c31", "c29", "c1", "c15", "c17", "c19", "c21", "c23", "c25"]
                        ad = activate + deactivate

                        activation.extend(activate)
                        deactivation.extend(deactivate)

                        self.answer = f"{self.subject} is {self.past_verb}."

                        if self.activity == "activate":
                            print("Activate---")
                            if self.control in deactivate:
                                self.control = activate[deactivate.index(self.control)]
                            if self.control in activation:
                                try:
                                    self.ins.activate(value=int(self.control[1:]), data=None)
                                    self.research_file.append({"answered": self.research_file.read()["answered"] + 1})
                                    self.done = True
                                except:
                                    self.ins.activate(12, "Turn on control, then start")
                                    self.ins.activate(37, "Turn on control, then start")

                        elif self.activity == "deactivate":
                            print("Deactivate---")
                            if self.control in activate:
                                self.control = deactivate[activate.index(self.control)]
                            if self.control in deactivation:
                                try:
                                    self.ins.activate(value=int(self.control[1:]), data=None)
                                    self.research_file.append({"answered": self.research_file.read()["answered"] + 1})
                                    self.done = True
                                except:
                                    self.ins.activate(12, "Turn on control, then start")
                                    self.ins.activate(37, "Turn on control, then start")

                        elif self.activity == "input":
                            print("Input---")
                            if "data" in self.sentence:
                                print(self.sentence)
                                if ("dir" in self.sentence) or ("path" in self.sentence) or ("directory" in self.sentence):
                                    self.data = self.sentence[-1]
                                    print(self.sentence[-1])
                                elif "text" in self.sentence:
                                    try:
                                        self.data = " ".join(self.sentence[self.sentence.index("text") + 1:])
                                    except:
                                        print("Execution Failed due to lack of data input")

                            else:
                                print("Execution Failed due to lack of data input")

                            if self.control in inputs:
                                self.ins.activate(value=int(self.control[1:]), data=self.data)
                                self.answer = f"{self.subject} is {self.past_verb}."
                                self.ins.activate(12, self.answer)
                                self.research_file.append({"answered": self.research_file.read()["answered"] + 1})
                                self.done = True

        if self.done:
            self.ins.activate(37, self.answer)
            self.ins.activate(37, "Done.")
            self.research_file.append({"answered": self.research_file.read()["answered"] + 1})

        else:
            self.ins.activate(37, "What? complete the sentence.")
            self.research_file.append({"answered": self.research_file.read()["answered"] + 1})

    def change_pronoun(self, pronoun):
        if pronoun == "you":
            return "i"
        if pronoun == "i":
            return "you"
        if pronoun == "your":
            return "my"
        if pronoun == "my":
            return "your"
        else:
            return pronoun


class RunCode:
    def __init__(self, ins):
        self.old_ids = []
        self.get_reply = False
        self.ins = ins
        dir__ = os.path.join(os.path.dirname(os.path.realpath(__file__)), "researchFile.json")
        self.research_file = filehandler.FileHandler(dir__)
        self.previous_id = None

    def send(self, sentence):
        print("Entered RunCode---")
        sentence = sentence
        db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
        db = database.Database(db_path)
        sentence_ = list(sentence)
        sentence_.sort()
        search = " ".join(sentence_).strip()
        get_ = db.table_data("history_neurons", search=[["questions", f"'{search}'"]], like=["="])
        if get_:
            print("Already available history neurons---")
            self.previous_id = [get_[0]]
            Engine(pre_data=True, ins=self.ins, ids=self.previous_id)
        else:
            what = ["what", "when", "where", "who", "whom", "which", "whose", "why", "how"]
            do_ranking = False
            for w in sentence:
                if w in what:
                    do_ranking = True
            if do_ranking:
                get_ = rankning(sentence)
            print(get_, "ranking---")

            if get_ and self.get_reply is not True:
                print("Ranking Checkup--")
                self.previous_id = db.table_data("history_neurons", search=[["nid", f"'{get_}'"]], like=["="])
                self.ins.activate(37, f"You're asking, '{self.previous_id[0][6]}'")
                self.research_file.append({"answered": self.research_file.read()["answered"] + 1})
                self.get_reply = True
                self.previous_sentence = sentence
                self.old_ids = sentence

            elif self.get_reply:
                print("Replying")
                self.get_reply = False
                if "yes" in sentence or "yeah" in sentence:
                    Engine(pre_data=True, ins=self.ins, ids=self.previous_id)
                elif "no" in sentence or "not" in sentence:
                    self.ins.activate(37, "Ranking Operation rejected")
                    tense_algorithm = Tense(self.previous_sentence)
                    self.previous_id = tense_algorithm.get_answer()
                    print("Engine---,,---")
                    Engine(pre_data=False, ins=self.ins, ids=self.previous_id)

                else:
                    print(sentence)
                    # print("started---0")
                    tense_algorithm = Tense(sentence)
                    self.previous_id = tense_algorithm.get_answer()
                    print("Engine---,,")
                    Engine(pre_data=False, ins=self.ins, ids=self.previous_id)

            else:
                print("Regular Circuit---")
                # if sentence[0] == "change":
                #     if self.previous_id is not None:
                #         if sentence[1] == "answer":
                #             answer= None
                #             if "as" == sentence[1]:
                #                 answer= sentence[sentence.index("as")+ 1:]
                #             elif "," == sentence[1]:
                #                 answer= sentence[sentence.index(",")+ 1:]
                #             elif "into" == sentence[1]:
                #                 answer= sentence[sentence.index("into")+ 1:]
                #             elif "to" == sentence[1]:
                #                 answer= sentence[sentence.index("to")+ 1:]
                #             else:
                #                 answer= sentence[2:]
                #             if answer is not None:
                #                 answer = " ".join(answer)
                #                 self.previous_id.pop(3)
                #                 self.previous_id.insert(3, answer)
                #                 db.update_table("history_neurons", from_= ["'nid'", f"'{self.previous_id[1]}'"], to= ["'answers'", f"'{answer}'"])
                #
                #         if sentence[1] == "word":
                #             ans_words = self.previous_id[3].strip().split()
                #             from_to_ = sentence[sentence.index("word")+ 1:]
                #             from_,  to_ = from_to_[0], from_to_[-1]
                #             if from_ in ans_words:
                #                 ans_words.replace(from_, to_)
                #                 answer= " ".join(ans_words)
                #                 self.previous_id.pop(3)
                #                 self.previous_id.insert(3, ans_words)
                #                 db.update_table("history_neurons", from_= ["'nid'", f"'{self.previous_id[1]}'"], to= ["'answers'", f"'{self.previous_id[3]}'"])
                #
                # elif sentence[0] == "remove":
                #     if self.previous_id is not None:
                #         answer = None
                #         if sentence[1] == "word":
                #             ans_words = self.previous_id[3].strip().split()
                #             remove = sentence[sentence.index("word")+ 1:]
                #             if len(remove) >= 1:
                #                 r = remove[-1]
                #                 if r in ans_words:
                #                     ans_words.remove(r)
                #                     ans_words= " ".join(ans_words)
                #                     self.previous_id.pop(3)
                #                     self.previous_id.insert(3, ans_words)
                #                     db.update_table("history_neurons", from_= ["'nid'", f"'{self.previous_id[1]}'"], to= ["'answers'", f"'{self.previous_id[3]}'"])
                #
                # elif sentence[0] == "add" and "word" in sentence:
                #     if "after" in sentence:
                #         ans_words = self.previous_id[3].strip().split()
                #         last = sentence[-1]
                #         if last in ans_words:
                #             word = sentence[sentence.index("word")+ 1]
                #             ans_words.insert(ans_words.index(last)+ 1, word)
                #
                #             ans_words= " ".join(ans_words)
                #             self.previous_id.pop(3)
                #             self.previous_id.insert(3, ans_words)
                #             db.update_table("history_neurons", from_= ["'nid'", f"'{self.previous_id[1]}'"], to= ["'answers'", f"'{self.previous_id[3]}'"])
                #
                #     if "after" in sentence:
                #         ans_words = self.previous_id[3].strip().split()
                #         last = sentence[-1]
                #         if last in ans_words:
                #             word = sentence[sentence.index("word")+ 1]
                #             place = ans_words.index(last)- 1
                #             if place == -1:
                #                 place = 0
                #             ans_words.insert(place, word)
                #
                #             ans_words= " ".join(ans_words)
                #             self.previous_id.pop(3)
                #             self.previous_id.insert(3, ans_words)
                #             db.update_table("history_neurons", from_= ["'nid'", f"'{self.previous_id[1]}'"], to= ["'answers'", f"'{self.previous_id[3]}'"])
                #
                #     if "end" in sentence:
                #         ans_words = self.previous_id[3].strip().split()
                #         word = sentence[sentence.index("word")+ 1]
                #         ans_words.append(word)
                #
                #         ans_words= " ".join(ans_words)
                #         self.previous_id.pop(3)
                #         self.previous_id.insert(3, ans_words)
                #         db.update_table("history_neurons", from_= ["nid", f"{self.previous_id[1]}"], to= ["answers", f"'{self.previous_id[3]}'"])

                # else:
                print(sentence)
                print("started---0")
                tense_algorithm = Tense(sentence)
                self.previous_id = tense_algorithm.get_answer()
                print("Engine---")
                Engine(pre_data=False, ins=self.ins, ids=self.previous_id)


class SlaiCode:
    def __init__(self, system_control):
        self.asking_value = []
        self.do = False
        self.do_ = True
        self.drone_work = False
        self.process_name = None
        self.engine = RunCode(system_control)
        self.activation = False
        self.test = []
        self.asking = False
        self.x1 = 0
        self.y1 = 0
        self.knowing_order = None
        self.know_word = None
        self.to_know_words = []
        self.unavailable_words = []
        self.check_list = None
        self.next_process = False
        self.code = ""
        self.response = "off"
        self.output = None
        self.words = None
        self.system_control = system_control
        self.text = None
        self.ai_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "slai-file.py")
        db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
        self.db = database.Database(db_path)

        dir__ = os.path.join(os.path.dirname(os.path.realpath(__file__)), "researchFile.json")
        self.research_file = filehandler.FileHandler(dir__)

        self.research_file.append({"opened": self.research_file.read()["opened"] + 1})
        database_size = self.research_file.read()

        dict__ = database_size["database_size"]
        dict_ = numpy.array(dict__)
        try:
            if str(datetime.date.today()) not in dict_[:, 0]:
                dict__.append([str(datetime.date.today()), os.path.getsize(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db"))])
                self.research_file.append({"database_size": dict__})
            else:
                del dict__[-1]
                dict__.append([str(datetime.date.today()), os.path.getsize(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db"))])
                self.research_file.append({"database_size": dict__})
        except:
            dict__.append([str(datetime.date.today()), os.path.getsize(os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db"))])
            self.research_file.append({"database_size": dict__})

    def start(self):
        pass

    def end(self):
        pass

    def input(self, text=None):
        self.text = text

    def check_conditions(self):
        self.text = self.text.strip("? ")
        if "'" in self.text or '"' in self.text:
            self.words = split_quoted(self.text)
        else:
            self.words = self.text.split()
        self.check_words()

    def check_words(self):
        self.check_list = wordsUnavailability(self.words)
        for w in self.check_list:
            if ":" in w:
                self.check_list.remove(w)

        # self.to_know_words = self.check_list[1]
        # for word in self.to_know_words:
        #     if word not in self.unavailable_words:
        #         self.unavailable_words.append(word)
        # if not self.unavailable_words:
        #     self.activation = True

    def ask_words(self):
        if self.check_list:
            if len(self.check_list) == 1:
                ask__ = f"What is {self.check_list[0]}?"
                self.ask(ask__)
                self.system_control.activate(12, ask__)
                self.research_file.append({"answered": self.research_file.read()["answered"] + 1})
            else:
                ask_ = ', \n'.join(self.check_list)
                ask__ = f"What is {ask_}?"
                self.ask(ask__)
                self.system_control.activate(12, ask__)
                self.research_file.append({"answered": self.research_file.read()["answered"] + 1})

            # else:
            #     self.activation = True

    def ask(self, text):
        self.system_control.activate(37, text)
        self.research_file.append({"answered": self.research_file.read()["answered"] + 1})
        self.response = 'on'

    def code_analyzer(self):
        self.do_ = True
        output_data_text = None

        # try:
        print("code analyser started---")
        get_ = ["", "", "", ""]
        get_ = self.db.table_data("subverdet", search=[["words", f"'{self.words[0]}'"], ["sv", "'ver'"]],
                                  condition=["AND"],
                                  like=["=", "="])

        print(self.words, 10000)
        data_find = {"ver": "verb",
                     "sub": "subject",
                     "obj": "object",
                     }
        if (len(self.words) == 1 and ("report" not in self.words and "emergency" not in self.words and "yeah" not in self.words and "yes" not in self.words and "no" not in self.words and "not" not in self.words)) or ("info" in self.words or "information" in self.words and len(self.words) > 1):
            print("entered info path---")
            info_word = self.words[-1]
            above_lines = ""
            get_ = self.db.table_data("subverdet", search=[["words", f"'{info_word}'"]], like=["="])
            if get_:
                if get_[0][3] == "ver":
                    above_lines += f"""The word '{info_word}' is a verb to {get_[0][2]} the process,\n"""
                elif get_[0][3] == "sub":
                    above_lines += f"""The word '{info_word}' is a subject and having control of {get_[0][2]},\n"""
                else:
                    above_lines += f"""The word '{info_word}' is having no control and no process command,\n"""
            else:
                above_lines += f"""The word '{info_word}' is having no control and no process command,\n"""

            get_ = self.db.table_data("neurons", search=[["name", f"'{info_word}'"]], like=["="])

            if get_:
                above_lines += f"""it is added as a {get_[0][3]} in my database,\n"""
                if get_[0][4]:
                    above_lines += f"""the meaning of the word '{info_word}' is {get_[0][4]}\n"""
            else:
                above_lines += f"""it is not added as a subject or verb in my database,\n"""

            get_present = self.db.table_data("verbs", search=[["present", f"'{info_word}'"]], like=["="])
            get_past = self.db.table_data("verbs", search=[["past", f"'{info_word}'"]], like=["="])
            get_singular = self.db.table_data("verbs", search=[["singular", f"'{info_word}'"]], like=["="])

            if get_present:
                above_lines += f"""it is a present verb,
'{get_present[0][2]}' is a past form it and
'{get_present[0][3]}' is a verb + (s or es) form it."""

            elif get_past:
                above_lines += f"""it is a past form of {get_past[0][1]}
'{get_present[0][3]}' is a verb + (s or es) form it."""

            elif get_singular:
                above_lines += f"""it is a verb + (s or es) form of {get_singular[0][1]}
'{get_singular[0][2]}' is a past form of it."""

            else:
                above_lines += f"""{info_word} is not added as verb in my database.\nCan you add?"""

            self.system_control.activate(37, above_lines)
            self.system_control.activate(12, "Here you go")
            self.research_file.append({"answered": self.research_file.read()["answered"] + 1})

        elif "report" in self.words:
            print("report---")
            open_research_module()
            original_path = os.path.dirname(os.path.realpath(__file__))
            self.system_control.activate(12, "Created report, check below path")
            self.system_control.activate(37, f"Created report, check this directory {os.path.join(os.path.join(original_path, 'Report'), 'Doc')}")

        elif "database" in self.words:
            try:
                command = self.words[self.words.index("database")+ 1:]
                j_command = " ".join(command)
                output_data_text = self.db.query(f"""{j_command}""")
                print(j_command, 0)
                output_data_text = [i for i in output_data_text.fetchall()]
                print(output_data_text, 0)
                self.db.close()
                if output_data_text:
                    output_data_text = numpy.array(output_data_text)
                    output_data_text = pandas.DataFrame(output_data_text)
                    self.system_control.activate(37, str(output_data_text))
                    self.system_control.activate(12, "Here the results,")
                    self.research_file.append({"answered": self.research_file.read()["answered"] + 1})
                else:
                    self.system_control.activate(37, str(output_data_text))
                    self.system_control.activate(12, "Nothing found or updated  database.")
                    self.research_file.append({"answered": self.research_file.read()["answered"] + 1})
            except:
                tell = f"query command is incorrect, if you want to learn SQL operations and all related materials, follow the below link"
                self.system_control.activate(12, tell)
                link = tell + "\n\nhttps://www.w3schools.com/sql/"
                self.system_control.activate(37, link)
                self.research_file.append({"answered": self.research_file.read()["answered"] + 1})

        elif "system" in self.words and "setting" in self.words:
            try:
                # system setting change voice female
                data_ = None
                default_ = None
                property_ = None
                data_ = self.words[-1]
                if "change" in self.words:
                    property_ = self.words[self.words.index("change") + 1]
                    self.db.update_table("system", from_= ["property", f"%{property_}%"], to= ["data", f"{data_}"], like= "LIKE")
                    above_line = f"in system setting, {property_} value changed into {data_}"
                    self.system_control.activate(37, above_line)
                    self.system_control.activate(12, above_line)
                    self.research_file.append({"answered": self.research_file.read()["answered"] + 1})

                elif "default" in self.words:
                    default_ = self.db.table_data(table= "system", search=["property", f"'%{data_}%'"], like= "LIKE")
                    self.db.update_table("system", from_= ["property", f"%{data_}%"], to= ["data", f"{default_[0][3]}"], like= "LIKE")
                    above_line = f"in system setting, {data_} value changed into default value {default_[0][3]}"

                    self.system_control.activate(37, above_line)
                    self.system_control.activate(12, above_line)
                    self.research_file.append({"answered": self.research_file.read()["answered"] + 1})
            except:
                above_line = "sorry, check your sentence"
                self.system_control.activate(37, above_line)
                self.system_control.activate(12, above_line)
                self.research_file.append({"answered": self.research_file.read()["answered"] + 1})

        else:
            if ("disable" in self.words or "off" in self.words or "deactivate" in self.words) and "speech" in self.words:
                print("speech disable---")
                self.system_control.speech_engine_work = False
                output_data_text = "Disabled speech engine"
                self.do_ = False

            if ("enable" in self.words or "on" in self.words or "activate" in self.words) and "speech" in self.words:
                print("speech enable---")
                self.system_control.speech_engine_work = True
                output_data_text = "Enabled speech engine"
                self.do_ = False
            try:
                if "verb" in self.words or "verbs" in self.words:
                    print("verb---")
                    status = add_verb([self.words[0], self.words[2], self.words[4]])
                    verbs(self.words[0])
                    verbs(self.words[2])
                    verbs(self.words[4])

                    if not status:
                        self.db.update_table("verbs",["present", f"{self.words[0]}"], ["singular", f"{self.words[2]}"])
                        self.db.update_table("verbs",["present", f"{self.words[0]}"], ["past", f"{self.words[4]}"])
                        output_data_text = f"verb {self.words[0]} is updated"
                    else:
                        output_data_text = f"{self.words[0]}, {self.words[2]}, {self.words[4]} are added as verbs"

                    if self.words[0] in self.check_list:
                        self.check_list.remove(self.words[0])
                    if self.words[2] in self.check_list:
                        self.check_list.remove(self.words[2])
                    if self.words[4] in self.check_list:
                        self.check_list.remove(self.words[4])
                    self.do_ = False
            except:
                pass

            try:
                if ("like" in self.words or "same" in self.words) and "word" in self.words:
                    print("subject entering---")
                    word_to_add, into_word = self.words[self.words.index("word")+ 1], self.words[-1]
                    db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Memory-Permanent.db")
                    db = database.Database(db_path)
                    get_ = db.table_data("subverdet", search=[["words", f"'{into_word}'"], ["sv", "'sub'"]],
                                         condition=["AND"],
                                         like=["=", "="])
                    if get_:
                        available = db.table_data("subverdet", search=[["words", f"'{word_to_add}'"], ["sv", "'sub'"]],
                                                  condition=["AND"],
                                                  like=["=", "="])
                        control = get_[0][2]
                        if not available:
                            db.insert("subverdet", [f"{word_to_add}", f"{control}", "sub"])
                            output_data_text = f"{word_to_add} is added similar to {into_word}"
                        else:
                            db.update_table("subverdet", ["words", f"{word_to_add}"], ["control_id", f"{control}"])
                        output_data_text = f"{word_to_add} is updated to the subject {into_word}"
                    else:
                        print(f"There is no subject called {into_word} in my database.")
                        output_data_text = f"What is the subject called {into_word}?"
                    self.do_ = False
            except:
                pass

            if "subject" in self.words:
                print("suject---")
                status = subject(self.words[0])
                if not status:
                    output_data_text = f"already {self.words[0]} is added as subject"
                else:
                    output_data_text = f"{self.words[0]} is added as subject"
                if self.words[0] in self.check_list:
                    self.check_list.remove(self.words[0])
                self.do_ = False

            if "object" in self.words:
                print("object---")
                status = object_(self.words[0])
                if not status:
                    output_data_text = f"already {self.words[0]} is added as object"
                else:
                    output_data_text = f"{self.words[0]} is added as object"
                if self.words[0] in self.check_list:
                    self.check_list.remove(self.words[0])
                self.do_ = False

            # in drone, create process dofront, if position is left side then drone movement will goes to left, on
            # in drone, create process offfront, if position is left side then drone movement will goes to left, off

            try:
                if "in" == self.words[0] and "drone" == self.words[1] and "create" in self.words:
                    print("Drone_Create---")
                    process_name = self.words[self.words.index("process")+1]
                    position = self.words[self.words.index("position")+1]
                    movement = self.words[self.words.index("movement")+1]
                    status = self.words[-1]

                    get_ctrl = self.db.table_data("subverdet", search=[["words", f"'{movement}'"], ["sv", "'sub'"]],
                                                  condition=["AND"],
                                                  like=["=", "="])
                    get_act = self.db.table_data("subverdet", search=[["words", f"'{status}'"], ["sv", "'ver'"]],
                                                 condition=["AND"],
                                                 like=["=", "="])
                    ctrl = get_ctrl[0][2]
                    act = "activate"
                    if get_act:
                        act = get_act[0][2]

                    data = f"{process_name}, {position}, {ctrl}, {act}"
                    process(process_name, data)

                    if process_name in self.check_list:
                        self.check_list.remove(process_name)
                    self.do_ = False

            except:
                print("I can't get you... What?")

            try:
                if get_:
                    if get_[0][1] == "activate" and "drone" == self.words[1] and "process" in self.words:
                        print("Drone_Activate---")
                        process_name = self.words[self.words.index("process")+1]
                        get__ = self.db.table_data("neurons", search=[["name", f"'{process_name}'"], ["type", "'process'"]], condition=["AND"],
                                                   like=["=", "="])
                        if get__:
                            self.process_name = process_name

                        else:
                            print(f"There is no process {process_name}")
                        self.do_ = False

            except:
                pass

            try:
                if ("enable" in self.words or "activate" in self.words or "deactivate" in self.words or "disable" in self.words or "input" in self.words) and "word" in self.words and ("to" in self.words or "for" in self.words):
                    print("enable disable set---")
                    verb, work = self.words[self.words.index("word")+ 1], self.words[-1]
                    check = self.db.table_data("subverdet", search=[["words", f"'{verb}'"], ["sv", "'ver'"]], condition=["AND"],
                                              like=["=", "="])
                    get_ = self.db.table_data("subverdet", search=[["words", f"'{work}'"], ["sv", "'ver'"]], condition=["AND"],
                                              like=["=", "="])
                    duty = get_[0][2]
                    if check:
                        self.db.update_table("subverdet", ["words", f"{verb}"], ["control_id", f"{duty}"])
                        output_data_text = f"{verb} is to {duty}, updated."
                    else:
                        self.db.insert("subverdet", [verb, duty, "ver"])
                        output_data_text = f"{verb} is to {duty}, saved."
                    self.do_ = False

                elif "is" in self.words and "word" in self.words and "like" not in self.words:
                    print("create desc")
                    # the word name is
                    name = self.words[self.words.index("word", 1)+ 1]
                    desc = " ".join(self.words[self.words.index("is")+ 1:])
                    status = self.db.table_data(table= "neurons", search= [["name", f"'{name}'"],["type", f"'desc'"]], like= ["=", "="], condition= ["AND"])
                    print(status, 100)
                    if not status:
                        print("1 desc")
                        id_ = create_id("ND")
                        self.db.insert("neurons", [f"{id_}", f"{name}", f"desc", f"{desc}"])
                        output_data_text = f"the word '{name}' meaning added into my database."
                    else:
                        print("2 desc")
                        self.db.update_table("neurons", ["nid", f"{status[0][1]}"],["data", f"{desc}"])
                        output_data_text = f"the word '{name}' meaning updated into my database."
                    self.do_ = False
            except:
                pass

            try:
                if get_[0][2] == "activate" and "arduino" == self.words[1]:
                    print("Connected, 100000")
                    self.system_control.activate(30)
                    self.system_control.activate(12, "Enabled arduino")
                    self.system_control.activate(37, "Enabled arduino")
                    self.do_ = False
            except:
                pass

            try:
                if get_[0][2] == "deactivate" and "arduino" == self.words[1]:
                    print("Disconnected, 100000")
                    self.system_control.activate(31)
                    self.system_control.activate(12, "Disabled arduino")
                    self.system_control.activate(37, "Disabled arduino")
                    self.do_ = False
            except:
                pass

            try:
                if get_[0][2] == "activate" and "drone" == self.words[1]:
                    print("Activated, 100000")
                    self.system_control.activate(28)
                    self.drone_work = True
                    self.do_ = False

            except Exception as e:
                print(e)

            try:
                if (get_[0][2] == "deactivate" and "drone" == self.words[1]) or "emergency" == self.words[0]:
                    self.system_control.activate(29)
                    self.drone_work = False
                    print("Deactivated, 100000")
                    self.do_ = False
            except:
                pass

            if self.do_:
                print("Engine---")
                self.engine.send(self.words)
            if output_data_text:
                print("speech engine last work")
                self.system_control.activate(37, output_data_text)
                self.system_control.activate(12, output_data_text)
                self.research_file.append({"answered": self.research_file.read()["answered"] + 1})
        # except Exception as e:
        #     print(e, "e")
        #     self.system_control.activate(37, "What?")
        #     self.system_control.activate(12, "What?")
        #     self.research_file.append({"answered": self.research_file.read()["answered"] + 1})

    def process(self):
        self.research_file.append({"runcount": self.research_file.read()["runcount"] + 1})
        # try:
        if self.text is not None:
            self.research_file.append({"asked": self.research_file.read()["asked"] + 1})
            self.check_conditions()
            self.check_words()
            self.code_analyzer()
            self.ask_words()
            self.text = None
            create_file(self.ai_file_dir, self.code)
            # execute_file(self.ai_file_dir) # ToDo: Uncomment

        # except:
        #     self.system_control.activate(37, "Unknown Error Occurred")
        #     self.system_control.activate(12, "Unknown Error Occurred")
        #     self.text = None
        #     time.sleep(1)

            # if self.response == "on":
            #     self.unavailable_words.remove(self.know_word)
            #     self.response = "off"

        # elif self.unavailable_words and self.response == "off":
        #     self.know_word = self.unavailable_words[0]
        #     self.ask(f"What is {self.know_word}?")

        # if self.activation:
        # self.code_analyzer()
        # self.activation = False
        if self.process_name is not None and self.drone_work:
            print("Drone---Started---")
            file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "datum.txt"), "rt")
            data = [float(i) for i in file.read().strip("()").split(", ")]
            x1, y1, *x2_y2 = data
            if x1 < self.x1:
                self.lr = "left"
            else:
                self.lr = "right"

            if y1 < self.y1:
                self.ud = "up"
            else:
                self.ud = "down"

            get_process_name = self.db.table_data("neurons", search=[["name", f"'{self.process_name}'"], ["type", "'process'"]], condition=["AND"],
                     like=["=", "="])

            process_name, position, movement, status = get_process_name[0][4].split(", ")

            activate = ["c14", "c16", "c18", "c20", "c22", "c24"]
            deactivate = ["c15", "c17", "c19", "c21", "c23", "c25"]
            ad = activate + deactivate

            if self.lr == position:
                self.do = True
            if self.ud == position:
                self.do = True

            if self.do:
                if movement in ad:
                    if status == "activate":
                        if movement in deactivate:
                            movement = activate[deactivate.index(movement)]
                        n_ = int(movement[1:])
                        print(n_, "N_")
                        self.system_control.activate(n_)
                        print(int(movement[1:]), "movement")

                    if status == "deactivate":
                        if movement in activate:
                            movement = deactivate[activate.index(movement)]
                        n__ = int(movement[1:])
                        print(n__, "N__")
                        self.system_control.activate(n__)
                        print(int(movement[1:]), "movement")
                self.do = False
            print(self.lr, self.ud, self.x1, self.y1, "Data---")
            self.x1 = x1
            self.y1 = y1

