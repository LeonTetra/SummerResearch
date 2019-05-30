
import webscraper as web


def main():
    ws = web.WebScraper('Germany', 'weimar')
    ws.search()


if __name__ == "__main__":
    main()
