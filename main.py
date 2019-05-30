
import webscraper as web


def main():
    ws = web.WebScraper('Germany', 'hitler')
    ws.search()


if __name__ == "__main__":
    main()
