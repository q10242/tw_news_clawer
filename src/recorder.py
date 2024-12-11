import os

def to_txt_record(media, title, date, author, url, content, keyword=None):

    path = f'results/{media}'
    if keyword is not None:
        path += f'/{keyword}'
    print("save to path: " + path)
    if not os.path.exists(path):
        os.makedirs(path)
    title = title.replace('/', '_')
    # 以utf-8編碼寫入檔案
    with open(f'{path}/{title}.txt', 'w', encoding='utf-8') as f:
        f.write(f'媒體名稱：{media}\n')
        f.write(f'標題：{title}\n')
        f.write(f'日期：{date}\n')
        f.write(f'記者：{author}\n')
        f.write(f'網址：{url}\n')
        f.write(f'內文：{content}\n')
        f.close()
    return True


if __name__ == '__main__':
    to_txt_record('中央社', '台灣疫情', '2021-05-15', '記者A', '疫情', 'https://www.cna.com.tw/news/aasd', '內文內容')