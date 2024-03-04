import os
from user.user import User
from user.patron import Patron
from user.librarian import Librarian

class LoginActions:
  def loginMenu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to the Library Management System!\n")
    print("1. Login")
    print("2. Register")
    print("3. Exit")
    option = input("Enter your option: ")
    return option
  
  def registerMenu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Register User Menu!\n")
    print("1. Register Patron")
    print("2. Register Librarian")
    print("3. Return to Main Menu")
    option = input("Enter your option: ")
    return option

  def performLoginActions():
      loginOption = LoginActions.loginMenu()
      os.system('cls' if os.name == 'nt' else 'clear')
      if loginOption == '1':
          retData = User.login()
          if( retData['success']== False):          
              input("Login Failed! Press Enter to Try Again!")
          else:
              input("Successfully Logged In Press Enter to Continue...")
              return retData
      elif loginOption == '2':
          registerActions = LoginActions.performRegisterActions()
          while  registerActions == 'continue':
              registerActions = LoginActions.performRegisterActions()
          if(registerActions == 'registered'):
            os.system('cls' if os.name == 'nt' else 'clear')
            input("Successfully Registered Press Enter Key to log in!!")
            os.system('cls' if os.name == 'nt' else 'clear')
            retData = User.login()
            if( retData['success']== False):
                input("Login Failed! Press Enter to Try Again!")
            else:
                input("Successfully Logged In Press Enter to Continue...")
                return retData
      elif loginOption == '3':
          return 'exit'
      else:
          print("Not a valid option. Please try again.")
      return 'continue'
  
  def performRegisterActions():
      loginOption = LoginActions.registerMenu()
      os.system('cls' if os.name == 'nt' else 'clear')
      if loginOption == '1':
          Patron().add()
          return 'registered'
      elif loginOption == '2':
          Librarian().add()
          return 'registered'
      elif loginOption == '3':
          return 'exit'
      else:
          print("Not a valid option. Please try again.")
      return 'continue'