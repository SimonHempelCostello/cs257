'''
    booksdatasourcetest.py
    10/2/2021

    Simon Hempel-Costello, Anders Shenholm
    Revised by Simon Hempel-Costello, Anders Shenholm
'''
import booksdatasource
import sys
import argparse
import sys

class BooksSearch:

    def __init__(self, file_string):
        self.data_source = booksdatasource.BooksDataSource(file_string)

    def titlesearch_return(self, arguments):
        #if -y is called, sort by date, otherwise sort by title
        if(arguments.y):
            book_list =  self.data_source.books(arguments.titlesearch, sort_by='year')
        else:
            book_list =  (self.data_source.books(arguments.titlesearch))
        return self.return_list(book_list, post_text= '\n')

    def authorsearch_return(self, arguments):
        #Print out the authors and the books they wrote
        author_list = self.data_source.authors(arguments.authorsearch)
        output_string = ''
        for a in author_list:
            output_string+= str(a) + ', Books Written:' + str(self.data_source.search_books_by_author(a)) + '\n'
        return output_string

    def datesearch_return(self, arguments):
        #Print out the books between the given years
        return self.return_list(self.data_source.books_between_years(arguments.startdate, arguments.enddate), post_text='\n')

    def return_list(self,in_list, pre_text = '', post_text = '' ):
        output_string= ''
        for a in in_list:
            output_string += (str(pre_text) + str(a) + str(post_text))
        return output_string

class BooksCommandLineInterface():
    
    def __init__(self) -> None:
        self.titlesearch_help = 'Given a search string S, print a list of books whose titles contain S (case-insensitive). Books may be sorted by title (by default) or by publication year.'
        self.date_sort_help = 'sort books by year instead of title'
        self.authorsearch_help = 'Given a search string S, print a list of authors whose names contain S (case-insensitive), for each author, print their books'
        self.datesearch_help = 'Given a range of years A to B, print a list of books published between years A and B. If a start date is not given, it searches for books that are before the end date, and if an end date is not given, then it searches for books after the start date.If neither are given, all books will be published in increasing order of date'
        self.start_date_help = 'date to start the list with'
        self.end_date_help = 'date to end the list with'

    def get_arguements(self):
        parser = argparse.ArgumentParser('handle books commands')
        subparsers = parser.add_subparsers(description = 'commands')
        #Break parsing into 3 subparsers for explicity in code definition
        title_parser = subparsers.add_parser('titlesearch',help = self.titlesearch_help)
        title_parser.add_argument(
            'titlesearch',
            help = self.titlesearch_help,
            default  = '',
            nargs='?',
        )
        #call for date sort
        title_parser.add_argument(
            '-y',
            help = self.date_sort_help,
            default  = '',
            action='store_true'
        )
        #parsing for author search
        author_parser = subparsers.add_parser('authorsearch',help =self.authorsearch_help)
        author_parser.add_argument(
            'authorsearch',
            #sorry for inconsistency here with the "" vs ', I wanted to show posession and didn't want to deal with the symbol stuff for python
            help = self.authorsearch_help,
            default  = '',
            nargs='?',
        )
        #parsing for date search
        date_search = subparsers.add_parser('datesearch',help = self.datesearch_help)
        date_search.add_argument(
            'datesearch',
            help = self.datesearch_help,
            default  = '',
            nargs='?',
        )
        #start date parsing
        date_search.add_argument(
            '--startdate','-s',
            help = self.start_date_help,
            default = None, 

        )
        #end date parsing
        date_search.add_argument(
            '--enddate','-e',
            help = self.end_date_help,
            default = None
        )
        args = parser.parse_args()
        return args

if __name__ == '__main__':
    book_interface = BooksCommandLineInterface()
    arguments = book_interface.get_arguements()
    book_search = BooksSearch('books1.csv')
    output = ''
    if('titlesearch' in arguments):
        output = book_search.titlesearch_return(arguments)
    elif('authorsearch' in arguments ):
        output = book_search.authorsearch_return(arguments)
    elif('datesearch' in arguments):
        output = book_search.datesearch_return(arguments)
    else:
        raise ValueError('some command must be inputted, please enter one of (titlsearch, datesearch, authorsearch, --help) to continue')
    print(output)
