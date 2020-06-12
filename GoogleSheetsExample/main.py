import myModule
import gspread
from gspread.models import Cell
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("/Users/markfaulkner/Desktop/GitHub_Repos/Google-Ads-Python/GoogleSheetsExample/client_secret.json", scope)

client = gspread.authorize(creds)

masterSheet = client.open("Mark's SKAG Test Sheet")  # Open the spreadhseet
# masterSheet = client.open_by_url("Mark's SKAG Test Sheet")  # Open the spreadhseet by url

pprint(masterSheet)

def getWorksheetValues(worksheetName):
    tempWorksheet = masterSheet.worksheet(worksheetName)
    values = tempWorksheet.col_values(1)
    return values

values = getWorksheetValues("Campaigns")
pprint(values)

values = getWorksheetValues("Negative Keywords")
pprint(values)

# campaignsSheet = masterSheet.worksheet("Campaigns")
# campaigns = campaignsSheet.col_values(1)
# pprint(campaigns)

# negativeKeywordsSheet = masterSheet.worksheet("Negative Keywords")
# negativeKeywords = negativeKeywordsSheet.col_values(1)
# pprint(negativeKeywords)

# newWorksheet = masterSheet.add_worksheet(title="My New Sheet", rows="700", cols="1")

keywords = ['a', 'b', 'c']


def addKeywordsToWorksheet(worksheetName, keywords):
    tempWorksheet = masterSheet.worksheet(worksheetName)
    newCells = []

    for i, keyword in enumerate(keywords, start=1):
        newCells.append(Cell(row=i, col=1, value=keyword))
    
    tempWorksheet.update_cells(newCells)

addKeywordsToWorksheet('My New Sheet', keywords)

# myNewSheet = masterSheet.worksheet("My New Sheet")

# newCells = []

# for i, keyword in enumerate(keywords, start=1):
#     # myNewSheet.update('A'+ str(i), keyword)
#     newCells.append(Cell(row=i, col=1, value=keyword))

# myNewSheet.update_cells(newCells)






# data = sheet1.get_all_records()  # Get a list of all records
# pprint(data)


# row = sheet.row_values(3)  # Get a specific row
# col = sheet.col_values(3)  # Get a specific column
# cell = sheet.cell(1,2).value  # Get the value of a specific cell

# insertRow = ["hello", 5, "red", "blue"]
# sheet.add_rows(insertRow, 4)  # Insert the list as a row at index 4

# sheet.update_cell(2,2, "CHANGED")  # Update one cell

# numRows = sheet.row_count  # Get the number of rows in the sheet