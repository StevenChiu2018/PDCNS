import requests
import csv


class Server:
    def __init__(self, url: str) -> None:
        self.url: str = url
        self.raw_result = None
        self.csv_row_list = None

    def send(self, params={}):
        self.csv_row_list = None
        self.raw_result = requests.get(url=self.url, params=params)

    def extract_csv_row_list(self):
        if not self.csv_row_list is None:
            return self.csv_row_list

        raw_data = self.raw_result.content.decode('utf-8')
        self.csv_row_list = list(csv.reader(
            raw_data.splitlines(), delimiter=','))

        return self.csv_row_list


if __name__ == '__main__':
    server = Server(url='http://178.16.143.126:8000/get_samples')

    server.send({'num_samples': 100})

    print(server.extract_csv_row_list())
