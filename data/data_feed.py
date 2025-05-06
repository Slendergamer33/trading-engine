import pandas as pd

class HistoricCSVDataHandler:
    def __init__(self, filepath):
        self.data = pd.read_csv(filepath, parse_dates=['timestamp'])

        # 🔥 Normalize all column names to lowercase
        self.data.columns = self.data.columns.str.lower()

        self.data.set_index('timestamp', inplace=True)
        self.current_idx = 0

    def has_next(self):
        return self.current_idx < len(self.data)

    def get_next_bar(self):
        if self.has_next():
            row = self.data.iloc[self.current_idx]
            self.current_idx += 1
            return row
        return None
