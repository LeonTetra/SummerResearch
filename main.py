
import webscraper as web
import similarity as sim

def main():
    ws = web.WebScraper('Germany', 'weimar')
    if not ws.load_data():
        ws.search()
        ws.save_data()
    ws.quit()
    s = sim.SimilarityIndex(ws.data)
    s.submit_to_check()



if __name__ == "__main__":
    main()
