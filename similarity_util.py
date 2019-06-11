

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
        split = words.split(' ')
        length = len(split)
        wb = []
        wb.append(words)
        segs = 1
        step = length
        while step >= 1:
            for i in range(0, segs):
                wb.append(self.__create_long_string(split[(i*step):((i*step)+step)]))
            step = step // 2
            segs *= 2
        return wb

    def __recursively_create_word_list(self, words, length):
        if length <= 1:
            return ""

    @staticmethod
    def __create_long_string(words):
        s = ""
        for i in words:
            s += i + " "
        return s[0:len(s)-1]
