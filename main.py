
import webscraper as web
import similarity as sim
import similarity_util as su

def main():
    ws = web.WebScraper('Germany', 'weimar')
    if not ws.load_data():
        ws.search()
        ws.save_data()
    ws.quit()
    s = sim.SimilarityIndex(ws.data)
    with open('test_submission_neg.txt', 'r') as fd:
        content = fd.read()
    resneg = su.Result(title="Test Submission Neg", author="Duncan Copeland", content=content, date='6/11/2019')
    with open('test_submission_pos.txt', 'r') as fd:
        content = fd.read()
    respos = su.Result(title="Test Submission Pos", author="Duncan Copeland", content=content, date='6/11/2019')
    s.submit_to_check(resneg)
    s.submit_to_check(respos)



if __name__ == "__main__":
    main()
