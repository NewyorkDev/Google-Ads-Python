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


def createAdGroups(adwords_client, campaignId, keywords):
    ad_group_service = adwords_client.GetService('AdGroupService', version='v201809')

    operations = []

    for keyword in keywords:
          operations.append({
            'operator': 'ADD',
          'operand': {
              'campaignId': campaignId,
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


def addKeywordsToAdGroups(adwords_client, ad_groups, matchType):
    ad_group_criterion_service = adwords_client.GetService('AdGroupCriterionService', version='v201809')

    operations = []

    for ad_group in ad_groups['value']:
        adGroupId = ad_group['id']
        keyword = ad_group['name'][12:]

        operations.append({
            'operator': 'ADD',
            'operand': {
                 'xsi_type': 'BiddableAdGroupCriterion',
                 'adGroupId': adGroupId,
                 'criterion': {
                 'xsi_type': 'Keyword',
                 'matchType': matchType,
                 'text': keyword
                 }
            }
        })

    ad_group_criteria = ad_group_criterion_service.mutate(operations)['value']
    
    return ad_group_criteria


def createSkags(adwords_client, campaign, mt):
    campaignId = campaign['id']
    campaignName = campaign['name']
    originalKeywords = campaign['keywords']
    matchType = 'BROAD'    # 'PHRASE', 'BROAD' or 'EXACT'
    keywords = []

    # Set matchType and alter originalKeywords if need be
    if mt == 'broad':
        matchType = 'BROAD'
        keywords = originalKeywords
    if mt == 'exact':
        matchType = 'EXACT'
        keywords = modifyKeywordList(originalKeywords, 'exact')
    if mt == 'phrase':
        matchType = 'PHRASE'
        keywords = modifyKeywordList(originalKeywords, 'phrase')
    if mt == 'broad match mod':
        matchType = 'BROAD'
        keywords = modifyKeywordList(originalKeywords, 'broad match mod')

    # Create Ad Groups
    ad_groups = createAdGroups(adwords_client, campaignId, keywords)

    # Add Keywords To Ad Groups 'PHRASE', 'BROAD' or 'EXACT'
    ad_group_criteria = addKeywordsToAdGroups(adwords_client, ad_groups, matchType)


def modifyKeywordList(originalKeywords, matchType):

    newKeywords = []

    if matchType == 'exact':
        for keyword in originalKeywords:
            x = '[' + keyword + ']'
            newKeywords.append(x)

    if matchType == 'phrase':
        for keyword in originalKeywords:
            x = '"' + keyword + '"'
            newKeywords.append(x)

    if matchType == 'broad match mod':
        for keyword in originalKeywords:
            hasSpace = re.search(" ", keyword)

            if hasSpace != None:
                x = "+" + re.sub(" ", " +", keyword)
                newKeywords.append(x)
            else:
                x = "+" + keyword
                newKeywords.append(x)

    return newKeywords
