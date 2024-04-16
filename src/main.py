
from media.ettoday import EtToday


def main():

    keywords = [
        '新北市板橋',
        '新北市三重',
        '新北市中和',
        '新北市永和',
        '新北市新莊',
        '新北市新店',
        '新北市土城',
        '新北市蘆洲',
        '新北市樹林',
        '新北市汐止',
        '新北市鶯歌',
        '新北市三峽',
        '新北市淡水',
        '新北市瑞芳',
        '新北市五股',
        '新北市泰山',
        '新北市林口',
        '新北市深坑',
        '新北市石碇',
        '新北市坪林',
        '新北市三芝',
        '新北市石門',
        '新北市八里',
        '新北市平溪',
        '新北市雙溪',
        '新北市貢寮',
        '新北市金山',
        '新北市萬里',
        '新北市烏來',
    ]
    ettoday = EtToday()
    for keyword in keywords:
        ettoday.search(keyword)

if __name__ == '__main__':
    main()