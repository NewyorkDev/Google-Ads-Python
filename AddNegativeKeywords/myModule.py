from googleads import adwords
from googleads import errors
import uuid
import re


def getAllCampaigns(adwords_client):
    campaign_service = adwords_client.GetService('CampaignService', version='v201809')

    # Construct selector and get all campaigns.
    offset = 0
    pageSize = 100
    selector = {
        'fields': ['Id', 'Name', 'Status'],
        'paging': {
            'startIndex': str(offset),
            'numberResults': str(pageSize)
        }
    }

    page = campaign_service.get(selector)

    # Display results.
    if 'entries' in page:
        campaignList = []

        for campaign in page['entries']:
            campaignList.append({ 'id': campaign['id'], 'name': campaign['name'], 'status': campaign['status'] })

        return campaignList
            
    else:
        print('No campaigns were found.')

def addNegativeKeywords(adwords_client, campaigns, negativeKeywords):
    shared_set_service = adwords_client.GetService('SharedSetService', version='v201809')
    shared_criterion_service = adwords_client.GetService('SharedCriterionService', version='v201809')
    campaign_shared_set_service = adwords_client.GetService('CampaignSharedSetService', version='v201809')

    # Keywords to create a shared set of.
    # keywords = ['mars cruise', 'mars hotels']

    # Create shared negative keyword set.
    shared_set = {
        'name': 'API Negative keyword list - %d' % uuid.uuid4(),
        'type': 'NEGATIVE_KEYWORDS'
    }

    # Add shared set.
    operations = [{
        'operator': 'ADD',
        'operand': shared_set
    }]

    response = shared_set_service.mutate(operations)

    if response and response['value']:
        shared_set = response['value'][0]
        shared_set_id = shared_set['sharedSetId']

        print('Shared set with ID %d and name "%s" was successfully added.' % (
            shared_set_id, shared_set['name']
        ))
    else:
        raise errors.GoogleAdsError('No shared set was added.')

        # Add negative keywords to shared set.
    shared_criteria = [
        {
            'criterion': {
                'xsi_type': 'Keyword',
                'text': keyword,
                'matchType': 'BROAD'
            },
            'negative': True,
            'sharedSetId': shared_set_id
        } for keyword in negativeKeywords
    ]

    operations = [
        {
            'operator': 'ADD',
            'operand': criterion
        } for criterion in shared_criteria
    ]

    response = shared_criterion_service.mutate(operations)

    if 'value' in response:
        for shared_criteria in response['value']:
            print('Added shared criterion ID %d "%s" to shared set with ID %d.' % (
                shared_criteria['criterion']['id'],
                shared_criteria['criterion']['text'],
                shared_criteria['sharedSetId']
            ))
    else:
        raise errors.GoogleAdsError('No shared keyword was added.')

    for campaign in campaigns:

            # Attach the articles to the campaign.
        campaign_set = {
            'campaignId': campaign['id'],
            'sharedSetId': shared_set_id
        }

        operations = [
            {
                'operator': 'ADD',
                'operand': campaign_set
            }
        ]

        response = campaign_shared_set_service.mutate(operations)

        if 'value' in response:
            print('Shared set ID %d was attached to campaign ID %d' % (
                response['value'][0]['sharedSetId'], response['value'][0]['campaignId']
            ))
        else:
            raise errors.GoogleAdsError('No campaign shared set was added.')
