import pandas as pd

class ResultSaver:
    def __init__(self, filename):
        self.filename = filename

    def save(self, data_samples):
        """データをCSVに保存"""
        df = pd.DataFrame(data_samples)
        df.to_csv(self.filename, index=False)
        print(f"データを {self.filename} に保存しました！")