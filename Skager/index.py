from googleads import adwords
import myModule

ENABLE_VARIANT_MATCH_TYPES = True

print('---------- Start ----------')

# adwords_client = adwords.AdWordsClient.LoadFromStorage('/Users/markfaulkner/Desktop/pythonTest/googleads.yaml')
adwords_client = adwords.AdWordsClient.LoadFromStorage('/Users/markfaulkner/Desktop/GitHub_Repos/Google-Ads-Python/googleads.yaml')

# Campaigns List
campaigns = ['paramotor', 'ppg', 'paraglider']

# Get Keyword Suggestions
print('Getting keywords...')
data = myModule.getKeywordsForAllCampaigns(adwords_client, campaigns, 2)

# Create Campaigns
print('Creating campaigns...')
newCampaigns = myModule.createCampaigns(adwords_client, campaigns)

# Add newly created Campaign Id's to data
print('Assigning new campaign ids to campaign objects...')
for i in range(len(data)):
    data[i].update(id = newCampaigns['value'][i]['id'])

# For each Campaign generate Skags for each match variant
print('Creating skags...')
for campaign in data:
    if ENABLE_VARIANT_MATCH_TYPES:
        myModule.createSkags(adwords_client, campaign, 'broad')
        myModule.createSkags(adwords_client, campaign, 'phrase')
        myModule.createSkags(adwords_client, campaign, 'exact')
        myModule.createSkags(adwords_client, campaign, 'broad match mod')
    else: 
        myModule.createSkags(adwords_client, campaign, 'broad')

print('---------- End ----------')