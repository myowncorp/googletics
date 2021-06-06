from google.oauth2 import service_account
from googleapiclient.discovery import build
import pprint
from googletics import *

	
	
	
	
def create_highscore_sheet():
	
	# First we need to creat the sheet
	spread_body ={"properties": {"title": 'highscores'}}
	
	spreadsheet = myService.spreadsheets.create(body=spread_body).execute()
	print("created the spreadsheet here: " + spreadsheet['spreadsheetUrl'])
	
	
	batch_req = {
		"updateSheetProperties": {
			"properties": {
				"sheetId": 0, 
				"title": "daily"
			},
			"fields": "title",
			}
		}
	
	batch_body = {'requests': batch_req}
	#now we need to update the sheet name
	
	resp = sheet.batchUpdate(spreadsheetId=spreadsheet['spreadsheetId'], body= batch_body).execute()
	print(resp)
	
def main():
	''' the main purpose of this is to be a more user friendly "pretty" CMD app
		for viewing the google drives/sheets/ and other files of a serviceworker/s
		easily and quickly. Using my library.
	'''
	SERVICE_ACC_FILE='keys.json'

	SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
	creds = None
	creds = service_account.Credentials.from_service_account_file(SERVICE_ACC_FILE, scopes=SCOPES)
	sheetservice = build('sheets', 'v4', credentials=creds)
	driveservice = build('drive', 'v3', credentials=creds)
	sheet = sheetservice.spreadsheets()
	myServices = Services(creds=creds,spreadsheetService=sheet,driveService=driveservice)
		
	
	myServices.createSpreadsheet("babooloo")
if __name__== '__main__':
	main()
	
