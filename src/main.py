
from src.media.ettoday import EtToday
from src.media.tvbs import TVBS
from src.media.ltn import LTN
from src.media.ftvnews import FtvNews
from src.media.ttv import Ttv

def main(keywords = None, weeks_limit = None):
    ettoday = EtToday(weeks_limit)
    tvbs = TVBS(weeks_limit)
    ltn = LTN(weeks_limit)
    ftvnews = FtvNews(weeks_limit)
    ttv = Ttv(weeks_limit)
    for keyword in keywords:
        # ettoday.search(keyword)
        # tvbs.search(keyword)
        # ltn.search(keyword)
        # ftvnews.search(keyword)
        ttv.search(keyword)

if __name__ == '__main__':
    main()