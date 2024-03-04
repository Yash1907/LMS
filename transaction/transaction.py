from datetime import datetime, timedelta
import utils.persistentStore as persistentStore
from book.book import Book
from user.patron import Patron
import json
import os
ps = persistentStore.PersistentStore()

class Transaction:
    def __init__(self, bookId='', userId=''):
        self.bookId = bookId
        self.userId = userId
        self.checkoutDate = ''
        self.dueDate = ''
        self.checkinDate = ''
        self.fineAmount = 0
        self.finePaid = False

    def check_out(userId):
        transaction = Transaction().getUserInput(True,userId)
        bookStr = ps.get('Book',transaction.bookId)
        if bookStr == '':
            print("OOS 0 Book is out of stock.")
            return
        book = json.loads(bookStr)
        if int(book['quantity']) > 0:
            Book.update_quantity(transaction.bookId,True)
            Patron.update_booksBorrowed(transaction.userId,True)
            checkOutDateTime = datetime.now()
            transaction.checkoutDate = checkOutDateTime.strftime('%Y-%m-%dT%H:%M:%S')
            # Assuming 14 days for due date
            transaction.dueDate = (checkOutDateTime + timedelta(days=14)).strftime('%Y-%m-%dT%H:%M:%S')
            print(f"Book {book['isbn']} checked out. Due Date: {transaction.dueDate}")
            entityId = transaction.userId + transaction.bookId + transaction.checkoutDate
            ps.create('Transaction',entityId,json.dumps(transaction.__dict__))
        else:
            print("OOS 1 Book is out of stock.")

    def check_in(userId):
        transaction = Transaction().getUserInput(False,userId)
        txnDb = Transaction.getTransactionForCheckIn(transaction.bookId,transaction.userId)
        if txnDb['bookId'] != '':
            transaction.__dict__.update(txnDb)
            transaction.checkinDate = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            Book.update_quantity(transaction.bookId,False)
            Patron.update_booksBorrowed(transaction.userId,False)
            transaction.fineAmount = Transaction.calculate_fine(transaction.dueDate)
            if(transaction.fineAmount > 0):
                Patron.update_fineAmount(transaction.userId,transaction.fineAmount,0)
            print(f"checked in.")
            entityId = transaction.userId + transaction.bookId + transaction.checkoutDate
            ps.update('Transaction',entityId,json.dumps(transaction.__dict__))
        else:
            print("Already checked in.")

    def getTransactionForCheckIn(bookId, userId):
        transactionStrList = ps.getAll('Transaction',userId+bookId)
        transaction = { 'bookId' : ''}
        for transactionStr in transactionStrList:
            transaction = json.loads(transactionStr)
            if(transaction['checkinDate'] == ''):
                break
            transaction = { 'bookId' : ''}
        return transaction
    
    def getOutstandingTransactions(userId=''):
        if(userId == ''):
          while(userId.strip() == ""):          
            userId = input("Enter Patron Id: ")
        transactionStrList = ps.getAll('Transaction',userId)
        transactionList = []
        for transactionStr in transactionStrList:
            transaction = json.loads(transactionStr)
            if(transaction['checkinDate'] == ''):
                transactionList.append(transaction)
                fineAmt = Transaction.calculate_fine(transaction['dueDate'])
                if(fineAmt > 0):
                  transaction['fineAmount'] = fineAmt
                  entityId = transaction['userId'] + transaction['bookId'] + transaction['checkoutDate']
                  ps.update('Transaction', entityId,json.dumps(transaction))
        return transactionList
    
    def getTotalFineOutstanding(userId=''):
        if(userId == ''):
          while(userId.strip() == ""):          
            userId = input("Enter Patron Id: ")
        transactionStrList = ps.getAll('Transaction',userId)
        fineDue = 0
        for transactionStr in transactionStrList:
            transaction = json.loads(transactionStr)
            if(transaction['finePaid'] == False):
                fineDue += float(transaction['fineAmount'])
        return fineDue

    def displayList(list):
        count = 0
        print("%12s %10s %10s %10s %10s %10s" % ("ISBN","PatronID","CheckOut","Due Date","CheckIn","FineDue"))
        for txn in list:
            checkOutDt = txn['checkoutDate'][:10]
            dueDt = txn['dueDate'][:10]
            checkinDt = '' if txn['checkinDate'] == '' else txn['checkinDate'][:10]
            print("%12s %10s %10s %10s %10s %10s" % (txn['bookId'],txn['userId'],checkOutDt,dueDt,checkinDt,txn['fineAmount']))
            count = count+1
            if(count % 10 == 0):
                input("Enter for next page")
                os.system('cls' if os.name == 'nt' else 'clear')
                print("%12s %10s %10s %10s %10s %10s" % ("ISBN","PatronID","CheckOut","Due Date","CheckIn","FineDue"))
        return
    
    def calculate_fine(dueDateStr):
        fineAmount = 0
        dueDate = datetime.fromisoformat(dueDateStr)
        currDate = datetime.now()
        if currDate > dueDate:
            days_overdue = (currDate - dueDate).days
            fineAmount = round(days_overdue * 0.05,2)  # Assuming a fine of $0.05 per day overdue
        return fineAmount
    
    def display_transaction_details(self):
        print(f"Book Id: {self.bookId}")
        print(f"Patron Id: {self.userId}")
        print(f"Checkout Date: {self.checkoutDate}")
        print(f"Checkin Date: {self.checkinDate}")
        print(f"Due Date: {self.dueDate}")
        print(f"Fine Amount: ${self.fineAmount}")
        print(f"Fine Paid: {self.finePaid}")

    def sortBy(txn):
        return txn['dueDate']

    def pay_fine(userId='', amount=''):
        if(userId == ''):
          while(userId.strip() == ""):          
            userId = input("Enter Patron Id: ")
        while(amount.strip() == ""):      
            amount = input("Enter Amount: ")
        amount = float(amount)
        transactionStrList = ps.getAll('Transaction',userId)
        fineDue = 0
        transactionList = []
        for transactionStr in transactionStrList:
            transaction = json.loads(transactionStr)
            if(transaction['finePaid'] == False and transaction['checkinDate'] != ''):
                fineDue += float(transaction['fineAmount'])
                transactionList.append(transaction)
        if(len(transactionList) == 0):
           print("Fines Can be Paid once you check in the books!!")
           return
        transactionList.sort(key=Transaction.sortBy)
        totalFineAmt = 0
        finePaidAmt = amount
        for txn in transactionList:
            totalFineAmt += float(txn['fineAmount'])
            if(amount > 0):
              if (amount >= float(txn['fineAmount'])):
                amount -= float(txn['fineAmount'])
                txn['fineAmount'] = 0
                txn['finePaid'] = True
              else:
                txn['fineAmount'] = round(float(txn['fineAmount']) - amount,2)
                amount = 0
                txn['finePaid'] = False
              entityId = txn['userId'] + txn['bookId'] + txn['checkoutDate']
              ps.update('Transaction', entityId,json.dumps(txn))
        Patron.update_finePaid(userId,totalFineAmt,finePaidAmt)       
    
    def getUserInput(self, checkOutFlag, userId=''):
        if(userId != ''):
            self.userId = userId
        while(self.userId.strip() == ""):          
          self.userId = input("Enter Patron Id: ")        
        while(self.bookId.strip() == ""):
          self.bookId = input(f"Enter Check {'Out' if checkOutFlag==True else 'In'} ISBN: ")
        return self