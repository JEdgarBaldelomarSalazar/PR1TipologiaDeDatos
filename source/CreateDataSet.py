import pandas as pd
class CreateDataSet:

    def __init__(self):
        self.path = '../dataset/'

    def export_csv(self, filename, content) -> None:
        data = {}
        try:
            print(filename)
            for item in content:
                print(item)
                """year = key.split("M")[0]
                month = key.split("M")[1]
                if year not in data:
                    data[year] = {}

                data[year][month] = item
            file_path = self.path + filename + ".csv"

            df = pd.DataFrame(data)
            df = df.transpose()
            df.to_csv(file_path)"""

        except Exception as e:
            print(f"An error occurred: {e}")