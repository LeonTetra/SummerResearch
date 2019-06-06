

class Result:
    def __init__(self, title='', author='', db='', date='', content=''):
        self.title = title
        self.author = author
        self.db = db
        self.date = date
        self.content = content


class BagOfWords:
    def __init__(self, words):
        self.word_bag = self.__create_word_bag(words)

    def __create_word_bag(self, words):
        for i in words:
            print(i)