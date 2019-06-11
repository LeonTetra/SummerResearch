import similarity_util as su

class SimilarityIndex:
    def __init__(self, data):
        self.data = data

    def submit_to_check(self, result):
        test = self.data['Content'][1]
        wb = su.BagOfWords(test)
        to_compare = su.BagOfWords(result.content)
        hits = 0
        misses = 0
        for i in to_compare:
            for j in wb:
                if i == j:
                    hits += 1
        print(result.title, ' Results')
        print('hits: ', hits)
        print('misees: ', misses)
        print('per: ', ((hits/(hits+misses))*100))
        print()