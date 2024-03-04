import utils.persistentStore as pStore
import json, hashlib
from getpass import getpass
ps = pStore.PersistentStore()

class User:
  def __init__(self, name = "", phone='', emailAddress='', userId = '', userRole = '', password = ''):
    self.name = name
    self.phone = phone
    self.emailAddress = emailAddress
    self.userId = userId
    self.userRole = userRole
    self.password = password

  def getUserInput(self, forDelete=False):
    while(self.userId.strip() == ""):
      self.userId = input("Enter Id: ")
    if(forDelete):
        return
    while(self.name.strip() == ""):          
      self.name = input("Enter Name: ")
    while(self.phone.strip() == ""):          
      self.phone = input("Enter Phone Number: ")
    while(self.emailAddress.strip() == ""):
      self.emailAddress = input("Enter Email: ")

  def registerUser(self):
    self.getUserInput()
    repassword = ''
    while(self.password.strip() == ""):
      self.password = getpass()
      while(repassword.strip() == ''):
        repassword = getpass("Re-enter Password")
      if self.password != repassword:
        print('Passwords dont match try again!')
        self.password = ''
        repassword = ''
    self.password = hashlib.sha256(self.password.encode()).hexdigest()

  def login():
    userId = ''
    password = ''
    while(userId.strip() == ''):
      userId = input("Username : ")
    while(password.strip() == ''):
      password = getpass()
    return User.valid_password(userId,password)

  def display_details(user):
      print(f"Name: {user['name']}")
      print(f"User ID: {user['userId']}")
      print(f"Phone Number: {user['phone']}")
      print(f"Email Address: {user['emailAddress']}")

  def add(self):
      self.registerUser()
      ps.create('User',self.userId,json.dumps(self.__dict__))

  def update(self):
      self.getUserInput()
      userStr = ps.get('User',self.userId)
      if(userStr == ''):
         print('User Does not exist to update...')
         return
      user = json.loads(userStr)
      user['userId'] = self.userId
      user['name'] = self.name
      user['phone'] = self.phone
      user['emailAddress'] = self.emailAddress
      self.__dict__.update(user)
      ps.update('User',self.userId,json.dumps(self.__dict__))

  def delete(userId):
      if ps.get('User',userId) != '':
          ps.delete("User",userId)
      else:
          print("Cannot delete as that User does not exist!")
  
  def valid_password(userId, password):
      userStr = ps.get('User',userId)
      if(userStr != ''):
        user = json.loads(userStr)
        pw_hash = hashlib.sha256(password.encode()).hexdigest()
        if user['password'] == pw_hash:
            return {'success':True, 'userId':userId, 'userRole':user['userRole']}
      return {'valid_password':False, 'userId':userId, 'userRole':''}
