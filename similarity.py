import similarity_util as su
from sklearn import cluster as c
class SimilarityIndex:
    def __init__(self, data):
        self.data = data
        self.vocabularies = self.build_vocabularies()

    def submit_to_check(self, result):
        wordbags = []
        for i in self.vocabularies:
            wordbags.append(i.create_bag_of_words([result.content]))
        for i in wordbags:
            if i[0].any():
                print(su.find_index(i))
        wordbags = su.compress(wordbags)
        km = c.KMeans()
        km.fit(wordbags)
        print()

    def build_vocabularies(self):
        vocabs = []
        for i in self.data['Content']:
            vocabs.append(su.Vocabulary([i]))
        return vocabs
