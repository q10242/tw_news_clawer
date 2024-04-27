
from src.media.ettoday import EtToday
from src.media.tvbs import TVBS

def main(keywords = None, weeks_limit = None):
    ettoday = EtToday(weeks_limit)
    tvbs = TVBS(weeks_limit)
    for keyword in keywords:
        ettoday.search(keyword)
        tvbs.search(keyword)

if __name__ == '__main__':
    main()