# https://developers.google.com/adwords/api/docs/samples/python/advanced-operations#create-a-negative-broad-match-keywords-list-and-attach-it-to-a-campaign

from googleads import adwords
import myModule


print('---------- Start ----------')

adwords_client = adwords.AdWordsClient.LoadFromStorage('/Users/markfaulkner/Desktop/GitHub_Repos/Google-Ads-Python/googleads.yaml')

negativeKeywords = ['jobs', 'careers', 'boobs', 'sex', 'free', 'diy']

campaigns = myModule.getAllCampaigns(adwords_client)

print(campaigns)

myModule.addNegativeKeywords(adwords_client, campaigns, negativeKeywords)

print('---------- End ----------')