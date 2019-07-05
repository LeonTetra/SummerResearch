import webscraper as web
import similarity as sim
import similarity_util as su
import plagiarism_model as pm


def main():
    ws = web.WebScraper('Germany', 'weimar')
    if not ws.load_data():
        ws.search()
        ws.save_data()
    ws.quit()
    with open('test.txt', 'r') as fd:
        content = fd.read()
    test = su.Result(title="Test Submission; Please Ignore", author="Duncan Copeland", content=content, date='6/11/2019')
    ws.append_to_data(test)
    s = sim.SimilarityIndex(ws.data)
    inds = s.submit_to_check(test)
    ml = pm.MLPlagiarismChecker(inds)


if __name__ == "__main__":
    main()
