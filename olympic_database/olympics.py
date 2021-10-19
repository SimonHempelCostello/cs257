'''
    booksdatasourcetest.py
    10/2/2021

    Simon Hempel-Costello, Anders Shenholm
    Revised by Simon Hempel-Costello, Anders Shenholm
'''
import argparse

class olympics():
    
    def __init__(self) -> None:
        self.namesearch_help = 'Given a NOC search string, show the names of athletes who have represented that NOC'
        self.medallist_help = 'Lists all NOCs in order of the gold medals they have won, in decreasing order of gold medals'
        self.agesearch_help = 'Given a youngest age, oldest age, or both, will search for olympians within the given ages. If a youngest age only is given, all athletes older than that will be presented, vice versa for oldest'

    def get_arguements(self):
        parser = argparse.ArgumentParser('handle olympics commands')
        subparsers = parser.add_subparsers(description = 'commands')
        NOC_name_parser = subparsers.add_parser('namesearch',help = self.titlesearch_help)
        #parsing for NOC search
        NOC_name_parser.add_argument(
            'namesearch',
            help = self.namesearch_help,
            default  = '',
            nargs='?',
        )
        #parsing for medal list
        medal_parser = subparsers.add_parser('medallist',help =self.authorsearch_help)
        medal_parser.add_argument(
            'medallist',
            help = self.medallist_help,
            default  = '',
            action='store_true'
        )
        #parsing for agesearch search
        age_search = subparsers.add_parser('age_search',help = self.datesearch_help)
        age_search.add_argument(
            'age_search',
            help = self.datesearch_help,
            default  = '',
            nargs='?',
        )
        #start date parsing
        age_search.add_argument(
            '--startage','-s',
            help = self.start_date_help,
            default = None, 

        )
        #end date parsing
        age_search.add_argument(
            '--endage','-e',
            help = self.end_date_help,
            default = None
        )
        args = parser.parse_args()
        return args

if __name__ == '__main__':
    pass