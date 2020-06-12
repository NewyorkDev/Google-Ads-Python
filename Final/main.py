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
ENABLE_VARIANT_MATCH_TYPES = True
KEYWORDS_PER_CAMPAIGN = 100

print('---------- Start ----------')

print('Creating AdWords Client...')
adwords_client = adwords.AdWordsClient.LoadFromStorage('/Users/markfaulkner/Desktop/GitHub_Repos/Google-Ads-Python/Final/googleads.yaml')

# Connect to Google Sheet
print('Getting Google Sheet: ' + SPREAD_SHEET_NAME + '...')
spreadsheet = mySheets.getSpreadsheet(SPREAD_SHEET_NAME, SPREAD_SHEET_PATH)

# Get lists of Campaign Names & Negative Keywords from worksheets
print('Getting campaign names from Google Sheet...')
campaignNames = mySheets.getWorksheetValues(spreadsheet, "Campaigns")
print('Getting negative keywords from Google Sheet...')
negativeKeywords = mySheets.getWorksheetValues(spreadsheet, "Negative Keywords")

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

# Create Campaigns in Google Ads
print('Creating campaigns in Google Ads...')
newCampaigns = myAds.createCampaigns(adwords_client, campaignNames)

# Add newly created Campaign Id's to data
print('Assigning new campaign ids to campaign objects...')
for i in range(len(data)):
    data[i].update(id = newCampaigns['value'][i]['id'])

# Add negative keywords to newly created campaigns
print('Adding negative keywords to new campaigns...')
myAds.addNegativeKeywords(adwords_client, newCampaigns['value'], negativeKeywords)

# For each Campaign generate Skags for each match variant
print('Creating skags...')
for campaign in data:
    if ENABLE_VARIANT_MATCH_TYPES:
        myAds.createSkags(adwords_client, campaign, 'broad')
        myAds.createSkags(adwords_client, campaign, 'phrase')
        myAds.createSkags(adwords_client, campaign, 'exact')
        myAds.createSkags(adwords_client, campaign, 'broad match mod')
    else: 
        myAds.createSkags(adwords_client, campaign, 'broad')


print('---------- End ----------')
