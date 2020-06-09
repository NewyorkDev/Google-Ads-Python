"""This example retrieves keywords that are related to a given keyword.
The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.
"""

from googleads import adwords
import sys, json


# Optional AdGroup ID used to set a SearchAdGroupIdSearchParameter.
# AD_GROUP_ID = 'INSERT_AD_GROUP_ID_HERE'
PAGE_SIZE = 100

def read_in():
    lines = sys.stdin.readlines()
    return json.loads(lines[0])


def main(client):
  campaignNames = read_in()  # Get campaign names from node.js
#   print(campaignNames)

  # Initialize appropriate service.
  targeting_idea_service = client.GetService(
      'TargetingIdeaService', version='v201809')

  # Construct selector object and retrieve related keywords.
  selector = {
      'ideaType': 'KEYWORD',
      'requestType': 'IDEAS'
  }

  selector['requestedAttributeTypes'] = [
      'KEYWORD_TEXT', 'SEARCH_VOLUME', 'CATEGORY_PRODUCTS_AND_SERVICES']

  offset = 0
  selector['paging'] = {
      'startIndex': str(offset),
      'numberResults': str(PAGE_SIZE)
  }

  selector['searchParameters'] = [{
      'xsi_type': 'RelatedToQuerySearchParameter',
      'queries': campaignNames
    #   'queries': ['apple']
  }]

  # Language setting (optional).
  selector['searchParameters'].append({
      'xsi_type': 'LanguageSearchParameter',
      'languages': [{'id': '1000'}]
  })

  # Network search parameter (optional)
  selector['searchParameters'].append({
      'xsi_type': 'NetworkSearchParameter',
      'networkSetting': {
          'targetGoogleSearch': True,
          'targetSearchNetwork': False,
          'targetContentNetwork': False,
          'targetPartnerSearchNetwork': False
      }
  })

  more_pages = True

  keywords = []

  while more_pages:
    page = targeting_idea_service.get(selector)


    # Display results.
    if 'entries' in page:
      for result in page['entries']:
        attributes = {}
        for attribute in result['data']:
          attributes[attribute['key']] = getattr(
              attribute['value'], 'value', '0')
        # print(attributes['KEYWORD_TEXT'])
        keywords.append(attributes['KEYWORD_TEXT'])
    else:
      print('No related keywords were found.')
    offset += PAGE_SIZE
    selector['paging']['startIndex'] = str(offset)
    more_pages = offset < int(page['totalNumEntries'])


  # Initialize client object.
  print(",".join(keywords))


adwords_client = adwords.AdWordsClient.LoadFromStorage('/Users/markfaulkner/Desktop/pythonTest/googleads.yaml')

main(adwords_client)

sys.stdout.flush()