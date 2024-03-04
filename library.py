# todo login for special user
# todo display details for patron
# todo display details for book

from transaction.transactionActions import TransactionActions
from user.patronActions import PatronActions
from book.bookActions import BookActions
from user.loginActions import LoginActions
from report.reportActions import ReportActions
from user.globalContext import GlobalContext

import os

gContext = GlobalContext()

def menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Main Menu:")
    print("1. Books")
    print("2. Users")
    print("3. Transactions")
    if(gContext.userRole == 'LIBRARIAN'):
      print("4. Reports")
    print("5. Exit")
    option = input("Enter your option: ")
    return option

# Main program loop
def performLibraryActions():
  while True:
      option = menu()  
      if option == '1':
          while BookActions.performBookActions(gContext) == True:
              pass
      elif option == '2':
          while PatronActions.performPatronActions(gContext) == True:
            pass
      elif option == '3':
          while TransactionActions.performTransactionActions(gContext) == True:
              pass
      elif option == '4' and gContext.userRole == 'LIBRARIAN':
          while ReportActions.performReportActions() == True:
              pass          
      elif option == '5':
          print("Program Exited")
          break
      else:
          print("Not a valid option. Please try again.")

def perfomrLoginAction():
  while True:
      retData = LoginActions.performLoginActions()
      if(isinstance(retData,dict) == True):
        if(retData['success'] == True):
            gContext.userId = retData['userId']
            gContext.userRole = retData['userRole']
            performLibraryActions()
      elif(retData == 'exit'):
          break

perfomrLoginAction()