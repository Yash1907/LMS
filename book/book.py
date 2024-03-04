import json
import utils.persistentStore as pStore
import random
import csv
import os
ps = pStore.PersistentStore()
class Book:
    def __init__(self, title='', author='', isbn='', quantity='', year=''):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.quantity = quantity
        self.year = year

    def update_quantity(isbn, checkOutFlag):
        bookStr = ps.get('Book',isbn)
        if (bookStr != ''):
          book = (json.loads(bookStr))
          if(checkOutFlag == True):
              book['quantity'] = int(book['quantity']) - 1
          else:
              book['quantity'] = int(book['quantity']) + 1
          ps.update("Book",book['isbn'],json.dumps(book))

    def display_details(isbn):
        bookStr = ps.get('Book',isbn)
        if(bookStr != ''):
          book = json.loads(bookStr)
          print(f"Title: {book['title']}")
          print(f"Author: {book['author']}")
          print(f"ISBN: {book['isbn']}")
          print(f"Year: {book['year']}")
          print(f"Quantity: {book['quantity']}")
        else:
           print("That book does not exist !")
    
    def add():
        book = Book()
        book.getUserInput()
        existingBookStr = ps.get('Book',book.isbn)
        if existingBookStr != '':
            existingBook = json.loads(existingBookStr)
            book['quantity'] += existingBook['quantity']
            ps.update("Book",book.isbn,json.dumps(book.__dict__))
        else:
            ps.create("Book",book.isbn,json.dumps(book.__dict__))

    def update():
        book = Book()
        book.getUserInput()
        if ps.get('Book',book.isbn) != '':
            ps.update('Book',book.isbn,json.dumps(book.__dict__))
        else:
            print("Cannot update as the book does not exist!")

    def delete(isbn):
        if ps.get('Book',isbn) != '':
            ps.delete("Book",isbn)
        else:
            print("Cannot delete as that book does not exist!")

    def getUserInput(self, forDelete=False):
        while(self.isbn.strip() == ""):
          self.isbn = input("Enter ISBN: ")
        if(forDelete):
           return
        while(self.title.strip() == ""):          
          self.title = input("Enter Book Title: ")
        while(self.author.strip() == ""):          
          self.author = input("Enter Author Name(s): ")
        while(self.year.strip() == ""):
          self.year = input("Enter Publish Year (YYYY): ")
        while(self.quantity.strip() == ""):
          self.quantity = input("Enter Book Quantity: ")
    
    def loadBooks():
        f = open("book_list.csv")
        book = Book()
        for lineArry in csv.reader(f):
            #lineArry = line.split('",')
            book.isbn = lineArry[4]
            book.title = lineArry[1]
            book.author = lineArry[2]
            book.year = lineArry[8].split('-')
            year = 0
            if len(book.year) == 2:
              if(book.year[1].isnumeric() == True):
                  year = int(book.year[1])
              else:
                  if(book.year[0].isnumeric() == True):
                    year = int(book.year[0])
              if(year < 24):
                  year = year + 2000
              else:
                  year = year + 1900
            book.quantity = random.randrange(1,10)
            book.year = year
            ps.create('Book',book.isbn, json.dumps(book.__dict__))
    
    def search(searchStr):
      bookStrList = ps.getAll('Book')
      resultList = []
      for bookStr in bookStrList:
        if(bookStr.lower().find(searchStr.lower()) != -1):
          resultList.append(json.loads(bookStr))
      return resultList
    
    def displayList(list):
        count = 0
        print("%10s %4s %2s %20s %50s" % ("ISBN","Year","Qty","Author","Title"))
        for book in list:
            print("%10s %4s %2s %24s %60s" % (book['isbn'],book['year'],book['quantity'],book['author'],book['title']))
            count = count+1
            if(count % 10 == 0):
                input("Enter for next page")
                os.system('cls' if os.name == 'nt' else 'clear')
                print("%10s %4s %2s %20s %50s" % ("ISBN","Year","Qty","Author","Title"))
