import unittest
import os, sys
daos_path = os.path.abspath(os.path.join('..'))
sys.path.append(daos_path)
from daos import tennisAtpDao as dao
import pandas as pd


class tennis_atp_dao_test(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        return 

    def test_can_concatenate_multiple_files(self):
        directory = r'test_data/single_match'
        dao.MEN_DATA_DIR = directory
        dao.WOMEN_DATA_DIR = directory
        atp_c_df, wta_c_df = dao.read_by_date(1, latest=3)

        # Technical debt: Compare whole row, not just winner name
        assert(len(atp_c_df[atp_c_df.winner_name == 'Stanislas Wawrinka']) == 1)
        assert(len(atp_c_df[atp_c_df.winner_name == 'Tatsuma Ito']) == 1)
        assert(len(atp_c_df[atp_c_df.winner_name == 'Austin Krajicek']) == 1)

    def test_calculates_set_common_opponents(self):
        directory         = r'test_data/common_opponents'
        dao.MEN_DATA_DIR      = directory
        dao.WOMEN_DATA_DIR      = directory
        set_com_opps, df_com_opps = dao.common_opponents('Stanislas Wawrinka','Tatsuma Ito',
                                                          earliest=1,
                                                          latest=1)

        assert(len(set_com_opps) == 1)
        assert('Austin Krajicek' in set_com_opps)

    def test_ignores_input_players_as_comm_opponents(self):
        directory = r'test_data/common_opponents_ignore_players'
        dao.MEN_DATA_DIR = directory
        dao.WOMEN_DATA_DIR = directory

        set_com_opps, df_com_opps = dao.common_opponents('Stanislas Wawrinka','Tatsuma Ito',
                                                         earliest=1,latest=1, courts=["Hard"])

        assert(len(set_com_opps) == 1)
        assert('Austin Krajicek' in set_com_opps)
        assert('Stanislas Wawrinka' not in set_com_opps)
        assert('Tatsuma Ito' not in set_com_opps)
                

    # Should have 2 of these, one for common opponents and another for data.
    def test_ignores_if_row_contains_nan_values(self):
        directory = r'test_data/common_opponents_nan_values'
        dao.MEN_DATA_DIR = directory
        dao.WOMEN_DATA_DIR = directory
        com_opps, df = dao.common_opponents('Stanislas Wawrinka','Tatsuma Ito',
                                            earliest=1,latest=1)
       
        assert(len(com_opps) == 0)
        assert(len(df) == 0)

    def test_can_filter_courts(self):
        directory = 'test_data/common_opponents'
        dao.MEN_DATA_DIR = directory
        dao.WOMEN_DATA_DIR = directory

        com_opps, df = dao.common_opponents('Stanislas Wawrinka','Tatsuma Ito',
                                            earliest=1,latest=1,
                                            courts=["Hard"])
        self.assertEqual(len(com_opps),1)
        self.assertEqual(len(df),2)

    def test_can_filter_by_player(self):
        directory         = r'test_data/filter_by_player'
        dao.MEN_DATA_DIR  = directory
        dao.WOMEN_DATA_DIR  = directory
        atp_df_1, wta_df_1 = dao.read_by_date(1, latest=1)

        df = dao.filter_by_player(atp_df_1,'Stanislas Wawrinka')

        for index, row in df.iterrows():
            assert (row['winner_name'] == 'Stanislas Wawrinka') or (row['loser_name'] == 'Stanislas Wawrinka')

    def test_can_filter_by_multiple_players(self):
        directory         = r'test_data/filter_by_multiple_player'
        dao.MEN_DATA_DIR  = directory
        dao.WOMEN_DATA_DIR  = directory
        atp_df_1, wta_df_1 = dao.read_by_date(1, latest=1)

        players = ['Stanislas Wawrinka', 'Rafael Nadal']
        df = dao.filter_by_player(atp_df_1,players)

        for index, row in df.iterrows():
            has_filter_happened = any(map(lambda x: (row['winner_name'] == x) or (row['loser_name'] == x), players))
            assert has_filter_happened

if __name__ == '__main__':
    unittest.main()
