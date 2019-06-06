import similarity_util as su

class SimilarityIndex:
    def __init__(self, data):
        self.data = data

    def submit_to_check(self, result=None):
        test = self.data['Content'][1]
        wb = su.BagOfWords(test)