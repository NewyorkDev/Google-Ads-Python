# 3rd Party
from googleads import adwords
from googleads import errors
from pprint import pprint

# My modules
import myAds
import mySheets

# Constants
SPREAD_SHEET_NAME = "Mark's SKAG Test Sheet"
SPREAD_SHEET_PATH = "/Users/markfaulkner/Desktop/GitHub_Repos/Google-Ads-Python/GoogleSheetsExample/client_secret.json"
KEYWORDS_PER_CAMPAIGN = 600

print('---------- Start ----------')

print('Creating AdWords Client...')
adwords_client = adwords.AdWordsClient.LoadFromStorage('/Users/markfaulkner/Desktop/GitHub_Repos/Google-Ads-Python/Final/googleads.yaml')

# Connect to Google Sheet
print('Getting Google Sheet: ' + SPREAD_SHEET_NAME + '...')
spreadsheet = mySheets.getSpreadsheet(SPREAD_SHEET_NAME, SPREAD_SHEET_PATH)

# Get list of Campaign Names from worksheets
print('Getting campaign names from Google Sheet...')
campaignNames = mySheets.getWorksheetValues(spreadsheet, "Campaigns")

# Create new Worksheets for campaign names
print('Creating campaign worksheets...')
for campaignName in campaignNames:
    newSheet = mySheets.createWorksheet(spreadsheet, campaignName)

# Need to generate keyword suggestions for each campaign
print('Getting keyword suggestions for campaigns...')
data = myAds.getKeywordsForAllCampaigns(adwords_client, campaignNames, KEYWORDS_PER_CAMPAIGN)

# Save keyword suggestions to google sheets
print('Saving keyword suggestions to Google Sheets...')
for campaign in data:
    mySheets.addKeywordsToWorksheet(spreadsheet, campaign['name'], campaign['keywords'])

print('---------- End ----------')
