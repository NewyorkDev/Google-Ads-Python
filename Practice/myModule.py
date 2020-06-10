from googleads import adwords
import uuid
import re


def getKeywordsForAllCampaigns(adwords_client, campaigns, numberOfKeywords):
    data = []
    for campaign in campaigns:
        # getKeywords needs to return a list of keywords
        keywords = getKeywords(adwords_client, campaign, numberOfKeywords)
        data.append({'name': campaign, 'keywords': keywords})
    return data


def getKeywords(adwords_client, campaignName, numberOfKeywords):

    # Initialize appropriate service.
    targeting_idea_service = adwords_client.GetService(
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
        'numberResults': str(numberOfKeywords)
    }

    selector['searchParameters'] = [{
        'xsi_type': 'RelatedToQuerySearchParameter',
        'queries': [campaignName]
        # 'queries': ['apple']
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

    keywords = []

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
        print('No related keywords were found for ' + campaignName)

    return keywords


def createCampaigns(adwords_client, campaignNames):
    print('Create All Campaigns')

    # Initialize appropriate services.
    campaign_service = adwords_client.GetService(
        'CampaignService', version='v201809')
    budget_service = adwords_client.GetService(
        'BudgetService', version='v201809')

    # Create a budget, which can be shared by multiple campaigns.
    budget = {
        'name': 'My random budget #%s' % uuid.uuid4(),
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

    operations = []

    # Construct operations and add campaigns.
    for campaignName in campaignNames:
        operations.append({
            'operator': 'ADD',
            'operand': {
                'name': '[C] ' + campaignName,
                'status': 'PAUSED',
                'advertisingChannelType': 'SEARCH',
                'biddingStrategyConfiguration': {
                    'biddingStrategyType': 'MANUAL_CPC',
                },
                'budget': {
                    'budgetId': budget_id
                },
                'networkSetting': {
                    'targetGoogleSearch': 'true',
                    'targetSearchNetwork': 'true',
                    'targetContentNetwork': 'false',
                    'targetPartnerSearchNetwork': 'false'
                }
            }})

    campaigns = campaign_service.mutate(operations)

    return campaigns
    # # Display results.
    # for campaign in campaigns['value']:
    #     print('Campaign with name "%s" and id "%s" was added.'
    #           % (campaign['name'], campaign['id']))


def createAdGroups(adwords_client, data):
    print('Add Ad Groups!')

    ad_group_service = adwords_client.GetService('AdGroupService', version='v201809')

    # Operations holds all the objects and all the Ad Groups we want to add
    operations = []

    for campaign in data:
        campaignName = '[C] ' + campaign['name']
        for keyword in campaign['keywords']:
          print(keyword, campaignName)
          operations.append({
            'operator': 'ADD',
          'operand': {
              'campaignId': campaign['id'],
              'name': '[AG] [SKAG] ' + keyword,
              'status': 'ENABLED',
              'biddingStrategyConfiguration': {
                  'bids': [
                      {
                          'xsi_type': 'CpcBid',
                          'bid': {
                              'microAmount': '1000000'
                          }
                      }
                  ]
              }
          }
          })

    ad_groups = ad_group_service.mutate(operations)

    return ad_groups

    # Display results.
    # for ad_group in ad_groups['value']:
    #     print('Ad group with name "%s" and id "%s" was added.'
    #           % (ad_group['name'], ad_group['id']))


def addKeywordsToAdGroups(adwords_client, ad_groups):
    ad_group_criterion_service = adwords_client.GetService('AdGroupCriterionService', version='v201809')

    operations = []

    for ad_group in ad_groups['value']:
        adGroupId = ad_group['id']
        adGroupName = ad_group['name']
        keyword = adGroupName[12:]

        operations.append({
            'operator': 'ADD',
            'operand': {
                 'xsi_type': 'BiddableAdGroupCriterion',
                 'adGroupId': adGroupId,
                 'criterion': {
                 'xsi_type': 'Keyword',
                 'matchType': 'BROAD', # or PHRASE, EXACT
                 'text': keyword
                 }
            }
        })

    ad_group_criteria = ad_group_criterion_service.mutate(operations)['value']
    
    return ad_group_criteria


def appendVariantMatchTypes(campaigns):
    # For every keyword in each campaign we need to generate 3 or 4 variants and append to the list

    for campaign in campaigns:
        newKeywords = []

        for keyword in campaign['keywords']:
            newKeywords.append(generateExactMatch(keyword))
            newKeywords.append(generatePhraseMatch(keyword))
            newKeywords.append(generateBroadMatchModifier(keyword))

        for newKeyword in newKeywords:
            campaign['keywords'].append(newKeyword)

    return campaigns


def generateExactMatch(keyword):
    return '[' + keyword + ']'


def generatePhraseMatch(keyword):
    return '"' + keyword + '"'


def generateBroadMatchModifier(keyword):
    
    hasSpace = re.search(" ", keyword)

    if hasSpace != None:
        string = "+" + re.sub(" ", " +", keyword)
        return string

    else:
        return keyword