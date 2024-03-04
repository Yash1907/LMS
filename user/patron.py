import utils.persistentStore as pStore
import json, os
from user.user import User
ps = pStore.PersistentStore()

class Patron(User):
    def __init__(self, name='', userId='', phone='', emailAddress='', borrowedQty=0, 
                 finesDue=0,finesPaid=0, userRole = "PATRON", password = ''):
        super().__init__(name, phone, emailAddress, userId, userRole, password)
        self.finesDue = finesDue
        self.finesPaid = finesPaid
        self.borrowedQty= borrowedQty

    def display_details(patronId):
        patronStr = ps.get('User',patronId)
        if(patronStr != ''):
          patron = json.loads(patronStr)
          User.display_details(patron)
          print(f"Fines Due: {patron['finesDue']}")
          print(f"Fines Paid To Date: {patron['finesPaid']}")
          print(f"Borrowed Quantity: {patron['borrowedQty']}")
        else:
          print("Patron details not found!")
    
    def update_booksBorrowed(userId, checkOutFlag):
        patronStr = ps.get('User',userId)
        if (patronStr != ''):
          patron = (json.loads(patronStr))
          if(patron['borrowedQty'] == ''):
             patron['borrowedQty'] = '0'
          if(checkOutFlag == True):
              patron['borrowedQty'] = int(patron['borrowedQty']) + 1
          else:
              patron['borrowedQty'] = int(patron['borrowedQty']) - 1
          ps.update('User',patron['userId'],json.dumps(patron))
    
    def update_fineAmount(userId, fineAmountDue, fineAmountPaid):
        patronStr = ps.get('User',userId)
        if (patronStr != ''):
          patron = (json.loads(patronStr))
          if(fineAmountPaid > 0):
             patron['finesPaid'] = patron['finesPaid'] + fineAmountPaid
          patron['finesDue'] = patron['finesDue'] + fineAmountDue - patron['finesPaid']
          ps.update('User',patron['userId'],json.dumps(patron))

    def update_finePaid(userId, fineAmountTotalDue, fineAmountPaid):
        patronStr = ps.get('User',userId)
        if (patronStr != ''):
          patron = (json.loads(patronStr))
          if(fineAmountPaid > 0):
             patron['finesPaid'] = patron['finesPaid'] + fineAmountPaid
          patron['finesDue'] = fineAmountTotalDue
          ps.update('User',patron['userId'],json.dumps(patron))
          
    def list():
       os.system('cls' if os.name == 'nt' else 'clear')
       patronList = ps.getAll('User')
       count = 0
       print("%20s %6s %10s %24s %6s %6s %4s" % ('Name','ID','Phone','Email Address','Fines Due','Fines Paid','Qty Borrowed'))
       for patronStr in patronList:
          count += 1
          obj = json.loads(patronStr)
          if(obj['userRole'] == 'PATRON'):
            print("%20s %6s %10s %24s %6s %6s %4s" % (obj['name'],obj['userId'],obj['phone'],obj['emailAddress'],obj['finesDue'],obj['finesPaid'],obj['borrowedQty']))
          else:
            print("%20s %6s %10s %24s %6s %6s %4s" % (obj['name'],obj['userId'],obj['phone'],obj['emailAddress'],"","",""))
          if count % 10 == 0:
            input("Enter for next page")
            os.system('cls' if os.name == 'nt' else 'clear')
            print("%20s %6s %10s %24s %6s %6s %4s" % ('Name','ID','Phone','Email Address','Fines Due','Fines Paid','Qty Borrowed'))