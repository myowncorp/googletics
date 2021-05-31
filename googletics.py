from google.oauth2 import service_account
from googleapiclient.discovery import build
import pprint




# google sheets
SERVICE_ACC_FILE='keys.json'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
creds = None
creds = service_account.Credentials.from_service_account_file(SERVICE_ACC_FILE, scopes=SCOPES)
sheetservice = build('sheets', 'v4', credentials=creds)
driveservice = build('drive', 'v3', credentials=creds)
sheet = sheetservice.spreadsheets()

class Services():
	def __init__(self, creds, **kwargs):
		# https://google-auth.readthedocs.io/en/latest/_modules/google/oauth2/service_account.html
		self.serviceAcc = creds
		# https://developers.google.com/resources/api-libraries/documentation/sheets/v4/python/latest/index.html
		self.spreadsheets = kwargs['spreadsheetService'] 
		# https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/index.html
		self.drive = kwargs['driveService']
		self.driveFiles = self.files()
	

	def files(self):
		
		''' Returns a list of File Objects in drive '''
		
		listOfFiles = self.drive.files().list().execute()['files']
		return listOfFiles
		
	def getSpreadsheets(self):
	
		''' Function:
				gets all the spreadsheets that the service acc has access to
			Returns:
				a list of spreadsheets '''
		
		resp = self.drive.files().list(q="mimeType='application/vnd.google-apps.spreadsheet'").execute()
		# for files in resp['files']:
			# print(f' Heres the spreadsheet name  {files["name"]} and here its ID {files["id"]} ')
			
		return resp['files']
	
	def createSheet(self, title):
		''' creates a spreadsheet with the given title in the drive '''
	

		spread_body = {'properties': {'title': title}}
	
		s = self.spreadsheets.create(body=spread_body).execute()
		return (s['spreadsheetUrl'])
	
	
#create a sheet
def create_sheet(title):
	
	''' creates a spreadsheet with the given title in the drive '''
	
	# will create a sheet with a title
	spread_body = {'properties': {'title': title}}
	
	spreadsheet = sheet.create(body=spread_body).execute()
	print(spreadsheet['spreadsheetUrl'])
	

def get_sheet(spId):
	'''
		Args:
			spId: a spread shit id 
		Returns:
			spreadsheet object
		Function:
			uses sheetsAPI to get the spreadsheet object  DOCS: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets
		ex:
			spId like "1mhHlSyFVnTCemdeikZQc1u4FxUTx8VdVAH0Bt-XdhN0" it will responde with the spreadsheet object  '''
			
			
	resp = sheet.get(spreadsheetId=spId).execute()
	print(resp['sheets'])
	return resp
	
def get_all_sheets():
	
	''' Function:
			gets all the spreadsheets that the service acc has access to
		Returns:
			a list of spreadsheets '''
	
	resp = driveservice.files().list(q="mimeType='application/vnd.google-apps.spreadsheet'").execute()
	for files in resp['files']:
		print(f' Heres the spreadsheet name  {files["name"]} and here its ID {files["id"]} ')
		
	return resp['files']
	
def get_all_sheets_owned(email):
	
	''' returns a list of all the file(objects) in the drive that are owned by the specified service accounts'''
	
	resp = driveservice.files().list(q=f"mimeType='application/vnd.google-apps.spreadsheet' and '{email}' in owners").execute()
	print("Here is all the spreadsheets you own: ")
	for files in resp['files']:
		print(f' Name: {files["name"]} ID: {files["id"]} ')
		
	return resp['files']
	
	
def del_all_sheets():
	
	''' deletes all the spreadsheets that you are the owner of '''
	
	resp = get_all_sheets_owned(SERVICE_ACC_EMAIL)
	for files in resp:
		driveservice.files().delete(fileId=files['id']).execute()
		print(f'deleted spreadsheet with name: {files["name"]}')

def del_sheet_vals(spId, rang):
	
	''' resets all the values in a range in a spreadsheet  '''
	
	sheet.values().clear(spId,range=rang).execute()
	

def create_highscore_sheet():
	
	# First we need to creat the sheet
	spread_body ={"properties": {"title": 'highscores'}}
	
	spreadsheet = sheet.create(body=spread_body).execute()
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
	
def list_all_sheets(spId):
	''' Args:
			takes a spreadsheetId 
		Returns:
			A list of all the sheets in a spreadsheet
		Note: in this case sheets refers to actual sheets !spreadsheets '''
		
		
	resp = get_sheet(spId)
	sheets = resp['sheets']
		
	return sheets


def main():
	myService = Services(creds=creds,spreadsheetService=sheetservice, driveService=driveservice)
	SERVICE_ACC_EMAIL= myService.creds.service_account_email
	return 0

if __name__== "__main__":
	main()
