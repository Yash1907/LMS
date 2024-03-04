import utils.persistentStore as persistentStore
import json, os
ps = persistentStore.PersistentStore()

class Report:
    def getCheckedOutBooks():
        transactionStrList = ps.getAll('Transaction')
        transactionList = []
        for transactionStr in transactionStrList:
            transaction = json.loads(transactionStr)
            if(transaction['checkinDate'] == ''):
                transactionList.append(transaction)
        return transactionList
    
    def getOutstandingFineDues():
        transactionStrList = ps.getAll('Transaction')
        transactionList = []
        for transactionStr in transactionStrList:
            transaction = json.loads(transactionStr)
            if(float(transaction['fineAmount']) > 0 and transaction['finePaid'] == False):
                transactionList.append(transaction)
        return transactionList
    
    def getTotalFineOutstanding():
        transactionStrList = ps.getAll('Transaction')
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
    