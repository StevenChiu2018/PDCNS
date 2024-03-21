import os
from survey_database.server import Server


class Disease:
    def __init__(self, filename: str, num: int) -> None:
        self.server = Server('http://178.16.143.126:8000/get_samples')
        self.filename: str = filename
        self.num: int = num
        self.result = None

    def retrieve_data(self):
        if not os.path.exists(self.filename):
            self.write_to_file()

        f = open(file=self.filename, mode='r')
        statistical = {}
        num = self.num

        while num > 0:
            row = f.readline()
            disease = row.split(',')[0]

            if disease in statistical:
                statistical[disease] += 1
            else:
                statistical[disease] = 1

            print('Left ' + str(num) + ' records to be read', end='\r')

            num -= 1

        return statistical

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
