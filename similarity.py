import similarity_util as su
from sklearn import cluster as c
class SimilarityIndex:
    def __init__(self, data):
        self.data = data
        self.vocabularies = self.build_vocabularies()

    def submit_to_check(self, result):
        wordbags = []
        indices = []
        for i in self.vocabularies:
            wordbags.append(i.create_bag_of_words(result.content))
        for i in wordbags:
            s = sum(i)
            sim_index = s / su.num_words(result.content)
            indices.append(sim_index)
        return indices

    def build_vocabularies(self):
        vocabs = []
        for i in self.data['Content']:
            vocabs.append(su.Vocabulary([i]))
        return vocabs
