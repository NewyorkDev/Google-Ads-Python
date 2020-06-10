from googleads import adwords
import myModule
import time

# adwords_client = adwords.AdWordsClient.LoadFromStorage('/Users/markfaulkner/Desktop/pythonTest/googleads.yaml')
adwords_client = adwords.AdWordsClient.LoadFromStorage('/Users/markfaulkner/Desktop/GitHub_Repos/Google-Ads-Python/googleads.yaml')

campaigns = ['paramotor', 'ppg', 'paraglider']

data = myModule.getKeywordsForAllCampaigns(adwords_client, campaigns, 2)
print(data)

#  Now we can either fill a google sheet with the data or start creating campaigns

# Create all campaigns
newCampaigns = myModule.createCampaigns(adwords_client, campaigns)

# ALTERNATIVELY WE COULD LOOP OVER AND CHECK GROUP NAMES BEFORE UPDATING ID
# Need to add campaign ID to the data
for i in range(len(data)):
    data[i].update(id = newCampaigns['value'][i]['id'])

#  Give time for campaigns to be created
# time.sleep(2)

for campaign in newCampaigns['value']:
    print('Campaign with name "%s" and id "%s" was added.'
          % (campaign['name'], campaign['id']))

# Add Ad Groups to newly created campaigns
ad_groups = myModule.createAdGroups(adwords_client, data)

for ad_group in ad_groups['value']:
        print('Ad group with name "%s" and id "%s" was added.'
              % (ad_group['name'], ad_group['id']))

# Ad keyords to Ad Group
ad_group_criteria = myModule.addKeywordsToAdGroups(adwords_client, ad_groups)

for criterion in ad_group_criteria:
    print('Keyword ad group criterion with ad group id "%s", criterion id '
        '"%s", text "%s", and match type "%s" was added.'
        % (criterion['adGroupId'], criterion['criterion']['id'],
            criterion['criterion']['text'],
            criterion['criterion']['matchType']))