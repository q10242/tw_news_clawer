
import bs4, requests, time
from src.recorder import to_txt_record
from datetime import datetime, timedelta
class UDN:
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
        self.keyword = keyword
        not_last_page = True
        while(not_last_page and not self.reach_end):
            print('UDN search: ' + keyword)
            api_url = self.url + str(self.page) + self.condition + keyword
            self.page+=1
            html_json = requests.get(api_url).json()
            news_list= html_json['lists']
            # 如果news_list的長度為0 則已經到底了
            if len(news_list) == 0:
                not_last_page = False
                self.reach_end = True
                break
            self.handle_news(news_list)
            pass
    def handle_news(self, news_list):
        # 這裡傳過來的是一個list 這個list裡面裝的是dict 
        for news in news_list:

            # 這裡的news是一個dict
            self.handle_article(news['titleLink'], news['title'], news['time']['dateTime'])
            if self.reach_end:
                break
           
    def handle_article(self, titleLink, title, dateTime):
        # 如果超過時間限制就停止
        if self.week_limit is not None:
            if datetime.strptime(dateTime, '%Y-%m-%d %H:%M') < datetime.now() - self.week_limit:
                self.reach_end = True
                return
                

        request = requests.get(titleLink)
        soup = bs4.BeautifulSoup(request.text, 'html.parser')
        try:
            author = soup.select('.article-content__subinfo > section > span')[0]
        except IndexError:
            return


        author = (author.text.replace('\n', '').replace(' ', '').replace('聯合報／記者', '').strip())
        content_selector = 'article > div > section.article-content__editor > p'
        contentText = ''
        content = soup.select(content_selector)
        for p in content:
           if p.text.strip() != '':
               contentText += p.text.strip() + '\n'
        to_txt_record('UDN', title, dateTime, author, titleLink, contentText, self.keyword)


if __name__ == '__main__':
    tvbs = TVBS(40)
    tvbs.search('新北市板橋')
    print('Done')