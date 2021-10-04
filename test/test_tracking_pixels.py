import unittest
import pandas as pd
from datetime import datetime
from report.tracking_pixels import *
from pandas._testing import assert_frame_equal


class TestTrackingPixelsReport(unittest.TestCase):

    def setUp(self):
        self.log_path = os.path.join('.', 'samples', 'example1.log')

    def test_open_log(self):
        # arrange
        expected_columns = ['timestamp', 'url', 'userid']

        # act
        df = open_log(self.log_path)
        columns_df = list(df.columns)

        # assert
        self.assertTrue(type(df), pd.DataFrame)
        self.assertTrue(set(columns_df).intersection(expected_columns))


    def test_convert_timezone(self):
        # arrange
        date_local = datetime.datetime.strptime('2013-09-01T08:00:00+0100', "%Y-%m-%dT%H:%M:%S%z")
        date_utc = datetime.datetime.strptime('2013-09-01T07:00:00+0000', "%Y-%m-%dT%H:%M:%S%z")

        # act
        cv_date = convert_timezone(date_local)

        # assert
        self.assertTrue(cv_date.tzinfo is pytz.utc)
        self.assertEqual(date_local, date_utc)


    def test_clean_data(self):
        # arrange
        input_data = [{'timestamp': '2013-09-01 22:00:00UTC', 'B': None, 'userid ': 0, 'url': '/contact.html'}]

        expected = [{'timestamp': '2013-09-01 22:00:00UTC', 'userid': 0, 'url': '/contact.html'}]
        df_expected = pd.DataFrame(expected)
        df_expected.loc[:, 'timestamp'] = pd.to_datetime(df_expected['timestamp'])

        # act
        df = clean_data(pd.DataFrame(input_data))

        # assert
        assert_frame_equal(df, df_expected)


    def test_calc_statistics(self):
        # arrange
        date_from = datetime.datetime.strptime('2013-09-01T09:00:00+0000', "%Y-%m-%dT%H:%M:%S%z")
        date_to = datetime.datetime.strptime('2013-09-01T09:59:00+0000', "%Y-%m-%dT%H:%M:%S%z")

        data = [{'timestamp': '2013-09-01 09:00:00UTC', 'url': '/contact.html', 'userid': 12345},
                {'timestamp': '2013-09-01 09:00:00UTC', 'url': '/contact.html', 'userid': 12346},
                {'timestamp': '2013-09-01 10:00:00UTC', 'url': '/contact.html', 'userid': 12345},
                {'timestamp': '2013-09-01 11:00:00UTC', 'url': '/contact.html', 'userid': 12347}]

        df_test_data = pd.DataFrame(data)
        df_test_data.loc[:, 'timestamp'] = pd.to_datetime(df_test_data['timestamp'])

        expected = [{'url': '/contact.html', 'pageviews': 2, 'visitors': 2}]
        df_expected = pd.DataFrame(expected)

        # act
        df_result = calc_statistics(df_logs=df_test_data,
                                    date_from=date_from,
                                    date_to=date_to)

        # assert
        assert_frame_equal(df_result, df_expected)