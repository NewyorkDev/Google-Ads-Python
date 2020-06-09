# https://developers.google.com/adwords/api/docs/samples/python/basic-operations#add-campaigns

import datetime
import uuid
from googleads import adwords


def main(client):
  # Initialize appropriate services.
  campaign_service = client.GetService('CampaignService', version='v201809')
  budget_service = client.GetService('BudgetService', version='v201809')

  # Create a budget, which can be shared by multiple campaigns.
  budget = {
      'name': 'Interplanetary budget #%s' % uuid.uuid4(),
      'amount': {
          'microAmount': '50000000'
      },
      'deliveryMethod': 'STANDARD'
  }

  budget_operations = [{
      'operator': 'ADD',
      'operand': budget
  }]

  # Add the budget.
  budget_id = budget_service.mutate(budget_operations)['value'][0][
      'budgetId']

  # Construct operations and add campaigns.
  operations = [{
      'operator': 'ADD',
      'operand': {
          'name': 'Interplanetary Cruise #%s' % uuid.uuid4(),
          # Recommendation: Set the campaign to PAUSED when creating it to
          # stop the ads from immediately serving. Set to ENABLED once you've
          # added targeting and the ads are ready to serve.
          'status': 'PAUSED',
          'advertisingChannelType': 'SEARCH',
          'biddingStrategyConfiguration': {
              'biddingStrategyType': 'MANUAL_CPC',
          },
          'endDate': (datetime.datetime.now() +
                      datetime.timedelta(365)).strftime('%Y%m%d'),
          # Note that only the budgetId is required
          'budget': {
              'budgetId': budget_id
          },
          'networkSetting': {
              'targetGoogleSearch': 'true',
              'targetSearchNetwork': 'true',
              'targetContentNetwork': 'false',
              'targetPartnerSearchNetwork': 'false'
          },
          # Optional fields
          'startDate': (datetime.datetime.now() +
                        datetime.timedelta(1)).strftime('%Y%m%d'),
          'frequencyCap': {
              'impressions': '5',
              'timeUnit': 'DAY',
              'level': 'ADGROUP'
          },
          'settings': [
              {
                  'xsi_type': 'GeoTargetTypeSetting',
                  'positiveGeoTargetType': 'DONT_CARE',
                  'negativeGeoTargetType': 'DONT_CARE'
              }
          ]
      }
  }, {
      'operator': 'ADD',
      'operand': {
          'name': 'Interplanetary Cruise banner #%s' % uuid.uuid4(),
          'status': 'PAUSED',
          'biddingStrategyConfiguration': {
              'biddingStrategyType': 'MANUAL_CPC'
          },
          'endDate': (datetime.datetime.now() +
                      datetime.timedelta(365)).strftime('%Y%m%d'),
          # Note that only the budgetId is required
          'budget': {
              'budgetId': budget_id
          },
          'advertisingChannelType': 'DISPLAY'
      }
  }]
  campaigns = campaign_service.mutate(operations)

  # Display results.
  for campaign in campaigns['value']:
    print('Campaign with name "%s" and id "%s" was added.'
          % (campaign['name'], campaign['id']))


if __name__ == '__main__':
  # Initialize client object.
  adwords_client = adwords.AdWordsClient.LoadFromStorage()

  main(adwords_client)