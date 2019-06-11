import numpy as np
import re

class Result:
    def __init__(self, title='', author='', db='', date='', content=''):
        self.title = title
        self.author = author
        self.db = db
        self.date = date
        self.content = content

class Vocabulary:
    def __init__(self, sentences):
        from sklearn.feature_extraction.text import CountVectorizer
        self.vectorizer = CountVectorizer(analyzer="word", tokenizer=None, preprocessor=None, stop_words=None,
                                     max_features=5000)
        train_data_features = self.vectorizer.fit_transform(sentences)

    def create_bag_of_words(self, text):
        return self.vectorizer.transform(["Machine learning is great"]).toarray()


# These functions were taken from insightsbot.com
# Entry titled "Bag of Words Algorithm in Python Introduction"
# Published 12/09/2017
def extract_words(sentence):
    ignore_words = ['a']
    words = re.sub("[^\w]", " ", sentence).split()  # nltk.word_tokenize(sentence)
    words_cleaned = [w.lower() for w in words if w not in ignore_words]
    return words_cleaned


def tokenize_sentences(sentences):
    words = []
    for sentence in sentences:
        w = extract_words(sentence)
        words.extend(w)

    words = sorted(list(set(words)))
    return words


def bagofwords(sentence, words):
    sentence_words = extract_words(sentence)
    # frequency word count
    bag = np.zeros(len(words))
    for sw in sentence_words:
        for i, word in enumerate(words):
            if word == sw:
                bag[i] += 1
    return np.array(bag)