from Scraper import Scraper
from PageLoader import PageLoader
from Parser import Parser
from result_saver import ResultSaver

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
        print("スクレイピング完了！" )

if __name__ == "__main__":
    # Main クラスをインスタンス化して実行
    suumo_scraper = Main()
    suumo_scraper.run()
    