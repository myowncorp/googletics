import unittest
from googletics import Services
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pprint

class TestServices(unittest.TestCase):

	def setUp(self):
		self.servF='keys.json'
	
		self.scopes = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
		self.creds = service_account.Credentials.from_service_account_file(self.servF, scopes=self.scopes)
		self.sheetservice = build('sheets', 'v4', credentials=self.creds)
		self.driveservice = build('drive', 'v3', credentials=self.creds)
		self.sheet = self.sheetservice.spreadsheets()
		self.myServices = Services(creds=self.creds,spreadsheetService=self.sheet,driveService=self.driveservice)
		
		
	def tearDown(self):
		self.myServices.delAllSpreadsheetsOwned()
		self.sheetservice.close()
		self.driveservice.close()

	def test_service_info(self):
		assert self.creds.service_account_email == 'ninyowacha@funbot-313515.iam.gserviceaccount.com'
		
	def test_delAllSpreadsheetsOwned(self):
		# clear the spread sheets
		self.myServices.delAllSpreadsheetsOwned()
		# get all the spreadsheets
		spreads = self.myServices.getAllSpreadsheetsOwned()
		# check that its a list
		self.assertEqual(type(spreads), list)
		# check that it's empty
		self.assertFalse(spreads)
		# create 2 spreadsheets
		self.myServices.createSpreadsheet("test123")
		self.myServices.createSpreadsheet("test321")
		# check to see if it recognizes them
		self.assertIsNotNone(spreads)
		# delete them again
		self.myServices.delAllSpreadsheetsOwned()
		# check once more
		self.assertFalse(spreads)
		
	def test_getAllSpreadsheets(self):
		spreads = self.myServices.getAllSpreadsheets()
		self.assertIn("rollbot", spreads[0]['name'])
		
	def test_createSpreadsheet(self):
		# check 2 of the same spreadsheet names
		testSpreadsheet1 = self.myServices.createSpreadsheet("sametitle")
		testSpreadsheet2 = self.myServices.createSpreadsheet("sametitle")
		spreads = self.myServices.getAllSpreadsheetsOwned()
		
		
if __name__=='__main__':
	unittest.main()
