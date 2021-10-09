'''
    booksdatasourcetest.py
    10/2/2021

    Simon Hempel-Costello, Anders Shenholm
    Revised by Simon Hempel-Costello

'''

import booksdatasource
import unittest

class BooksDataSourceTester(unittest.TestCase):
    def setUp(self):
        self.data_source = booksdatasource.BooksDataSource('books1.csv')

    def tearDown(self):
        pass

    def test_unique_author_len(self):
        authors = self.data_source.authors('Pratchett')
        self.assertTrue(len(authors) == 1)

    def test_unique_author_name(self):
        authors = self.data_source.authors('Pratchett')
        self.assertTrue(authors[0] == booksdatasource.Author('Pratchett', 'Terry'))

    def test_unique_title_single_author_len(self):
        books = self.data_source.books('Blackout')
        self.assertTrue(len(books)== 1)

    def test_unique_title_single_author_name(self):
        books = self.data_source.books('Blackout')
        author_name = 'Connie Willis'
        author = booksdatasource.Author('Pratchett', 'Terry')
        author_list = [author]
        self.assertTrue(books[0] == booksdatasource.Book('Blackout',2010,author_list))

    def test_unique_title_multiple_author_len(self):
        books = self.data_source.books('Good Omens')
        self.assertTrue(len(books)==1)

    def test_unique_title_multiple_author_names(self):
        books = self.data_source.books('Good Omens')
        author_neil = booksdatasource.Author('Gaiman', 'Neil')
        author_pratchett = booksdatasource.Author('Pratchett','Terry')
        author_list = [author_neil, author_pratchett]
        self.assertTrue(books[0] == booksdatasource.Book('Good Omens', 1990, author_list))

    def test_null_title_entry(self):
        books = self.data_source.books('')
        books = sorted(books, key = booksdatasource.Book.title)
        all_books  = sorted(self.data_source.all_books(), key  = booksdatasource.Book.title)
        self.assertTrue( books == all_books)

    def test_null_author_entry(self):
        authors = self.data_source.authors('')
        authors = sorted(authors, key = booksdatasource.Author.given_name)
        authors = sorted(authors, key = booksdatasource.Author.surname)
        all_authors  = sorted(self.data_source.all_authors(), key  = booksdatasource.Author.given_name)
        all_authors  = sorted(all_authors, key  = booksdatasource.Author.surname)
        self.assertTrue( authors == all_authors)

    def test_null_date_entry(self):
        books = self.data_source.books_between_years()
        books = sorted(books, key = booksdatasource.Book.title)
        all_books  = sorted(self.data_source.all_books(), key  = booksdatasource.Book.title)
        self.assertTrue( books == all_books)

    def test_non_unique_title_len(self):
        books = self.data_source.books('Street')
        self.assertTrue(len(books)==2)

    def test_non_unique_title_names_alphabetical(self):
        books = self.data_source.books('Street', 'title')
        author_lewis = booksdatasource.Author('Lewis', 'Sinclair')
        author_baldwin = booksdatasource.Author('Baldwin','James')
        author_list_main_street = [author_lewis]
        author_list_beale = [author_baldwin]
        self.assertTrue((books[0]  == booksdatasource.Book('If Beale Street Could Talk', 1974, author_list_beale)) and (books[1] == booksdatasource.Book('Main Street', 1920, author_list_main_street)))

    def test_non_unique_title_names_chronological(self):
        books = self.data_source.books('street', 'year')
        author_lewis = booksdatasource.Author('Lewis', 'Sinclair')
        author_baldwin = booksdatasource.Author('Baldwin','James')
        author_list_main_street = [author_lewis]
        author_list_beale = [author_baldwin]
        self.assertTrue((books[1]  == booksdatasource.Book('If Beale Street Could Talk', 1974, author_list_beale)) and (books[0] == booksdatasource.Book('Main Street', 1920, author_list_main_street)))

    def test_non_unique_author_len(self):
        authors = self.data_source.authors('Brontë')
        self.assertTrue(len(authors) == 3)

    def test_non_unique_author_name(self):
        authors = self.data_source.authors('Brontë')
        self.assertTrue(authors[0] == booksdatasource.Author('Brontë', 'Ann')and authors[1] == booksdatasource.Author('Brontë', 'Charlotte') and authors[2] ==booksdatasource.Author('Brontë', 'Emily'))

    def test_date_return_unique_len(self):
        books = self.data_source.books_between_years(1848, 1849)
        self.assertTrue(len(books) == 1)

    def test_date_return_unique_name(self):
        books = self.data_source.books_between_years(1848, 1849)
        author = booksdatasource.Author('Bronte', 'Ann')
        author_list = [author]
        self.assertTrue(books[0] == booksdatasource.Book('The Tenant of Wildfell Hall',1848,author_list))

    def test_date_return_non_unique_name(self):
        books = self.data_source.books_between_years(2020, None)
        author_schwab = booksdatasource.Author('Schwab', 'V.E.')
        author_list_schwab = [author_schwab]
        author_orenstein = booksdatasource.Author('Orenstein', 'Peggy')
        author_list_orenstein = [author_orenstein]
        self.assertTrue(books[0] == booksdatasource.Book('Boys and Sex',2020,author_list_orenstein) and books[1] ==booksdatasource.Book('The Invisible Life of Addie LaRue',2020,author_list_schwab))

    def test_bad_date_input(self):
        self.assertRaises(ValueError, self.data_source.books_between_years, "asdfadsadfs")

    def test_reversed_dates(self):
        self.assertRaises(ValueError, self.data_source.books_between_years,start_year=2021, end_year = 1900)

if __name__ == '__main__':
    unittest.main()

