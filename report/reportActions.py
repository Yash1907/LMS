import os
from report.report import Report

class ReportActions:
  def reportsMenu():
      os.system('cls' if os.name == 'nt' else 'clear')
      print("\nReports Menu:")
      print("1. Checked Out Books Report")
      print("2. Outstanding Dues Report")
      print("3. Total Outstanding Dues")
      print("4. Back to Main Menu")
      option = input("Enter your option: ")
      return option

  def performReportActions():
      reportsOption = ReportActions.reportsMenu()
      os.system('cls' if os.name == 'nt' else 'clear')
      if reportsOption == '1':
          Report.displayList(Report.getCheckedOutBooks())
      elif reportsOption == '2':
          Report.displayList(Report.getOutstandingFineDues())
      elif reportsOption == '3':
          totalDues = Report.getTotalFineOutstanding()
          print("Total Outstanding Amount of all dues is %6.2f" % (totalDues))
      elif reportsOption == '4':
          return False
      else:
          print("Not a valid option. Please try again.")
      input("Press Enter Key to Continue...")
      return True