import gspread
from gspread.models import Cell
from oauth2client.service_account import ServiceAccountCredentials

def createWorksheet(masterSheet, title):
    newWorksheet = masterSheet.add_worksheet(title=title, rows="700", cols="1")
    return newWorksheet

def getWorksheetValues(masterSheet, worksheetName):
    tempWorksheet = masterSheet.worksheet(worksheetName)
    values = tempWorksheet.col_values(1)
    return values

def addKeywordsToWorksheet(masterSheet, worksheetName, keywords):
    tempWorksheet = masterSheet.worksheet(worksheetName)
    newCells = []

    for i, keyword in enumerate(keywords, start=1):
        newCells.append(Cell(row=i, col=1, value=keyword))
    
    tempWorksheet.update_cells(newCells)

def getSpreadsheet(spreadsheetName, filePath):
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    # creds = ServiceAccountCredentials.from_json_keyfile_name("/Users/markfaulkner/Desktop/GitHub_Repos/Google-Ads-Python/GoogleSheetsExample/client_secret.json", scope)
    creds = ServiceAccountCredentials.from_json_keyfile_name(filePath, scope)
    client = gspread.authorize(creds)
    # masterSheet = client.open("Mark's SKAG Test Sheet")  # Open the spreadhseet
    masterSheet = client.open(spreadsheetName)  # Open the spreadhseet
    # masterSheet = client.open_by_url("https://asdasdfasdf.com")  # Open the spreadhseet by url
    return masterSheet