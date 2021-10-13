import csv
class Converter:
    def __init__(self) -> None:
        pass
    def read_in(self, athlete_event_file_name, NOC_file_name):

        self.athlete_event_list = []
        self.NOC_list = []
        with open(athlete_event_file_name) as file:
            self.athlete_event_list = csv.reader(file)
        with open(NOC_file_name) as file:
            self.NOC_list = csv.reader(file)
        pass