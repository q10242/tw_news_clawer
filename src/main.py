
from src.media.ettoday import EtToday


def main(keywords = None, weeks_limit = None):
    ettoday = EtToday(weeks_limit)
    for keyword in keywords:
        ettoday.search(keyword)

if __name__ == '__main__':
    main()