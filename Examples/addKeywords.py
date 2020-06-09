# https://developers.google.com/adwords/api/docs/samples/python/basic-operations#add-keywords-to-an-ad-group

# This example adds ad group criteria to an ad group.
# To get ad groups, run get_ad_groups.py.
# The LoadFromStorage method is pulling credentials and properties from a
# "googleads.yaml" file. By default, it looks for this file in your home
# directory. For more information, see the "Caching authentication information"
# section of our README.


from googleads import adwords


AD_GROUP_ID = 'INSERT_AD_GROUP_ID_HERE'


def main(client, ad_group_id):
  # Initialize appropriate service.
  ad_group_criterion_service = client.GetService(
      'AdGroupCriterionService', version='v201809')

  # Construct keyword ad group criterion object.
  keyword1 = {
      'xsi_type': 'BiddableAdGroupCriterion',
      'adGroupId': ad_group_id,
      'criterion': {
          'xsi_type': 'Keyword',
          'matchType': 'BROAD',
          'text': 'mars'
      },
      # These fields are optional.
      'userStatus': 'PAUSED',
      'finalUrls': {
          'urls': ['http://example.com/mars']
      }
  }

  keyword2 = {
      'xsi_type': 'NegativeAdGroupCriterion',
      'adGroupId': ad_group_id,
      'criterion': {
          'xsi_type': 'Keyword',
          'matchType': 'EXACT',
          'text': 'pluto'
      }
  }

  # Construct operations and add ad group criteria.
  operations = [
      {
          'operator': 'ADD',
          'operand': keyword1
      },
      {
          'operator': 'ADD',
          'operand': keyword2
      }
  ]
  ad_group_criteria = ad_group_criterion_service.mutate(
      operations)['value']

  # Display results.
  for criterion in ad_group_criteria:
    print('Keyword ad group criterion with ad group id "%s", criterion id '
          '"%s", text "%s", and match type "%s" was added.'
          % (criterion['adGroupId'], criterion['criterion']['id'],
              criterion['criterion']['text'],
              criterion['criterion']['matchType']))


if __name__ == '__main__':
  # Initialize client object.
  adwords_client = adwords.AdWordsClient.LoadFromStorage()

  main(adwords_client, AD_GROUP_ID)