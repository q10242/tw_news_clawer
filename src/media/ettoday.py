import bs4, requests, time
from recorder import to_txt_record
class EtToday:
    keyword = None

    url = "https://www.ettoday.net/news_search/doSearch.php?search_term_string="
    soup = None

    def search(self, keyword=None):
        print('ETtoday search: ' + keyword)
        self.keyword = keyword
        html_text = requests.get(self.url + keyword).text
        self.soup = bs4.BeautifulSoup(html_text, 'html.parser')
        page_info_selector = '#result-list > div.page_nav > div > p'
        page_info = self.soup.select(page_info_selector)[0].text

        # 範例 第1頁 | 共1000頁
        last_page = int(page_info.split('|')[1].split('共')[1].replace('頁', ''))
        for i in range(1, last_page + 1):
            self.parse_page(i)
    def parse_page(self, page):
        if self.keyword is None:
            self.keyword = ''
        html_text = requests.get(self.url + self.keyword + f'&page={page}').text
        self.soup = bs4.BeautifulSoup(html_text, 'html.parser')
        news_selector = '#result-list h2 a'
        news = self.soup.select(news_selector)
        for new in news:
            try:
                self.handle_news(new['href'])
            except:
                print('error handling news: ' + new.text)
            print(new.text)
    def handle_news(self, news_url):
        if news_url is None:
            return
        html_text = requests.get(news_url).text
        soup = bs4.BeautifulSoup(html_text, 'html.parser')
        title_selector = 'h1.title'
        content_selector = 'div.story p'
        time_selector = 'time.date'
        title = soup.select(title_selector)[0].text.strip()
        content = soup.select(content_selector)
        time = soup.select(time_selector)[0].text.strip()
        # 移除time的空白 
        time = time.strip()
        contentText = ''
        # 第一個元素是記者
        author = ''
        
        for c in content:
            if c.text == '':
                continue
            # 如果 c.text 是 ►、●、▲ 這三個符號開頭的話，就不要印出來
            if c.text.startswith('►') or c.text.startswith('●') or c.text.startswith('▲'):
                continue
            if author == '':
                author = c.text
            contentText += c.text + '\n'
        contentText = contentText.strip()
        to_txt_record('ETtoday', title, time, author, news_url, contentText, self.keyword)
        pass


if __name__ == '__main__':
    et = EtToday()
    et.handle_news('https://www.ettoday.net/news/20210515/1970006.htm')