
from src.media.ettoday import EtToday
from src.media.tvbs import TVBS
from src.media.ltn import LTN

def main(keywords = None, weeks_limit = None):
    ettoday = EtToday(weeks_limit)
    tvbs = TVBS(weeks_limit)
    ltn = LTN(weeks_limit)
    for keyword in keywords:
        ettoday.search(keyword)
        tvbs.search(keyword)
        ltn.search(keyword)

if __name__ == '__main__':
    main()