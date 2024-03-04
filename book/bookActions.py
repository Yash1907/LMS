import os
from book.book import Book

class BookActions:
  def booksMenu(gContext):
      os.system('cls' if os.name == 'nt' else 'clear')
      print("\nBooks Menu:")
      if(gContext.userRole == 'LIBRARIAN'):
        print("1. Add Book")
        print("2. Update Book")
        print("3. Delete Book")
      print("4. Search Book")
      print("5. Display Book")
      print("6. Back to Main Menu")
      option = input("Enter your option: ")
      return option

  def performBookActions(gContext):
      booksOption = BookActions.booksMenu(gContext)
      os.system('cls' if os.name == 'nt' else 'clear')
      if gContext.userRole == 'LIBRARIAN' and booksOption == '1':
          Book.add()
      elif gContext.userRole == 'LIBRARIAN' and booksOption == '2':
          Book.update()
      elif gContext.userRole == 'LIBRARIAN' and booksOption == '3':
          isbn = input("Enter the ISBN of the book you would like to delete: ")
          Book.delete(isbn)
      elif booksOption == '4':
          searchStr = ''
          while(searchStr == ''):
              searchStr = input('Enter Book Search String : ')
              bookList = Book.search(searchStr)
              Book.displayList(bookList)
      elif booksOption == '5':
          isbn = input("Enter the ISBN of the book you would like to display: ")
          Book.display_details(isbn)
      elif booksOption == '6':
          return False
      else:
          print("Not a valid option. Please try again.")
      input("Press Enter Key to Continue...")
      return True