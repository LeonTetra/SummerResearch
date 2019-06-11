import similarity_util as su

class SimilarityIndex:
    def __init__(self, data):
        self.data = data

    def submit_to_check(self, result):
        vocab = su.Vocabulary(self.data['Content'])
        wb = vocab.create_bag_of_words(["Machine learning is great"])
        print(result.title, ' Results')
        print('hits: ', hits)
        print('misees: ', misses)
        print('per: ', ((hits/(hits+misses))*100))
        print()