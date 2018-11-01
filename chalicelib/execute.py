from chalicelib import reports, utilities

import logging

logger = logging.getLogger(__name__)


@utilities.check_exceptions
def executor(name_of_report, bucket, key):
    try:
        report = getattr(reports, name_of_report)()
        report.load_from_csv(bucket, key)
        report.transform_csv_df()
        google_ids = report.google_play_order_ids()
        report.load_from_sql(google_ids)
        report.transform_sql_df()
        report.dataframe_to_s3(bucket)
    except Exception as e:
        logger.error(e.args[0])


@utilities.check_exceptions
def select_report(num):
    reports_mapping = {'1': "RevenueReport", '2': "SalesReport"}
    if num in reports_mapping.keys():
        return reports_mapping[num]
