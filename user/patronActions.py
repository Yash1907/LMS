import os
from user.patron import Patron

class PatronActions:
  def patronsMenu(gContext):
      os.system('cls' if os.name == 'nt' else 'clear')
      print("\nPatrons Menu:")
      if(gContext.userRole == 'LIBRARIAN'):
        print("1. Add User")
        print("2. Update User")
        print("3. Delete User")
        print("4. List Users")
      print("5. Display User")
      print("6. Back to Main Menu")
      option = input("Enter your option: ")
      return option

  def performPatronActions(gContext):
      patronsOption = PatronActions.patronsMenu(gContext)
      os.system('cls' if os.name == 'nt' else 'clear')
      if gContext.userRole == 'LIBRARIAN' and patronsOption == '1':
          Patron().add()
      elif gContext.userRole == 'LIBRARIAN' and patronsOption == '2':
          Patron().update()
      elif gContext.userRole == 'LIBRARIAN' and patronsOption == '3':
          id = input("Enter the ID of the patron you would like to delete: ")
          Patron.delete(id)
      elif gContext.userRole == 'LIBRARIAN' and patronsOption == '4':
          Patron.list()
      elif patronsOption == '5':
          if gContext.userRole == 'LIBRARIAN':
              id = input("Enter the ID of the patron you would like to display: ")
          else:
              id = gContext.userId
          Patron.display_details(id)
      elif patronsOption == '6':
          return False
      else:
          print("Not a valid option. Please try again.")
      input("Press Enter Key to Continue...")
      return True