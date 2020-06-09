from googleads import adwords
import uuid


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

    # Operations holds all the objects and all the Ad Groups we want to add
    operations = []

    for campaign in data:
        campaignName = '[C] ' + campaign.name
        for keyword in campaign.keywords:
          operations.append({
            'operator': 'ADD',
          'operand': {
              'campaignName': campaignName,
              'name': 'Earth to Venus Cruises #%s',
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

        
    ad_group_service = adwords_client.GetService('AdGroupService', version='v201809')
        

    # Construct operations and add ad groups.
    operations = [{
        'operator': 'ADD',
        'operand': {
            'campaignName': campaignName,
            'name': 'Earth to Mars Cruises #%s' % uuid.uuid4(),
            'status': 'ENABLED',
            'biddingStrategyConfiguration': {
                'bids': [
                    {
                        'xsi_type': 'CpcBid',
                        'bid': {
                            'microAmount': '1000000'
                        },
                    }
                ]
            },
            'settings': [
                {
                    # Targeting restriction settings. Depending on the
                    # criterionTypeGroup value, most TargetingSettingDetail only
                    # affect Display campaigns. However, the
                    # USER_INTEREST_AND_LIST value works for RLSA campaigns -
                    # Search campaigns targeting using a remarketing list.
                    'xsi_type': 'TargetingSetting',
                    'details': [
                        # Restricting to serve ads that match your ad group
                        # placements. This is equivalent to choosing
                        # "Target and bid" in the UI.
                        {
                            'xsi_type': 'TargetingSettingDetail',
                            'criterionTypeGroup': 'PLACEMENT',
                            'targetAll': 'false',
                        },
                        # Using your ad group verticals only for bidding. This is
                        # equivalent to choosing "Bid only" in the UI.
                        {
                            'xsi_type': 'TargetingSettingDetail',
                            'criterionTypeGroup': 'VERTICAL',
                            'targetAll': 'true',
                        },
                    ]
                }
            ]
        }
    }, {
        'operator': 'ADD',
        'operand': {
            'campaignId': campaign_id,
            'name': 'Earth to Venus Cruises #%s' % uuid.uuid4(),
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
    }]
    ad_groups = ad_group_service.mutate(operations)

    # Display results.
    for ad_group in ad_groups['value']:
        print('Ad group with name "%s" and id "%s" was added.'
              % (ad_group['name'], ad_group['id']))
