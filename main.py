
import webscraper as web


def main():
    ws = web.WebScraper()
    res = ws.get_search(topic='Germany', query='weimar')
    print(res[0])
    ws.get_article(res[0])

if __name__ == "__main__":
    main()
