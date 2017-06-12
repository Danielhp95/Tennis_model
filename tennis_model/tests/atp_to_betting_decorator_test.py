import unittest
import datetime
import os, sys
daos_path = os.path.abspath(os.path.join('..'))
sys.path.append(daos_path)
from daos import bettingDao as betdao
from daos import tennisAtpDao as atpdao
from daos.decorators import atp_to_betting as dec
import pandas as pd
from datetime import datetime


class atp_to_betting_decorator_test(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        return

    def test_change_name_atp_to_betting(self):
        df = pd.DataFrame(zip(['Rafael Nadal'],['Roger Federer']), 
                          columns=['winner_name','loser_name'])
        df = dec.change_name_atp_to_betting(df)
        assert df.loc[0]['winner_name'] == 'Nadal R.'
        assert df.loc[0]['loser_name'] == 'Federer R.'

    def test_change_date_betting_to_atp(self):
        df = pd.DataFrame(['2017-01-01'], columns=['Date'])
        df = dec.change_date_betting_to_atp(df)
        assert df.loc[0]['Date'] == '20170101'

    def test_change_date_atp_betting(self):
        df = pd.DataFrame(['20170101'], columns=['tourney_date'])
        df = dec.change_date_atp_to_betting(df)
        assert str(df.loc[0]['tourney_date']) == '2017-01-01 00:00:00'

    def test_dates_within_range_same_month(self):
        d1 = '2017-01-01'
        d2 = '2017-01-03'
        within_range = dec.dates_within_range(2, d1,d2)
        assert within_range

    def test_dates_within_range_different_month(self):
        d1 = '2017-01-31'
        d2 = '2017-02-03'
        within_range = dec.dates_within_range(4, d1,d2)
        assert within_range

    def test_dates_within_range_different_year(self):
        d1 = '2016-12-31'
        d2 = '2017-01-03'
        within_range = dec.dates_within_range(4, d1,d2)
        assert within_range

    def test_fix_dates_discrepancies(self):
        directory =  'test_data/atp_to_betting_decorator/'
        df1 = pd.read_csv(directory + 'atp1.csv')
        df2 = pd.read_csv(directory + 'bet1.csv')

        df1_f, df2_f = dec.fix_dates_discrepancies(df1, df2, range_in_days=1)
       
        assert str(df1_f.loc[0]['tourney_date']) == '2006-01-02'
        assert str(df1_f.loc[1]['tourney_date']) == '2006-01-09'

    def test_join_atp_bet_tables(self):
        directory =  'test_data/atp_to_betting_decorator/'
        df1 = pd.read_csv(directory + 'atp2.csv')
        df2 = pd.read_csv(directory + 'bet2.csv')

        joint_df = dec.join_atp_and_bet_tables(atp=df1,bet=df2)
        assert len(joint_df) == 2
        assert joint_df.loc[0]['B365W'] == 1.28
        assert joint_df.loc[0]['loser_hand'] == 'R'
        

