# https://developers.google.com/adwords/api/docs/reference/v201809/ReportDefinitionService
# https://developers.google.com/adwords/api/docs/appendix/reports#keywords
# https://developers.google.com/adwords/api/docs/guides/reporting
# https://developers.google.com/adwords/api/docs/appendix/reports/keywords-performance-report

from googleads import adwords


def main(client):
  # Initialize appropriate service.
  report_downloader = client.GetReportDownloader(version='v201809')

  # Create report query.
  report_query = (adwords.ReportQueryBuilder()
                  .Select('Clicks', 'Impressions', 'Cost', 'CampaignId', 'CampaignName', 'AdGroupId', 'AdGroupName', 'Id', 'Status')
                  # .From('CRITERIA_PERFORMANCE_REPORT')
                  .From('KEYWORDS_PERFORMANCE_REPORT')
                  .Build())

  

  return report_downloader.DownloadReportAsStringWithAwql(
        report_query, 'CSV', skip_report_header=True, skip_column_header=False,
        skip_report_summary=True, include_zero_impressions=True)


if __name__ == '__main__':
  print('Start')
  adwords_client = adwords.AdWordsClient.LoadFromStorage('/Users/markfaulkner/Desktop/GitHub_Repos/Google-Ads-Python/Final/googleads.yaml')

  result = main(adwords_client)

  f = open('test.csv', 'w')
  f.write(result)
  f.close()
  print('End')