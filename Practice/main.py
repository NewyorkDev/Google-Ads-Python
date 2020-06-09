from googleads import adwords
import myModule

adwords_client = adwords.AdWordsClient.LoadFromStorage('/Users/markfaulkner/Desktop/pythonTest/googleads.yaml')

campaigns = ['paramotor', 'ppg', 'paraglider']
#  or get keywords from Google Sheets

data = myModule.getKeywordsForAllCampaigns(adwords_client, campaigns, 2)
print(data)

#  Now we can either fill a google sheet with the data or start creating campaigns

# Create all campaigns
newCampaigns = myModule.createCampaigns(adwords_client, campaigns)

for campaign in newCampaigns['value']:
    print('Campaign with name "%s" and id "%s" was added.'
          % (campaign['name'], campaign['id']))

# Add Ad Groups to newly created campaigns
myModule.createAdGroups(adwords_client, data)