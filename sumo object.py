pip install requests
import requests
pip install retry==0.9.2

from bs4 import BeautifulSoup
from retry import retry
import urllib
import time
import numpy as np

data_samples = []

class Scraper:
    def __init__(self, loader, parser, saver, max_page=200):
        self.loader = loader
        self.parser = parser
        self.saver = saver
        self.max_page = max_page
        self.data_samples = []
        self.times = []
        self.start_time = time.time()

    def scrape_page(self, page):
        """1ページ分のスクレイピング"""
        soup = self.loader.load_page(page)
        page_data = self.parser.parse_page(soup)
        self.data_samples.extend(page_data)

    def run(self):
        """全ページのスクレイピングを実行"""
        for page in range(1, self.max_page + 1):
            print(f"{page}ページ目を処理中...")
            before = time.time()

            # ページをスクレイピング
            self.scrape_page(page)

            # 進捗表示
            after = time.time()
            running_time = after - before
            self.times.append(running_time)
            print(f'{page}ページ目：{running_time:.2f}秒')
            print(f'総取得件数：{len(self.data_samples)}')

            # 残り時間予測
            running_mean = np.mean(self.times)
            remaining_time = running_mean * (self.max_page - page)
            hour, rem = divmod(remaining_time, 3600)
            minute, second = divmod(rem, 60)
            print(f'残り時間：{int(hour)}時間{int(minute)}分{int(second)}秒\n')

            time.sleep(1)  # サーバ負荷軽減

        # データを保存
        self.saver.save(self.data_samples)
        print(f"スクレイピング完了！総件数：{len(self.data_samples)}")

class PageLoader:
    def __init__(self, base_url):
        self.base_url = base_url

    @retry(tries=3, delay=10, backoff=2)
    def load_page(self, page):
        """ページを読み込んでBeautifulSoupオブジェクトを返す"""
        url = self.base_url.format(page)
        response = requests.get(url)
        response.raise_for_status()  # HTTPエラーをチェック
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

class Parser:
    def parse_page(self, soup):
        """1ページ分のデータをパース"""
        data_samples = []
        buildings = soup.find_all(class_='cassetteitem')
        for building in buildings:
            data_home = self.parse_building(building)
            rooms = building.find(class_='cassetteitem_other')
            data_samples.extend(self.parse_rooms(rooms, data_home))
        return data_samples

    def parse_building(self, building):
        """建物データをパース"""
        data_home = []
        data_home.append(building.find(class_='cassetteitem_content-title').text)  # 建物名
        data_home.append(building.find(class_='cassetteitem_detail-col1').text)  # 住所

        # 最寄り駅の情報を取得
        stations = building.find(class_='cassetteitem_detail-col2')
        for station in stations.find_all(class_='cassetteitem_detail-text'):
            data_home.append(station.text)

        # 築年数と階数
        details = building.find(class_='cassetteitem_detail-col3')
        for detail in details.find_all('div'):
            data_home.append(detail.text)

        return data_home

    def parse_rooms(self, rooms, data_home):
        """部屋データをパース"""
        data_samples = []
        for room in rooms.find_all(class_='js-cassette_link'):
            data_room = []

            # 部屋情報を探索
            for idx, grandchild in enumerate(room.find_all('td')):
                if idx == 2:  # 階
                    data_room.append(grandchild.text.strip())
                elif idx == 3:  # 家賃と管理費
                    data_room.append(grandchild.find(class_='cassetteitem_other-emphasis ui-text--bold').text)
                    data_room.append(grandchild.find(class_='cassetteitem_price cassetteitem_price--administration').text)
                elif idx == 4:  # 敷金と礼金
                    data_room.append(grandchild.find(class_='cassetteitem_price cassetteitem_price--deposit').text)
                    data_room.append(grandchild.find(class_='cassetteitem_price cassetteitem_price--gratuity').text)
                elif idx == 5:  # 間取りと面積
                    data_room.append(grandchild.find(class_='cassetteitem_madori').text)
                    data_room.append(grandchild.find(class_='cassetteitem_menseki').text)
                elif idx == 8:  # URL
                    rel_url = grandchild.find(class_='js-cassette_link_href cassetteitem_other-linktext').get('href')
                    data_room.append(rel_url)

            # 建物データと結合
            data_samples.append(data_home + data_room)

        return data_samples

class ResultSaver:
    def __init__(self, filename):
        self.filename = filename

    def save(self, data_samples):
        """データをCSVに保存"""
        df = pd.DataFrame(data_samples)
        df.to_csv(self.filename, index=False)
        print(f"データを {self.filename} に保存しました！")

class Main:
    def __init__(self, base_url='https://suumo.jp/jj/chintai/ichiran/FR301FC001/?page={}', max_page=200, output_file='results.csv'):
        self.base_url = base_url
        self.max_page = max_page
        self.output_file = output_file
        
        self.loader = PageLoader(self.base_url)
        self.parser = Parser()
        self.saver = ResultSaver(self.output_file)
        self.scraper = Scraper(self.loader, self.parser, self.saver, max_page=self.max_page)
    
    def run(self):
        self.scraper.run()
        print("スクレイピング完了！")

if __name__ == "__main__":
    suumo_scraper = SuumoScraper()
    suumo_scraper.run()

