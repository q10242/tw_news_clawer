import bs4, requests, time
from src.recorder import to_txt_record
from datetime import datetime, timedelta
import re
import httpx
# 民視新聞
class FtvNews:
    keyword = None
    url = "https://www.ftvnews.com.tw/search/"
    soup = None
    reach_end = False
    week_limit = None
    page=1     
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Referer': 'https://example.com',
    }
    
    def __init__(self, week_limit=None):
        self.week_limit = week_limit

    def search(self, keyword=None):
        self.keyword = keyword
        session = requests.Session()
        with httpx.Client(headers=self.headers) as client:
            response = client.get(self.url + keyword +'/'+ str(self.page))
        if response.status_code == 200:
            self.soup = bs4.BeautifulSoup(response.text, 'html.parser')
        else:
            print('Request failed: ' + str(response.status_code))
            return  
        page_info_selector = '.pagiNum'
        page_info = self.soup.select(page_info_selector)
        match = re.search(r"/(\d+)", page_info[0].text)
        if match:
            total_pages = match.group(1)
        else:
            print("無法找到頁數")
            return
        for i in range(1, int(total_pages)+1):
            time.sleep(5)
            if self.reach_end:
                break
            self.parse_page(i)


    def parse_page(self, page):
        if self.keyword is None:
            self.keyword = ''
        html_text = requests.get(self.url + self.keyword + '/' + str(page)).text
        with httpx.Client(headers=self.headers) as client:
            response = client.get(self.url + self.keyword + '/' + str(page))
        if response.status_code == 200:
            self.soup = bs4.BeautifulSoup(response.text, 'html.parser')
        elif response.status_code == 429:
            # try again
            time.sleep(600)
            return self.parse_page(page)
        else:
            print('Request failed: ' + str(response.status_code))
            return    
        news_url_selector = '.clearfix a'
        news_url = self.soup.select(news_url_selector)
        for url in news_url:
            time.sleep(5)
            if self.reach_end:
                break
            if url['href'] == 'javascript:void(0)':
                continue
            self.parse_news(url['href'])

    
    def parse_news(self, url):
        
        base_url = 'https://www.ftvnews.com.tw'
        news_url = base_url + url
        with httpx.Client(headers=self.headers) as client:
            response = client.get(news_url)
        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
        elif response.status_code == 429:
            # try again
            time.sleep(600)
            return self.parse_news(url)
        
        title_selector = 'div.col-article.position-relative > div.scroll-header > h1'
        title = soup.select(title_selector)[0].text.strip()
        author_selector = '#preface'
        author = soup.select(author_selector)[0].text.strip().split('報導')[0] + '報導'
        first_text = soup.select(author_selector)[0].text.strip().split('報導')[1]
        content = soup.select('#newscontent p')
        for p in content:
            if '' in p.text.strip():
                content.remove(p)
        content_text = '\n'.join([p.text for p in content])
        content_text = first_text + '\n'+ content_text
        time_selector = '.date'
            
        time = soup.select(time_selector)
        # 如果發布時間已經超過週數限制，則設定self.reach_end為True
        # 發佈時間字串範例:  '發佈時間：2024/10/06 13:00'
        publish_time = time[0].text.strip().split('：')[1]
        publish_time = datetime.strptime(publish_time, '%Y/%m/%d %H:%M')
        if self.week_limit is not None:
            if datetime.now() - publish_time > timedelta(weeks=self.week_limit):
                self.reach_end = True
                return
        time = time[0].text.strip() + ' ' + time[1].text.strip()
        to_txt_record('FtvNews', title, time, author, news_url, content_text, self.keyword)

        

        
        

if __name__ == '__main__':
    ftvnews = FtvNews()
    ftvnews.parse_news('/news/detail/2024A06S04M1')
    print('Done')