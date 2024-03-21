import os
from survey_database.server import Server


class Disease:
    def __init__(self, url: str, filename: str, num) -> None:
        self.server = Server(url)
        self.filename: str = filename
        self.num: int = num
        self.statistical = None

    def retrieve_row(self):
        if not os.path.exists(self.filename):
            self.write_to_file()

        f = open(file=self.filename, mode='r')
        rows = []
        num = self.num

        while num > 0:
            row = f.readline()
            disease = row.split(',')[0]

            rows.append(disease)

            num -= 1

        return rows

    def retrieve_data(self):
        if not os.path.exists(self.filename):
            self.statistical = None
            self.write_to_file()

        if not self.statistical is None:
            return self.statistical

        f = open(file=self.filename, mode='r')
        self.statistical = {}
        num = self.num

        while num > 0:
            row = f.readline()
            disease = row.split(',')[0]

            if disease in self.statistical:
                self.statistical[disease] += 1
            else:
                self.statistical[disease] = 1

            print('Left ' + str(num) + ' records to be read', end='\r')

            num -= 1

        return self.statistical

    def write_to_file(self):
        f = open(file=self.filename, mode='w')
        num = self.num

        while num > 0:
            cur_num = min(num, 1000)
            self.server.send({'num_samples': cur_num})
            rows = self.server.raw_result.content.decode('utf-8').splitlines()
            for i in range(1, len(rows)):
                f.writelines(rows[i] + '\n')

            print('Left ' + str(num) + ' records to be collected', end='\r')

            num -= cur_num

        f.close()
