from google.oauth2 import service_account
from googleapiclient.discovery import build
import pprint




# google sheets
# this is roughly how you get this going
# when i use the class I just import it and build more complete functions


# SERVICE_ACC_FILE='keys.json'

# SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
# creds = None
# creds = service_account.Credentials.from_service_account_file(SERVICE_ACC_FILE, scopes=SCOPES)
# sheetservice = build('sheets', 'v4', credentials=creds)
# driveservice = build('drive', 'v3', credentials=creds)
# sheet = sheetservice.spreadsheets()
# myServices = Services(creds=creds,spreadsheetService=sheet,driveService=driveservice)



class Services():
	def __init__(self, creds, **kwargs):
		# https://google-auth.readthedocs.io/en/latest/_modules/google/oauth2/service_account.html
		self.serviceAcc = creds
		# https://developers.google.com/resources/api-libraries/documentation/sheets/v4/python/latest/index.html
		self.spreadsheets = kwargs['spreadsheetService'] 
		# https://developers.google.com/resources/api-libraries/documentation/drive/v3/python/latest/index.html
		self.drive = kwargs['driveService']
		self.driveFiles = self.drive.files()
		self.allSpreadsheets = self.getAllSpreadsheets()
		self.allMySpreadsheets = self.getAllSpreadsheetsOwned()
	

	def files(self):
		
		''' Returns a list of File Objects in drive '''
		
		listOfFiles = self.drive.files().list().execute()['files']
		return listOfFiles
		

	def createSpreadsheet(self, title):
		''' Args:
				title 
			Function:
				Creates a spreadsheet with the given title in the drive 
			Returns:
				The url of the spreadsheet'''

		spread_body = {'properties': {'title': title}}
	
		s = self.spreadsheets.create(body=spread_body).execute()
		return (s['spreadsheetUrl'])
	
	def getSpreadsheet(self, spId):
	
		'''
			Args:
				spId: a spread shit id 
			Returns:
				spreadsheet object
			Function:
				uses sheetsAPI to get the spreadsheet object  DOCS: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets
			ex:
				spId like "1mhHlSyFVnTCemdeikZQc1u4FxUTx8VdVAH0Bt-XdhN0" it will respond with the spreadsheet object  '''
				
				
		resp = self.get(spreadsheetId=spId).execute()
		print(resp['sheets'])
		return resp
	
	def getAllSpreadsheets(self):
	
		''' Function:
				gets all the spreadsheets that the service acc has access to
			Returns:
				a list of spreadsheets '''
		
		resp = self.driveFiles.list(q="mimeType='application/vnd.google-apps.spreadsheet'").execute()
		return resp['files']
	
	
	def getAllSpreadsheetsOwned(self):
	
		''' returns a list of all the file(objects) in the drive that are owned by the specified service accounts'''
		
		resp = self.driveFiles.list(q=f"mimeType='application/vnd.google-apps.spreadsheet' and '{self.serviceAcc.service_account_email}' in owners").execute()
		# resp[files] is a dict of dict for file in files
		return resp['files']
	
	
	def delAllSpreadsheetsOwned(self):
	
		''' deletes all the spreadsheets that you are the owner of '''
		
		resp = self.getAllSpreadsheetsOwned()
		for files in resp:
			self.drive.files().delete(fileId=files['id']).execute()
			print(f'deleted spreadsheet with name: {files["name"]}')
	
	def delSheetVals(self, spId, rang):
		
		''' resets all the values in a range in a spreadsheet  '''
		
		self.values().clear(spId,range=rang).execute()
		
	def listAllSheets(self,spId):
		''' Args:
				takes a spreadsheetId 
			Returns:
				A list of all the sheets in a spreadsheet
			Note: in this case sheets refers to actual sheets !spreadsheets '''
			
			
		resp = getSpreadsheet(self, spId)
		sheets = resp['sheets']
			
		return sheets


if __name__== "__main__":
	main()

# me llaman el ninyo wacha
