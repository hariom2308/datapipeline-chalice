from abc import ABC, abstractmethod
import pandas as pd
import boto3
import re
from sqlalchemy import create_engine
import time
from chalicelib import utilities, secretsmanager


class BaseRevenueReport(ABC):

    def __init__(self):
        self.dataframe = None
        self.engine = None

    @utilities.logs_decorator
    def load_from_csv(self, bucket, key):
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=bucket, Key=key)
        self.dataframe = pd.read_csv(obj['Body'])

    @utilities.logs_decorator
    def sql_connect_and_create_engine(self):
        credentials = secretsmanager.get_secret()
        server = f"mysql+pymysql://{credentials['USER']}:{credentials['PASSWORD']}@{credentials['HOST']}:{credentials['PORT']}/{credentials['SCHEMA']}"
        self.engine = create_engine(server, echo=False)


class RevenueReport(BaseRevenueReport):

    columns = ["Description", "Transaction Type", "Merchant Currency", "Buyer Currency", "Buyer Country",
               "Amount (Buyer Currency)", "Amount (Merchant Currency)"]
    columns_mapping = {'Amount (Buyer Currency)': 'Buyer Amount', 'Amount (Merchant Currency)': 'Merchant Amount'}
    columns_final = ['Description', 'Transaction Type', 'Buyer Country', 'Merchant Currency', 'Buyer Currency',
                     'Buyer Amount', 'Merchant Amount', 'Google Fee']

    def __init__(self):
        self.sql_df = None
        self.merged_df = None

    @utilities.logs_decorator
    def google_play_order_ids(self):
        return tuple(list(self.dataframe['google_play_order_id']))

    @utilities.logs_decorator
    def transform_csv_df(self):
        df = self.dataframe
        df = df[df['Buyer Currency'] == 'EUR']
        df = df[__class__.columns]
        df.rename(columns=__class__.columns_mapping, inplace=True)
        df["google_play_order_id"] = df.apply(lambda x: re.search('([0-9]+-)+[0-9]+', x['Description']).group(0)
                                                        if re.search('([0-9]+-)+[0-9]+', x['Description'])
                                                        else re.search('[.][0-9]+', x['Description']).group(0)[1:],
                                                        axis=1)
        self.dataframe = df

    @utilities.logs_decorator
    def load_from_sql(self, list_of_google_id):
        sql = f"""
            SELECT min(created_at) AS registration_date, google_play_order_id
            FROM google_payment_fetched_fact
            WHERE google_play_order_id IN {list_of_google_id}
            GROUP BY google_play_order_id;

            """
        self.sql_connect_and_create_engine()
        self.sql_df = pd.read_sql_query(sql, self.engine)

    @utilities.logs_decorator
    def transform_sql_df(self):
        df2 = self.sql_df
        self.merged_df = pd.merge(self.dataframe, df2, on=['google_play_order_id'], how='left')
        self.merged_df['Google Fee'] = self.merged_df.apply(lambda x:
                                                            0.2 * x['Merchant Amount']
                                                            if x['registration_date'] < pd.Timestamp('2018-01-01')
                                                            else 0.1 * x['Merchant Amount'], axis=1)
        self.merged_df = self.merged_df[__class__.columns_final]

    @utilities.logs_decorator
    def dataframe_to_s3(self, bucket):
        file_name = 'Reports/revenueReport' + time.strftime("%Y%m%d-%H%M%S") + '.csv'
        data = self.merged_df.to_csv(None)
        s3 = boto3.client('s3')
        s3.put_object(Bucket=bucket, Key=file_name, Body=data)
