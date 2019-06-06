
import webscraper as web
import similarity as sim

def main():
    ws = web.WebScraper('Germany', 'weimar')
    if not ws.load_data():
        ws.search()
        ws.save_data()
    s = sim.SimilarityIndex(ws.data)
    s.submit_to_check()
    ws.quit()


if __name__ == "__main__":
    main()
