import os
from transaction.transaction import Transaction

class TransactionActions:
  def transactionsMenu(gContext):
      os.system('cls' if os.name == 'nt' else 'clear')
      print("\nTransactions Menu:")
      print("1. Check Out")
      print("2. Check In")
      print("3. Get Outstanding Txns")
      print("4. Get Fine Due")
      print("5. Pay Fine Due")
      print("6. Back to Main Menu")
      option = input("Enter your option: ")
      return option

  def performTransactionActions(gContext):
      transcationsOption = TransactionActions.transactionsMenu(gContext)
      os.system('cls' if os.name == 'nt' else 'clear')
      userId = gContext.userId
      if(gContext.userRole == 'LIBRARIAN'):
          userId = ''
      if transcationsOption == '1':
          Transaction.check_out(userId)
      elif transcationsOption == '2':
          Transaction.check_in(userId)
      elif transcationsOption == '3':
          txnList = Transaction.getOutstandingTransactions(userId)
          Transaction.displayList(txnList)
      elif transcationsOption == '4':
          print("Total Fine OutStanding is : $ %4.2f" % (Transaction.getTotalFineOutstanding(userId)))
      elif transcationsOption == '5':
          Transaction.pay_fine(userId)
      elif transcationsOption == '6':
          return False
      else:
          print("Not a valid option. Please try again.")
      input("Press Enter Key to Continue...")
      return True