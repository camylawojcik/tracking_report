import os
import argparse
import sys
import dateutil
import pytz
import pandas as pd
from tabulate import tabulate
import datetime


def open_log(path: str) -> pd.DataFrame:
    """ Receives a string indicating the file path and return a dataframe of file data """
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"The file {path} does not exist.")

    try:
        return pd.read_csv(path, sep=";|,|\|", engine="python")

    except:
        raise argparse.ArgumentTypeError(f"The format of file {path} is not valid. Error: {sys.exc_info()[0]} - {sys.exc_info()[1]}")


def convert_timezone(date_convert: datetime) -> datetime:
    """ Receives a datetime with timezone parameter and sets the timezone to UTC """
    return date_convert.astimezone(pytz.utc)


def clean_data(df_data: pd.DataFrame) -> pd.DataFrame:
    """ Remove NaN columns, white spaces from column names and cast timestamp column to datetime

    Args:
        df_data : pd.Dataframe
            DataFrame with raw data

    Return:
         A pd.Dataframe with cleaned data

    """
    try:
        df_data.dropna(axis=1, how="all", inplace=True)
        df_data.columns = df_data.columns.str.replace(' ', '')
        df_data.loc[:, 'timestamp'] = pd.to_datetime(df_data['timestamp'])
        df_data['timestamp'] = df_data['timestamp'].apply(convert_timezone)
        return df_data

    except dateutil.parser.ParserError:
        print('Ops! Invalid date/hour!')
        sys.exit(os.EX_DATAERR)

    except KeyError:
        print('Ops! ', sys.exc_info()[1], 'column was not found.')
        sys.exit(os.EX_DATAERR)

    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit(os.EX_SOFTWARE)


def calc_statistics(df_logs: pd.DataFrame, date_from: datetime, date_to: datetime) -> pd.DataFrame:
    """ Calculate the page views and unique visitors.

    Args:
        df_logs: pd.DataFrame
            Filtered and Cleaned dataframe to generate output report
        date_from: datetime
            Date Range - Initial date
        date_to: datetime
            Date Range - Final date

    Returns:
        A dataframe with the number of page views and visitors for each url.
        Columns: url, pageviews, visitors
    """
    try:
        df_logs = df_logs.loc[(df_logs['timestamp'] >= date_from) & (df_logs['timestamp'] <= date_to)]

        # unique visitors by url
        df = df_logs.groupby("url").agg({"userid": pd.Series.nunique})
        df.rename(columns={'userid': 'visitors'}, inplace=True)

        # pageviews
        data = df_logs.groupby(["url"])
        data = data.size().reset_index(name="pageviews")
        df_merge = pd.merge(data, df, how="inner", on=["url"])

        return df_merge

    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit(os.EX_SOFTWARE)


if __name__ == '__main__':

    # Parse CLI Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("date_from",
                        help="Start date for time range filter. Example: '2013-09-01 09:00:00'.",
                        type=lambda d: dateutil.parser.parse(d))
    parser.add_argument("date_to",
                        help="End date for time range filter. Example: '2013-09-01 10:59:59'.",
                        type=lambda d: dateutil.parser.parse(d))
    parser.add_argument("log",
                        help="Path to a log of website visitors.",
                        type=open_log)
    parser.add_argument("-o", "--output",
                        help="Path to save the output as a CSV file.",
                        required=False,
                        type=str)
    args = parser.parse_args()


    # Standardize datetimes to UTC
    date_from = convert_timezone(args.date_from)
    date_to = convert_timezone(args.date_to)


    # Processing
    df_logs = clean_data(args.log)
    df_result = calc_statistics(df_logs, date_from, date_to)


    # Output
    print(tabulate(df_result, headers='keys', tablefmt='pretty', showindex=False))
    # If output parameter is set, save the file
    if args.output:
        df_result.to_csv(args.output, index=False)