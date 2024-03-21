from survey_database import Server


class GroundTruth:
    def __init__(self) -> None:
        self.server = Server('http://178.16.143.126:8000/ground_truth')
        self.result = None

    def get_amount(self):
        if not self.result is None:
            return self.result

        self.server.send()
        rows = self.server.raw_result.content.decode('utf-8').splitlines()

        self.result = len(rows)

        return self.result
