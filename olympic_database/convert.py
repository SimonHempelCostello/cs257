'''
October 13th 2021
Simon Hempel-Costello
'''
import csv
class Converter:

    def __init__(self) -> None:
        self.olympian_event_dictionary = {}
        self.event_NOC_dictionary = {}
        self.competitor_event_dictionary = {}
        pass

    def read_in(self, athlete_event_file_name, NOC_file_name):

        self.athlete_event_list = []
        self.NOC_list = []
        with open(athlete_event_file_name) as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                self.athlete_event_list.append(row)
        with open(NOC_file_name) as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                self.NOC_list.append(row)
        pass

    def write_olympians(self):
        with open('olympians.csv', 'w', encoding = 'UTF8') as file:
            writer = csv.writer(file)
            last_id = ""
            for a in self.athlete_event_list:
                id = a[0]
                full_name = a[1]
                if(" " in full_name):
                    first_name = full_name[: full_name.index(' ')]
                    last_name = full_name[full_name.index(' ') :]
                    output_row = [id , first_name,last_name]
                    if(id != last_id):
                        writer.writerow(output_row)
                        last_id = id

    def write_events(self):
        output_list = []
        with open('events.csv', 'w', encoding = 'UTF8') as file:
            writer = csv.writer(file)
            eventID = 0
            for a in self.athlete_event_list[1:]:
                for i in range(len(a)):
                    if a[i] == 'NA':
                        a[i] = 'NULL'
                id = str(a[0])
                games = a[8]
                year = a[9]
                season = a[10]
                city = a[11]
                sport = a[12]
                event = a[13]
                medal = a[14]
                sex = a[2]
                age = a[3]
                height = a[4]
                mass = a[5]
                NOC = a[7]
                output_row = [eventID , games,year, season, city, sport, event]
                writer.writerow(output_row)
                self.olympian_event_dictionary[eventID] = id
                self.event_NOC_dictionary[eventID] = NOC
                competitor = Competitor(age, sex, mass, height, NOC, medal)
                self.competitor_event_dictionary[eventID] = competitor
                eventID+=1

    def write_olympian_events(self):
        with open('olympians_events.csv', 'w', encoding = 'UTF8') as file:
            writer = csv.writer(file)
            for key in self.olympian_event_dictionary:
                athlete_id = self.olympian_event_dictionary[key]
                NOC = self.event_NOC_dictionary[key]
                eventID = key
                #athleteId = self.olympian_event_dictionary[eventID]
                #NOC = self.event_NOC_dictionary[eventID]
                output = [eventID, athlete_id, NOC]
                writer.writerow(output)
    def write_competitor_instance(self):
        with open('competitor_instance.csv', 'w', encoding = 'UTF8') as file:
            writer = csv.writer(file)
            for key in self.olympian_event_dictionary:
                athlete_id = self.olympian_event_dictionary[key]
                eventID = key
                competitor = self.competitor_event_dictionary[key]
                output = [eventID, athlete_id, competitor.sex, competitor.age, competitor.height, competitor.mass, competitor.NOC, competitor.medal]
                writer.writerow(output)
class Competitor:
    def __init__(self, age, sex, mass, height, NOC, medal) -> None:
        self.age = age
        self.sex = sex
        self.mass = mass
        self.height = height
        self.NOC = NOC
        self.medal = medal
        pass
    def age(self):
        return self.age
    def sex(self):
        return self.sex
    def mass(self):
        return self.mass
    def height(self):
        return self.height
    def NOC(self):
        return self.NOC
    def medal(self):
        return self.medal

if __name__ == "__main__":             
    c = Converter()
    c.read_in("athlete_events.csv", "noc_regions.csv")
    c.write_olympians()
    c.write_events()
    c.write_olympian_events()
    c.write_competitor_instance()


