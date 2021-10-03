import sys

import dateutil
import pandas as pd
from dateutil import parser, tz

def get_args(args):
    try:
        return parser.parse(args[1]), parser.parse(args[2]), args[3]
    except dateutil.parser.ParserError:
        print('Ops! Invalid date/hour!')

def get_logs(path):
    df = pd.read_csv(path, sep="|")

    return df

def clean_data(df_data):
    try:
        df_data = df_data.dropna(axis=1, how="all")
        df_data.columns = df_data.columns.str.replace(' ', '')
        df_data['timestamp'] = pd.to_datetime(df_data['timestamp'])

        return df_data
    except dateutil.parser._parser.ParserError:
        print('Ops! Invalid date/hour!')
    except KeyError:
        print('Ops! ', sys.exc_info()[1],'column was not found.')
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

def get_result(df_logs, date_from, date_to):
    df_logs = df_logs.loc[(df_logs['timestamp'] >= date_from) & (df_logs['timestamp'] <= date_to)]

    # unique visitors by url
    df = df_logs.groupby("url").agg({"userid": pd.Series.nunique})
    df.rename(columns={'userid': 'visitors'}, inplace=True)

    # pageviews
    data = df_logs.groupby(["url"])
    data = data.size().reset_index(name="pageviews")

    df_merge = pd.merge(data, df, how="inner", on=["url"])

    # df_merge.to_string(index=False)

    return df_merge

if __name__ == '__main__':
    date_from, date_to, path = get_args(sys.argv)

    df_logs = get_logs(path)

    df_logs = clean_data(df_logs)

    df_result = get_result(df_logs, date_from, date_to)

    df_result.to_string(index=False)
    print(df_result)