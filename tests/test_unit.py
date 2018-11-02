import pandas as pd
from chalicelib import reports


def setup_module(module):
    global d
    global df

    d = {'Description': ['GPA.3321-4440-5047-88266..0', '12999763169054705758.1367969845028899..38', 'GPA.3354-5114-3924-87624'],
         'Transaction Type': ['Charge', 'Charge', 'Charge'],
         'Transaction Date': ['Jul 1, 2018', 'Jul 1, 2018', 'Jul 1, 2018'],
         'Buyer Country': ['DE', 'IT', 'GB'],
         'Merchant Currency': ['EUR', 'EUR', 'EUR'],
         'Buyer Currency': ['EUR', 'EUR', 'GBP'],
         'Amount (Buyer Currency)': [7.64, 11.44, 7.58],
         'Amount (Merchant Currency)': [7.64, 11.44, 8.57]
         }
    df = pd.DataFrame(data=d)


def test_transform_csv_df():
    df1 = reports.RevenueReport()
    df1.dataframe = df
    df1.transform_csv_df()
    rows = df1.dataframe.shape[0]
    cols = df1.dataframe.shape[1]
    assert rows == 2
    assert cols == 8
    assert (df1.dataframe['google_play_order_id'] is not None)
    assert ('3321-4440-5047-88266' in list(df1.dataframe['google_play_order_id']))


# def test_upload_to_s3(monkeypatch):
#     monkeypatch.setattr('index.upload_to_s3', lambda x: 1)
#     assert index.upload_to_s3('accounting.xlsx') == 1
