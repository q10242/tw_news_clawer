import bs4, requests, time
from src.recorder import to_txt_record
from datetime import datetime, timedelta
import re

# 自由時報
class LTN:
    keyword = None
    url = "https://search.ltn.com.tw/list?keyword="
    
    conditions = "&sort=date&type=all&page="
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
        self.conditions = '&start_time=' + start_time + '&end_time=' + end_time + self.conditions
    
    def search(self, keyword=None):
        print('自由時報 search: ' + keyword)
        self.keyword = keyword
        html_text = requests.get(self.url + keyword + self.conditions + str(self.page)).text
        self.soup = bs4.BeautifulSoup(html_text, 'html.parser')

        page_info_selector = '.mark'
        if( self.soup.select(page_info_selector) != []):
            page_info = self.soup.select(page_info_selector)[0].text
            match = re.search(r'\d+', page_info)
            if match:
                records = int(match.group())
            else: 
                return
            # 每一頁有20筆資料  如果沒除盡就+1
            last_page = records // 20
            if records % 20 != 0:
                last_page += 1
            for i in range(1, last_page + 1):
                if self.reach_end:
                    break
                self.parse_page(i)
        
    def parse_page(self, page):
        if self.keyword is None:
            self.keyword = ''
        html_text = requests.get(self.url + self.keyword + self.conditions + str(page)).text
        self.soup = bs4.BeautifulSoup(html_text, 'html.parser')
        class_name = '.cont'
        news_url_list = self.soup.select(class_name) # 每一個的href屬性
        for news_url in news_url_list:
            # 略過財經和地產新聞以及娛樂新聞
            # 如果是是https://estate 開頭或者 https://ec 開頭
            if news_url.a['href'].startswith('https://estate') or news_url.a['href'].startswith('https://ec') or  news_url.a['href'].startswith('https://ent'):
                continue

            try:
                self.handle_news(news_url.a['href'])
            except:
                print('error handling news: ' + news_url.text)
    
    def handle_news(self, news_url):
        html_text = requests.get(news_url).text
        soup = bs4.BeautifulSoup(html_text, 'html.parser')

        title_selector = 'h1'
        title = soup.select(title_selector)[0].text.strip()
        time = soup.select('.time')[0].text.strip()
        content_selector = '.text.boxTitle.boxText > p'
        content = soup.select(content_selector)
        filtered_content = [p for p in content if not p.get('class')]

        first_p_text = filtered_content[0].text if filtered_content else ""
        match = re.search(r'〔(.*?)〕', first_p_text)
        author = match.group(1) if match else ""

 
        if filtered_content:
            first_p_text = filtered_content[0].text
            first_p_text = re.sub(r'.*〕', '', first_p_text)
            filtered_content[0].string = first_p_text
        # 過濾掉空白的p標籤
        for p in filtered_content:
            if p.text == '':
                filtered_content.remove(p)
            # 如果有包含☆的話就移除
            if '☆' in p.text:
                filtered_content.remove(p)
        content_text = '\n'.join(p.text for p in filtered_content)
        if content_text == '':
            return
        to_txt_record('ltn', title, time, author, news_url, content_text, self.keyword)

if __name__ == '__main__':
    ltn = ltn()
    ltn.handle_news('https://news.ltn.com.tw/news/society/breakingnews/4857742')
    print('Done')