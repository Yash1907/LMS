import shutil
import os

class PersistentStore():
  baseLocation = "./dbstore/"
  fileExt = ".dat"
  def __init__(self):
    if(os.path.exists(self.baseLocation) == False):
      os.mkdir(self.baseLocation)

  def get(self,entityName,entityId):
    if(entityName == '' or entityId == ''):
      raise Exception("entityName, entityId Cannot be Empty!")
    retLine = ''
    if(os.path.isfile(self.baseLocation + entityName + self.fileExt) == False):
      return retLine    
    f = open(self.baseLocation  + entityName + self.fileExt,"rt")
    for line in f:
      #print(line)
      if(line.startswith(entityId) == True):
        retLine = line[len(entityId):]
        break
    f.close()
    return retLine
    
  def create(self,entityName,entityId,entityData):
    if(entityName == '' or entityId == '' or entityData == ''):
      raise Exception("entityName, entityId, entityData Cannot be Empty!")
    if(os.path.isfile(self.baseLocation  + entityName + self.fileExt) == True):
      if(self.get(entityName,entityId) != ''):
          raise Exception(entityName + " " + entityId + " Already Exists!!")
    f = open(self.baseLocation  + entityName + self.fileExt,"+at")
    f.write(entityId + entityData + "\n")
    f.close()
    return
  
  def update(self,entityName,entityId,entityData):
    if(entityName == '' or entityId == '' or entityData == ''):
      raise Exception("entityName, entityId, entityData Cannot be Empty!")
    rf = open(self.baseLocation  + entityName + self.fileExt,"rt")
    wf = open(self.baseLocation  + entityName + self.fileExt + "__temp__","+at")
    for line in rf:
      if(line.startswith(entityId) == True):
          wf.write(entityId + entityData + '\n')
      else:
        wf.write(line)
    rf.close()
    wf.close()
    shutil.move(self.baseLocation  + entityName + self.fileExt + "__temp__",self.baseLocation  + entityName + self.fileExt)
    return
  
  def delete(self,entityName,entityId):
    if(entityName == '' or entityId == ''):
      raise Exception("entityName, entityId, entityData Cannot be Empty!")  
    rf = open(self.baseLocation  + entityName + self.fileExt,"rt")
    wf = open(self.baseLocation  + entityName + self.fileExt + "__temp__","+at")
    for line in rf:
      if(line.startswith(entityId) == False):
        wf.write(line)
    rf.close()
    wf.close()
    shutil.move(self.baseLocation  + entityName + self.fileExt + "__temp__",self.baseLocation  + entityName + self.fileExt)
    return
  
  def getAll(self,entityName, partialKey=''):
    if(entityName == ''):
      raise Exception("entityName Cannot be Empty!")
    retList = []
    if(os.path.isfile(self.baseLocation + entityName + self.fileExt) == False):
      return retList    
    f = open(self.baseLocation  + entityName + self.fileExt,"rt")
    for line in f:
      if(partialKey == '' or line.startswith(partialKey) == True):
        retList.append(line[line.find("{"):])
    f.close()
    return retList