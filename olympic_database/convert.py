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
        self.games_list =[]
        self.event_list = []
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
            gameID = 0
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
                competitor = Competitor(age, sex, mass, height, NOC, medal)
                game = Game(year, season, city, games)
                self.olympian_event_dictionary[eventID] = id
                self.event_NOC_dictionary[eventID] = NOC
                self.competitor_event_dictionary[eventID] = competitor
                if(game not in self.games_list):
                    self.games_list.append(game)
                output_row = [eventID,self.games_list.index(game),sport, event]
                writer.writerow(output_row)

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
                sex = competitor.sex
                age = competitor.age
                height = competitor.height
                mass = competitor.mass
                NOC = competitor.NOC
                medal = competitor.medal
                output = [eventID, athlete_id, sex, age, height, mass, NOC, medal]
                writer.writerow(output)
    def write_games(self):
        with open('games.csv', 'w', encoding = 'UTF8') as file:
            writer = csv.writer(file)
            for game in self.games_list:
                year = game.year
                season = game.season
                city = game.city
                title = game.title
                output = [self.games_list.index(game),year, season, city, title]
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
class Game():
    def __init__(self, year, season, city, title):
        self.year = year
        self.season = season
        self.city = city
        self.title = title
    def year(self):
        return self.year
    def season(self):
        return self.season
    def city(self):
        return self.city
    def title(self):
        return self.title
    def __str__(self):
        return self.title
    def __repr__(self):
        return self.title
    def __eq__(self, other):
        return (self.title == other.title and self.city == other.city)

if __name__ == "__main__":             
    c = Converter()
    c.read_in("athlete_events.csv", "noc_regions.csv")
    c.write_olympians()
    c.write_events()
    c.write_olympian_events()
    c.write_competitor_instance()
    c.write_games()


