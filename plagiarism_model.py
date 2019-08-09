import pandas
from matplotlib import pyplot as plt
import sklearn as skl

class MLPlagiarismChecker:
    def __init__(self, data, submission, sim_indices):
        self.data = data
        self.submission = submission
        self.sim_indices = sim_indices
        dfs = self.build_dataframes()
        km = skl.cluster.KMeans()
        X = (dfs['Similarity Index']).values.reshape(-1, 1)
        model = km.fit(X)
        cluster_labels = model.predict(X)
        cent = model.cluster_centers_
       # self.plot(model, cluster_labels, cent, dfs)

    def build_dataframes(self):
        print()
        df = pandas.DataFrame(self.data)
        df['Similarity Index'] = pandas.Series(self.sim_indices)
        return df

    # def plot(self, model, cluster_labels, cent, df):
    #     kmeans = pandas.DataFrame(cluster_labels)
    #     for i in df:
    #         print()
    #         for j in df:
    #             scatter = plt.scatter(df[i], df[j], c=kmeans[0])
    #             plt.colorbar(scatter)
    #             plt.savefig(i + '_' + j + '.png')
    #             plt.clf()
