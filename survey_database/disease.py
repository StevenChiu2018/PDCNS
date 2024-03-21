import os
from survey_database.server import Server


class Disease:
    def __init__(self, filename: str, num: int) -> None:
        self.server = Server('http://178.16.143.126:8000/get_samples')
        self.filename: str = filename
        self.num: int = num
        self.rows = None

    def retrieve_disease_statistical(self):
        rows = self.retrieve_rows()
        statistical = {}
        num = self.num
        row_count = 0

        while num > 0:
            row = rows[row_count]
            disease = row.split(',')[0]

            if disease in statistical:
                statistical[disease] += 1
            else:
                statistical[disease] = 1

            print('Left ' + str(num) + ' records to be read', end='\r')

            num -= 1
            row_count += 1

        return statistical

    def retrieve_rows(self):
        if not self.rows is None:
            return self.rows

        if not os.path.exists(self.filename):
            self.write_to_file()
        else:
            f = open(file=self.filename, mode='r')

            self.rows = []
            for row in f:
                self.rows.append(row[:-1])

        return self.rows

    def write_to_file(self):
        f = open(file=self.filename, mode='w')
        num = self.num
        self.rows = []

        while num > 0:
            cur_num = min(num, 1000)
            self.server.send({'num_samples': cur_num})
            rows = self.server.raw_result.content.decode('utf-8').splitlines()
            self.rows.extend(rows)
            for i in range(1, len(rows)):
                f.writelines(rows[i] + '\n')

            print('Left ' + str(num) + ' records to be collected', end='\r')

            num -= cur_num

        print(self.rows)
        f.close()
