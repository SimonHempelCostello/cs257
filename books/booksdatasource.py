#!/usr/bin/env python3
'''
    booksdatasourcetest.py
    10/2/2021

    Simon Hempel-Costello, Anders Shenholm
    Revised by Simon Hempel-Costello
'''


import csv

class Author:

    def __init__(self, surname='', given_name='', birth_year=None, death_year=None):
        self.surname = surname
        self.given_name = given_name
        self.birth_year = birth_year
        self.death_year = death_year

    def __eq__(self, other):
        ''' For simplicity, we're going to assume that no two authors have the same name. '''
        return self.surname == other.surname and self.given_name == other.given_name

    #basic string formatting for the printouts to make my life easy
    def __str__(self) -> str:
        return self.surname + "," + self.given_name + ",(" +str(self.birth_year) + "-"+ str(self.death_year) +")"

    def __repr__(self) -> str:
        return self.__str__()

    def given_name(self):
        return self.given_name

    def birth_year(self):
        return self.birth_year

    def death_year(self):
        return self.death_year

    def surname(self):
        return self.surname

class Book:

    def __init__(self, title='', publication_year=None, authors=[]):
        ''' Note that the self.authors instance variable is a list of
            references to Author objects. '''
        self.title = title
        self.publication_year = publication_year
        self.authors = authors

    def __eq__(self, other):
        ''' We're going to make the excessively simplifying assumption that
            no two books have the same title, so "same title" is the same
            thing as "same book". '''
        return self.title == other.title

    #basic string formatting for printouts to make my life easy
    def __str__(self) -> str:
        return self.title + "," + str(self.publication_year) + ",Author(s):" + str(self.authors)

    def __repr__(self) -> str:
        return self.__str__()

    def title(self):
        return self.title

    def authors(self):
        return self.authors

    def publication_year(self):
        return self.publication_year

class BooksDataSource:

    def __init__(self, books_csv_file_name):
        ''' The books CSV file format looks like this:

                title,publication_year,author_description

            For example:

                All Clear,2010,Connie Willis (1945-)
                "Right Ho, Jeeves",1934,Pelham Grenville Wodehouse (1881-1975)

            This __init__ method parses the specified CSV file and creates
            suitable instance variables for the BooksDataSource object containing
            a collection of Author objects and a collection of Book objects.
        '''
        #Read in csv file and input it into the two lists
        self.book_list = []
        self.author_list = []
        with open(books_csv_file_name) as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                #take each author entry in the csv file and parse it into a list of authors dealing with the potential for ands
                input_authors = self.parse_authors_from_csv_entry(row[2])
                for a in input_authors:
                    if(a not in self.author_list):
                        self.author_list.append(a)
                #create a book from the other two parts of the csv, and feed it the list generated from the authors
                input_book = Book(row[0],int(row[1]),input_authors)
                #add the book to the book list
                self.book_list.append(input_book)
        pass

    def parse_authors_from_csv_entry(self, input_entry):
        and_substring = ' and '
        and_offset = len(and_substring)
        author_list = []
        if and_substring in input_entry:
            pre_and_substring = input_entry[:input_entry.index(and_substring)]
            post_and_substring = input_entry[input_entry.index(and_substring) + and_offset:]
            #Now we have isolated one author in prestring, generate an author object from this string
            pre_string_author = self.author_from_string(pre_and_substring)
            author_list.append(pre_string_author)
            #Check if post string contains multiple authors, if so recursively splice it into 1, else, just add it to the list
            if(and_substring in post_and_substring):
                author_list.extend(self.parse_authors_from_csv_entry(post_and_substring))
            else:
                post_string_author = self.author_from_string(post_and_substring)
                author_list.append(post_string_author)
        else:
            input_author = self.author_from_string(input_entry)

            author_list.append(input_author)
        return author_list

    def author_from_string(self, input_string):
        #parsing based on dileneation of spaces, parenthesis and dashes
        last_name = input_string[input_string.index(" ")+1:input_string.index("(")-1]
        first_name = input_string[:input_string.index(" ")]
        birth_date = input_string[input_string.index("(")+1 : input_string.index("-")]
        death_date = input_string[input_string.index("-")+1 : input_string.index(")")]
        author  = Author(surname = last_name, given_name = first_name, birth_year = birth_date, death_year = death_date)
        return author

    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''
        #take your input text
        input_text = ''
        if(search_text!=None):
            input_text = search_text.lower()

        output_list = []
        for a in self.author_list:
            full_name = a.given_name.lower() + a.surname.lower()
            #check if the name is this full name
            if(input_text in full_name):
                output_list.append(a)

        #okay this is kinda jank, but it seems to work. We just sort the author list by given names first and, 
        #since the python sorting algorithm seems to try and maintain relative order when sorting by surname, 
        # those with a earlier given name are put first, without any real work on my part. 
        #I realize that on a O(n) level, it is probably a terrible method, and there is almost definitely some edge case where it doesn't work
        #but until then im keeping it
        output_list = sorted(output_list, key = lambda author:(author.surname, author.given_name))
        return output_list

    def books(self, search_text=None, sort_by='title'):
        ''' Returns a list of all the Book objects in this data source whose
            titles contain (case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        '''
        input_text = ''
        if(search_text!=None):
            input_text = search_text.lower()
        output_list = []
        for b in self.book_list:
            title = b.title.lower()
            if(input_text in title):
                output_list.append(b)
        #sorting books by title or by year given the tag
        if(sort_by == "year"):
            output_list = sorted(output_list, key = Book.publication_year)
        else:
            output_list = sorted(output_list, key = Book.title)
        return output_list 

    def books_between_years(self, start_year=None, end_year=None):
        ''' Returns a list of all the Book objects in this data source whose publication
            years are between start_year and end_year, inclusive. The list is sorted
            by publication year, breaking ties by title (e.g. Neverwhere 1996 should
            come before Thief of Time 1996).

            If start_year is None, then any book published before or during end_year
            should be included. If end_year is None, then any book published after or
            during start_year should be included. If both are None, then all books
            should be included.
        '''
        end_date = 1000000 #random future year
        start_date = -1000000 #random past year

        #sanitize to make sure we are getting dates, then convert to integers
        try:
            if(end_year != None):
                end_date = int(end_year)
            if(start_year != None):
                start_date = int(start_year)
        except ValueError:
            raise ValueError("Integer Numbers must be inputted as dates")
        if(start_date>end_date):
            raise ValueError("Start date must be before end date")
        output_list = []
        for b in self.book_list:
            #if its within those two dates, add it to the list
            if(b.publication_year>= start_date and b.publication_year <= end_date):
                output_list.append(b)
        output_list = sorted(output_list, key= lambda book: (book.publication_year, book.title))        
        return output_list

    def search_books_by_author(self, author):
        output_list = []
        for b in self.all_books():
            if(author in  b.authors):
                output_list.append(b.title)
        return output_list

    def all_books(self):
        return self.book_list

    def all_authors(self):
        return self.author_list

