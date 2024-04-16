import pandas as pd
class CreateDataSet:

    def __init__(self):
        self.path = '../dataset/'
        self.csv_extension = '.csv'

    def export_csv(self, filename, content) -> None:
        data = {}
        table_data = content[1:]
        try:
            print(filename)
            for item in reversed(table_data):
                period = item[0]
                value = item[1]
                year = period.split("M")[0]
                month = period.split("M")[1]
                if year not in data:
                    data[year] = {}
                data[year][month] = value

            file_path = self.path + filename + self.csv_extension
            df = pd.DataFrame(data)
            df.to_csv(file_path)
        except Exception as e:
            print(f"An error occurred: {e}")