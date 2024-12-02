import time
import numpy as np

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