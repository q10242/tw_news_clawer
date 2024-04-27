import bs4, requests, time
from src.recorder import to_txt_record
from datetime import datetime, timedelta
class TVBS:
    keyword = None

    url = "https://news.tvbs.com.tw/news/searchresult/"
    soup = None
    reach_end = False
    week_limit = None
    def __init__(self,week_limit=None):
        if week_limit is not None:
            self.week_limit = timedelta(weeks=week_limit) # 這是一個timedelta物件

    def search(self, keyword=None):
        print('TVBS search: ' + keyword)
        self.keyword = keyword
        html_text = requests.get(self.url + keyword + '/news').text
        self.soup = bs4.BeautifulSoup(html_text, 'html.parser')

        # 每一頁總共有 body > div > main > div > article > div.news_list > div.list > ul > li 個
        # 計算數字
        newsPerPage = len(self.soup.select('body > div > main > div > article > div.news_list > div.list > ul > li'))

        totalDataInfo = self.soup.select('body > div > main > div > article > div.news_list > div.search_result > div.keyword > ul > li.t2 > div.word > h1 > span:nth-child(2)')[0].text #   結果共1,231筆
        totalDataInfo = totalDataInfo.replace('筆', '')
        totalDataInfo = totalDataInfo.replace('結果共', '')
        totalDataInfo = totalDataInfo.replace(',', '')
        totalDataInfo = int(totalDataInfo)
        last_page = int(totalDataInfo / newsPerPage) + 1
        for i in range(1, last_page + 1):
            if self.reach_end:
                break
            self.parse_page(i)
    def parse_page(self, page):
        if self.keyword is None:
            self.keyword = ''
        html_text = requests.get(self.url + self.keyword + '/news/' + str(page) ).text
        
        self.soup = bs4.BeautifulSoup(html_text, 'html.parser')
        news_selector = 'body > div > main > div > article > div.news_list > div.list > ul li > a'
        news = self.soup.select(news_selector)
        for new in news:
            try:
                self.handle_news(new['href'])
            except:
                print('error handling news: ' + new.text)
            print(new.text.strip())
    def handle_news(self, news_url):
        if news_url is None:
            return
        html_text = requests.get(news_url).text
        soup = bs4.BeautifulSoup(html_text, 'html.parser')
        title_selector = 'h1.title'
        title = soup.select(title_selector)[0].text.strip()
        content_selector = '#news_detail_div'
        content = soup.select(content_selector)
        # 去掉script標籤
        for script in content[0].find_all('script'):
            script.decompose()
        # 如果<p>中有<a>則是廣告 ，去掉這個<p>
        for p in content[0].find_all('p'):
            if p.find('a') is not None:
                p.decompose()
        # 如果div中有img 則是圖片，去掉這個div
        for div in content[0].find_all('div'):
            if div.find('img') is not None:
                div.decompose()
        classes_to_remove = ['fly_outbox', 'nolazydiv', 'guangxuan', 'lazydiv']
        for class_name in classes_to_remove:
            for div in content[0].find_all('div', class_=class_name):
                div.decompose()
        # 如果<p>的sytle 是 'font-size: 1.2em;letter-spacing: normal;line-height: 1.8;' 則是廣告，去掉這個<p>
        for p in content[0].find_all('p', style='font-size: 1.2em;letter-spacing: normal;line-height: 1.8;'):
            p.decompose()
        # 拿到所有的<p> 以及<div> 並且把他們的text串起來
        content =content[0].find(['body']).text
        contentText = content.strip()
        
        author_selector = '.author'
        time = soup.select(author_selector)[0].text.strip()
        # 用\n分開
        time = time.split('\n')[1]
        # 發佈時間：2024/04/19 13:40
        # 最後更新時間：2024/04/19 13:40
        time = time.replace('發佈時間：', '')
        time = time.replace('最後更新時間：', '\n')
        time = time.split('\n')[0].strip()
        if self.week_limit is not None:
            # 把time轉換成能比較的格式
            time = time.split(' ')
            time = time[0].replace('/', '-').replace('/', '-') + ' ' + time[1]
            time = time.strip()
            time = datetime.fromisoformat(time)
            if datetime.now() - time > self.week_limit:
                self.reach_end = True
                return
        # 移除time的空白 
        # 第一個元素是記者
        # 記者
        # 在text "攝影"之後的 不是記者
        authors = soup.select(author_selector)[0]
        if '攝影' in authors.text:
            author = authors.text.split('攝影')[0]
        author = author.replace('記者', '')
        author = author.replace('/', '')
        author = author.replace(' ', ',')
        author = author.replace(',,', '')
        author = author.strip()
        to_txt_record('TVBS', title, time, author, news_url, contentText, self.keyword)
        pass
if __name__ == '__main__':

    tvbs = TVBS(week_limit=None)
    tvbs.handle_news('https://news.tvbs.com.tw/local/2460688')