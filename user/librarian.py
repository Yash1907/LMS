import json
from user.user import User
import utils.persistentStore as pStore
ps = pStore.PersistentStore()

class Librarian(User):
  def __init__(self, name="", phone='', emailAddress='', libId = '', userRole = 'LIBRARIAN', employeeID = ''):
    super().__init__(name, phone, emailAddress, libId, userRole)
    self.employeeID = employeeID

  def add(self):
      self.registerUser()
      while(self.employeeID.strip() == ""):
        self.employeeID = input("Enter Librarian ID: ")      
      ps.create('User',self.userId,json.dumps(self.__dict__))
  
  def update(self):
      self.getUserInput()
      while(self.employeeID.strip() == ""):
          self.employeeID = input("Enter Librarian ID: ")      
      ps.update('User',self.userId,json.dumps(self.__dict__))