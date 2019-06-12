import similarity_util as su

class SimilarityIndex:
    def __init__(self, data):
        self.data = data

    def submit_to_check(self, result):
        vocab = su.Vocabulary(self.data['Content'])
        wb = vocab.create_bag_of_words([result.content])
        print(result.title, ' Results')
        print(su.find_index(wb))
        print()