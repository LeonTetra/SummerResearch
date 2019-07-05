import pandas
from matplotlib import pyplot as plt

class MLPlagiarismChecker:
    def __init__(self, data, submission, sim_indices):
        self.data = data
        self.submission = submission
        self.sim_indices = sim_indices
        dfs = self.build_dataframes()
        #build model and plot figures

    def build_dataframes(self):
        print()
        df = pandas.DataFrame(self.data)
        df['Similarity Index'] = pandas.Series(self.sim_indices)
        return df