import unittest
import os, sys
daos_path = os.path.abspath(os.path.join('..'))
sys.path.append(daos_path)
from daos import bettingDao as dao
import pandas as pd
from pandas import read_excel

class betting_dao_test(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        return

    def test_can_filter_by_date(self):
        directory = r'test_data/betting_data/'
        df_1 = pd.read_excel(directory + '2012.xls')
        df_2 = pd.read_excel(directory + '2013.xlsx')
        df_3 = pd.read_excel(directory + '2012w.xls')
        df_4 = pd.read_excel(directory + '2013w.xlsx')
    
        dao.DATA_DIR = directory
        atp_df, wtp_df = dao.read_by_date(2012, latest=2013)

        assert len(df_1) + len(df_2) == len(atp_df)
        assert len(df_3) + len(df_4) == len(wtp_df)

    def test_can_filter_by_date_ignore_wtp(self):
        directory = r'test_data/betting_data/'
        df_1 = pd.read_excel(directory + '2012.xls')
        df_2 = pd.read_excel(directory + '2013.xlsx')
    
        dao.DATA_DIR = directory
        atp_df, wtp_df = dao.read_by_date(2012, latest=2013, ignore_wtp=True)

        assert len(df_1) + len(df_2) == len(atp_df)
        assert wtp_df == None



    def test_can_filter_by_tournament(self):
        directory = r'test_data/betting_data/test.xlsx'
        df = pd.read_excel(directory)
        df = dao.filter_by_tournament(df, ['Sonic Ericsson Open'])
        for index, row in df.iterrows():
            assert row['Tournament'] == 'Sonic Ericsson Open'

    def test_can_filter_by_tournamnet_round(self):
        directory = r'test_data/betting_data/test.xlsx'
        df = pd.read_excel(directory)
        df = dao.filter_by_round(df, ['1st Round'])

        for index, row in df.iterrows():
            assert row['Round'] == '1st Round'


    def test_can_filter_by_surface(self):
        directory = r'test_data/betting_data/test.xlsx'
        df = pd.read_excel(directory)
        df = dao.filter_by_surface(df, ['Grass'])

        for index, row in df.iterrows():
            assert row['Surface'] == 'Grass'

    def test_can_filter_by_best_of(self):
        directory = r'test_data/betting_data/test.xlsx'
        df = pd.read_excel(directory)
        df = dao.filter_by_best_of(df, 3)

        for index, row in df.iterrows():
            assert row['Best_of'] == 3

    def test_can_filter_by_player(self):
        directory = r'test_data/betting_data/test.xlsx'
        player = 'Wawrinka S.'
        df = pd.read_excel(directory)
        df = dao.filter_by_player(df, player)

        for index, row in df.iterrows():
            assert row['Winner'] == player or row['Loser'] == player 

    def test_can_filter_by_rank_position(self):
        directory = r'test_data/betting_data/test.xlsx'
        mini = 3
        maxi = 30
        df = pd.read_excel(directory)
        df = dao.filter_by_rank_position(df, mini, maximum=maxi)

        for index, row in df.iterrows():
            assert ((row['WRank'] >= mini & row['WRank'] <= maxi) or
                   (row['LRank'] >= mini & row['LRank'] <= maxi))

    def test_can_filter_by_rank_points(self):
        directory = r'test_data/betting_data/test.xlsx'
        mini = 3
        maxi = 30
        df = pd.read_excel(directory)
        df = dao.filter_by_rank_points(df, mini, maximum=maxi)

        for index, row in df.iterrows():
            assert ((row['WPts'] >= mini & row['WPts'] <= maxi) or
                   (row['LPts'] >= mini & row['LPts'] <= maxi))

