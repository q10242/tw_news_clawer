import bs4, requests, time
from src.recorder import to_txt_record
from datetime import datetime, timedelta
import re
import httpx
# 台視新聞
class Ttv:
    keyword = None
    url = "https://news.ttv.com.tw/search/"
    post_fix = "&chdtv"

    soup = None
    reach_end = False
    week_limit = None
    page=1
    def __init__(self,week_limit=None):
        end_time = datetime.now().date().strftime('%Y%m%d')
        if week_limit is not None:
            self.week_limit = timedelta(weeks=week_limit) # 這是一個timedelta物件
            start_time = (datetime.now() - self.week_limit).date().strftime('%Y%m%d')
        else: 
            start_time = '20041201'
    
    def search(self, keyword=None):
        self.reach_end = False
        print('台視新聞 search: ' + keyword)
        self.keyword = keyword
        html_text = requests.get(self.url + keyword).text
        self.soup = bs4.BeautifulSoup(html_text, 'html.parser')
        # 先找到有幾頁 一頁10筆
        page_info_selector = '.resultstats'
        self.soup.select(page_info_selector)
        page_info = self.soup.select(page_info_selector)[0].text
        total_data = int(page_info.strip().replace('總筆數','').replace('筆', '').strip())
        if (total_data % 10 == 0):
            total_page = total_data // 10  
        else:
            total_page = total_data // 10 + 1
        for page in range(1, total_page):
            self.page = page
            self.search_page(keyword, page)
            if self.reach_end:
                break
        return True

    # TODO 搜尋結果分頁
    def search_page(self, keyword, page):
        print('台視新聞 search_page: ' + keyword + '/' + str(page))
        html_text = requests.get(self.url + keyword + '?page=' + str(page)).text
        self.soup = bs4.BeautifulSoup(html_text, 'html.parser')
        news_selector = 'section.news-list.search-list.clearfix li a'
        news_list = self.soup.select(news_selector)
        for news in news_list:
            if self.reach_end:
                break
            url = news['href']
            if not self.get_news(url):
                self.reach_end = True
        return True
    
    def get_news(self, url):
        print('台視新聞 get_news: ' + url)
        url = 'https://news.ttv.com.tw' + url
        html_text = requests.get(url).text
        self.soup = bs4.BeautifulSoup(html_text, 'html.parser')
        title_selector = 'h1'
        title = self.soup.select(title_selector)[0].text.strip()
        date_selector = '.date.time'
        date = self.soup.select(date_selector)[0].text.strip()
        if self.week_limit is not None:
            if datetime.strptime(date, '%Y.%m.%d %H:%M').date() < (datetime.now() - self.week_limit).date():
                print('達到時間限制: ' + date)
                self.reach_end = True
                return False
        
        content_selector = '#newscontent > p'
        content = self.soup.select(content_selector)
        author = content[-1].text
        content = content[0:-1]
        content = '\n'.join([c.text for c in content])
        to_txt_record('Ttv', title, date, author, url, content, self.keyword)
        return True


if __name__ == '__main__':
    ttv = Ttv()
    ttv.get_news('/news/10911290002400N')
    print('Done')
    