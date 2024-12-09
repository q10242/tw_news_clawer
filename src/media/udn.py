
import bs4, requests, time
# from src.recorder import to_txt_record
from datetime import datetime, timedelta
class TVBS:
    keyword = None

    url = "https://udn.com/api/more?page="
    page=1
    condition= "&channelId=2&type=searchword&id=search:"
    soup = None
    reach_end = False
    week_limit = None
    def __init__(self,week_limit=None):
        if week_limit is not None:
            self.week_limit = timedelta(weeks=week_limit) # 這是一個timedelta物件

    def search(self, keyword=None):
        api_url = self.url + str(self.page) + self.condition + keyword
        print('TVBS search: ' + keyword)
        html_text = requests.get(api_url).json()
        print(html_text)

if __name__ == '__main__':
    tvbs = TVBS(40)
    tvbs.search('新北市板橋')
    print('Done')